import os
import time
import logging
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# ---------------- CPU STABILITY (WINDOWS SAFE) ----------------
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["MKL_SERVICE_FORCE_INTEL"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

torch.set_num_threads(2)

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

START_TIME = time.time()

def elapsed():
    return f"{(time.time() - START_TIME) / 60:.2f} min"

# ---------------- CONFIG ----------------
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LORA_PATH = "lora-nl-sql"
EVAL_DATA = "data/nl_sql_eval.jsonl"

MAX_INPUT_LEN = 192
MAX_NEW_TOKENS =60
# ---------------- LOAD DATA ----------------
logging.info("📦 Loading evaluation dataset...")
dataset = load_dataset("json", data_files=EVAL_DATA)["train"]
logging.info(f"📦 Loaded {len(dataset)} samples | elapsed={elapsed()}")
logging.info(f"🧪 Sample record:\n{dataset[0]}")

# ---------------- LOAD TOKENIZER ----------------
logging.info("🔤 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

# ---------------- LOAD BASE MODEL (ONCE) ----------------
logging.info("🧠 Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float32
)
base_model.eval()

# ---------------- ATTACH LoRA ----------------
logging.info("🧠 Attaching LoRA adapters...")
finetuned_model = PeftModel.from_pretrained(
    base_model,
    LORA_PATH,
    is_trainable=False
)
finetuned_model.eval()
logging.info("✅ LoRA adapters attached successfully")

# ---------------- SQL GENERATION ----------------
def generate_sql(model, instruction, input_text, tag="MODEL"):
    logging.info(f"🚀 [{tag}] Starting generation")

    prompt = f"""### Instruction:
{instruction}

### Input:
{input_text}

### SQL:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_LEN
    )

    start = time.time()
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id
        )

    logging.info(f"⏱ [{tag}] Generation finished in {(time.time() - start):.2f}s")

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "### SQL:" in decoded:
        sql = decoded.split("### SQL:")[-1]
    else:
        sql = decoded

    return sql.strip().lower()


#sanity check
logging.info("🧪 Running single-token sanity generation...")

test_inputs = tokenizer("SELECT 1;", return_tensors="pt")
with torch.inference_mode():
    out = finetuned_model.generate(**test_inputs, max_new_tokens=5)

logging.info("🧪 Sanity generation OK")




# ---------------- EVALUATION ----------------
logging.info("📊 ENTERING EVALUATION LOOP")
logging.info("=" * 80)

base_correct = 0
ft_correct = 0
total = len(dataset)

for idx, example in enumerate(dataset, start=1):
    logging.info(f"▶ Sample {idx}/{total}")

    instruction = example["instruction"]
    input_text = example["input"]
    gold_sql = example["output"].strip().lower()

    logging.info("📘 Instruction:")
    logging.info(instruction)

    logging.info("📥 Input:")
    logging.info(input_text)

    logging.info("🎯 Gold SQL:")
    logging.info(gold_sql)

    base_sql = generate_sql(base_model, instruction, input_text)
    logging.info("🤖 Base model SQL:")
    logging.info(base_sql)

    ft_sql = generate_sql(finetuned_model, instruction, input_text)
    logging.info("🧠 Fine-tuned model SQL:")
    logging.info(ft_sql)

    if gold_sql in base_sql:
        base_correct += 1
        logging.info("✅ Base model: CORRECT")
    else:
        logging.info("❌ Base model: INCORRECT")

    if gold_sql in ft_sql:
        ft_correct += 1
        logging.info("✅ Fine-tuned model: CORRECT")
    else:
        logging.info("❌ Fine-tuned model: INCORRECT")

    elapsed_min = (time.time() - START_TIME) / 60
    eta = (elapsed_min / idx) * (total - idx)

    logging.info(
        f"⏱ Progress {idx}/{total} | elapsed={elapsed_min:.2f} min | ETA={eta:.2f} min"
    )
    logging.info("-" * 80)

# ---------------- RESULTS ----------------
base_acc = (base_correct / total) * 100
ft_acc = (ft_correct / total) * 100

logging.info("✅ Evaluation completed")
logging.info(f"📈 Base model accuracy      : {base_acc:.2f}%")
logging.info(f"📈 Fine-tuned model accuracy: {ft_acc:.2f}%")
logging.info(f"⏱ Total evaluation time    : {elapsed()}")

print("\n================ FINAL RESULTS ================")
print(f"Base model accuracy      : {base_acc:.2f}%")
print(f"Fine-tuned model accuracy: {ft_acc:.2f}%")
print("================================================")
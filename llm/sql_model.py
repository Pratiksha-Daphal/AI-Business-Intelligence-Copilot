# from transformers import AutoTokenizer, AutoModelForCausalLM
# from peft import PeftModel
# import torch

# BASE_MODEL = "meta-llama/Llama-3-8B-Instruct"
# LORA_PATH = "./lora-nl-sql"

# tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
# base_model = AutoModelForCausalLM.from_pretrained(
#     BASE_MODEL,
#     load_in_8bit=True,
#     device_map="auto"
# )

# model = PeftModel.from_pretrained(base_model, LORA_PATH)
# model.eval()

# def generate_sql(prompt: str) -> str:
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     with torch.no_grad():
#         output = model.generate(
#             **inputs,
#             max_new_tokens=200,
#             temperature=0.1
#         )

#     return tokenizer.decode(output[0], skip_special_tokens=True)




# llm/sql_model.py Cpu stability fixes and lazy loading for faster API startup
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LORA_PATH = "lora-nl-sql"

tokenizer = None
model = None


def load_model():
    global tokenizer, model

    if model is not None:
        return

    print("🧠 Loading SQL generation model...")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32
    )
    base_model.eval()

    model = PeftModel.from_pretrained(base_model, LORA_PATH)
    model.eval()

    print("✅ SQL model loaded")


def generate_sql(query: str, context: dict = None) -> str:
    load_model()   # 🔥 lazy load happens here

    prompt = f"""### Instruction:
Generate a SQL query for the business question using the given schema.

### Question:
{query}

### SQL:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    return decoded.split("### SQL:")[-1].strip()

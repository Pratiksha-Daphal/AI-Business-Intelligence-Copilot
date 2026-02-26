import os
import logging

# ---------------- CPU STABILITY FIXES ----------------
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"

import torch
torch.set_num_threads(2)

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logging.info("🚀 Starting LoRA fine-tuning on CPU")

# ---------------- PATHS & CONSTANTS ----------------
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = "data/nl_sql_train.jsonl"
OUTPUT_DIR = "lora-nl-sql"

# ---------------- LOAD TOKENIZER ----------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# ---------------- LOAD MODEL ----------------
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map=None
)

# ---------------- APPLY LoRA ----------------
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ---------------- LOAD DATASET ----------------
dataset = load_dataset("json", data_files=DATA_PATH)["train"]
logging.info(f"Dataset loaded with {len(dataset)} samples")

# ---------------- TOKENIZATION ----------------
def tokenize_fn(example):
    prompt = f"""### Instruction:
Convert the following question to SQL.

### Question:
{example["input"]}

### SQL:
{example["output"]}
"""
    tokenized = tokenizer(
        prompt,
        truncation=True,
        padding="max_length",
        max_length=192,
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_fn, batched=False)
logging.info("Dataset tokenized successfully")


# ---------------- TRAINING ARGUMENTS ----------------
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    # CPU-safe configuration
    per_device_train_batch_size=1,
    gradient_accumulation_steps=2,
    num_train_epochs=1,
    learning_rate=2e-4,

    # Force logging
    logging_strategy="steps",
    logging_steps=1,
    report_to="none",

    # Disable everything non-essential
    save_strategy="no",
    dataloader_num_workers=0,
    dataloader_pin_memory=False,

    fp16=False,
    bf16=False,
    remove_unused_columns=False
)

# ---------------- TRAINER ----------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# ---------------- TRAIN ----------------
logging.info("🧠 Entering training loop...")
trainer.train()
logging.info("✅ Training completed")

# ---------------- SAVE LoRA ADAPTER ----------------
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

logging.info(f"💾 LoRA adapters saved to: {OUTPUT_DIR}")
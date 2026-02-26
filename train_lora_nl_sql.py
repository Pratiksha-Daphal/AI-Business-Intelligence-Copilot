from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

MODEL_NAME = "meta-llama/Llama-3-8B-Instruct"  # or smaller if needed

# Load dataset
dataset = load_dataset("json", data_files="data/nl_sql_train.jsonl")

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_8bit=True,
    device_map="auto"
)

# LoRA configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, lora_config)

# Prompt formatting
def format_prompt(example):
    prompt = f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    return {"text": prompt}

dataset = dataset.map(format_prompt)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_ds = dataset.map(tokenize, batched=True, remove_columns=dataset["train"].column_names)

# Training args
training_args = TrainingArguments(
    output_dir="./lora-nl-sql",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds["train"]
)

trainer.train()

model.save_pretrained("./lora-nl-sql")
tokenizer.save_pretrained("./lora-nl-sql")

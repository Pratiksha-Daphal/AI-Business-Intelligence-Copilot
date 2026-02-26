from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LORA_PATH = "lora-nl-sql"   # ❗ NO ./ prefix

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

model = PeftModel.from_pretrained(
    base_model,
    LORA_PATH,
    is_trainable=False
)

model.eval()

def generate_sql(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.1
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

def generate_sql(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=150, temperature=0.1)
    return tokenizer.decode(output[0], skip_special_tokens=True)

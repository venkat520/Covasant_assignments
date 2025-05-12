from flask import Flask, request, render_template
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_huggingface import HuggingFacePipeline  # Updated import
import torch

app = Flask(__name__)

# Load model and tokenizer
model_name = "gpt2"  # Change if you're using a different model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Fix pad_token warning
tokenizer.pad_token = tokenizer.eos_token

# Create a text generation pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    pad_token_id=tokenizer.eos_token_id
)

# Create LangChain LLM using the updated pipeline
llm = HuggingFacePipeline(pipeline=generator)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        # Use invoke instead of deprecated __call__
        response = llm.invoke(prompt).strip()
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)

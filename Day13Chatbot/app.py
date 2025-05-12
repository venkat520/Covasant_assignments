from flask import Flask, render_template, request, session
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

app = Flask(__name__)
app.secret_key = 'local-chatbot-secret'


model_name = "tiiuae/falcon-rw-1b"


tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # Safe for CPU
    device_map="cpu"
)


generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95
)


llm = HuggingFacePipeline(pipeline=generator)

@app.route("/", methods=["GET", "POST"])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        user_input = request.form["query"]

        
        prompt = ""
        for item in session['history']:
            prompt += f"User: {item['query']}\nAssistant: {item['response']}\n"
        prompt += f"User: {user_input}\nAssistant:"

        
        response = llm(prompt).strip()

        
        session['history'].append({"query": user_input, "response": response})
        session.modified = True

    return render_template("index.html", history=session['history'])

if __name__ == "__main__":
    app.run(debug=True)

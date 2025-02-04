# app.py
from flask import Flask, render_template, jsonify, request
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pyttsx3  # Optional for TTS

app = Flask(__name__)

# Load local model
MODEL_NAME = "microsoft/DialoGPT-medium"  # Or use "gpt2", "tinyllama-1.1b"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16
)

# Initialize TTS engine (optional)
tts_engine = pyttsx3.init()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    # Generate response
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )
    
    response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    
    # Optional TTS
    tts_engine.say(response)
    tts_engine.runAndWait()
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
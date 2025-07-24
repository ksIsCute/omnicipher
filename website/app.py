
from flask import Flask, render_template, request, jsonify, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ollama', methods=['POST'])
def ollama_api():
    user_input = request.json.get('message')
    context = request.json.get('context', '')
    ollama_url = 'http://localhost:11434/api/generate'
    # Model selection from frontend
    model = request.json.get('model', 'deepseek-r1:8b')
    # Combine context and user input for prompt
    prompt = f"{context}\nUser: {user_input}"
    payload = {
        'model': model,
        'prompt': prompt
    }
    response = requests.post(ollama_url, json=payload, stream=True)
    def generate():
        for line in response.iter_lines():
            if line:
                try:
                    import json
                    obj = json.loads(line.decode('utf-8'))
                    yield obj.get('response', '')
                except Exception:
                    yield line.decode('utf-8')
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

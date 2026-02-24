import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"  # or llama3, qwen:7b

def stream_answer(prompt: str):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.2,
            "num_predict": 120
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                yield data.get("response", "")

    except Exception as e:
        print("OLLAMA ERROR:", str(e))
        return "LLM generation failed."

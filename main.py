import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

def Chat(user_message):
    url = "https://api.together.xyz/v1/chat/completions"
    api_key = "6978af3490849153832a9a68b53c110040d83421fd6244c17718e863eb9ab4ba"
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>", "<|eom_id|>"],
        "stream": False
    }    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "FAILED_TO_RESPONSE: Invalid API response format."
    
    except requests.exceptions.RequestException as e:
        return f"FAILED_TO_RESPONSE: {str(e)}"

@app.get("/")
def read_root():
    return {"response": "Welcome to the LLM-based Chat API"}

@app.get("/chat")
def read_item(q: str):
    res = Chat(q)
    if "FAILED_TO_RESPONSE" in res:
        return {"status": "failure", "response": res}
    else:
        return {"status": "success", "response": res}

handler = Mangum(app)

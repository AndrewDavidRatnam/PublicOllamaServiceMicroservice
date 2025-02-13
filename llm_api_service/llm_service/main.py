from fastapi import FastAPI, HTTPException
from itertools import cycle
import ollama
import logging
from ollama import ChatResponse
from ollama import chat

# response: ChatResponse = chat(model='llama3.2:3b-instruct-q5_K_S', messages=[
#   {
#     'role': 'user',
#     'content': 'Hello my name is user',
#   },
# ])
# print(response['message']['content'])

app = FastAPI()

base_url = "http://localhost:11434"

@app.post("/generate")
async def generate_text(request: dict):
    # Get the next available Ollama instance
    client = ollama.Client(host=base_url)
    logging.info("URL:",base_url)
    try:
        response = client.chat(model="llama3.2:3b-instruct-q5_K_S", messages=[
            {"role":"user",
            "content":request["prompt"] 
            }])
        logging.info("AFter talking to ollama")
        return response
    except Exception as e:
        logging.info("Exception in generate text")
        raise HTTPException(status_code=500, detail=str(e))

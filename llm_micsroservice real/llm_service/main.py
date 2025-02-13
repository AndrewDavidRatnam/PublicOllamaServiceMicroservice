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

# Round-robin load balancing
OLLAMA_INSTANCES = [
    {"base_url": "http://localhost:11436"},
    {"base_url": "http://localhost:11435"},
    {"base_url": "http://localhost:11437"}
]
ollama_cycle = cycle(OLLAMA_INSTANCES)

@app.post("/generate")
async def generate_text(request: dict):
    # Get the next available Ollama instance
    instance = next(ollama_cycle)
    client = ollama.Client(host=instance["base_url"])
    logging.info("URL:",instance["base_url"])
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

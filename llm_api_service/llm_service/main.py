from fastapi import FastAPI, HTTPException
from itertools import cycle
import ollama
import logging
from ollama import ChatResponse
from ollama import chat
import asyncio
from ollama import AsyncClient

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
    async def chat(message1:str):
        message = {'role': 'user', 'content': message1}
        async for part in await AsyncClient().chat(model='llama3.2', messages=[message], stream=True):
            return (part['message']['content'], end='', flush=True)

    client = ollama.Client(host=base_url)
    logging.info("URL:",base_url)
    try:
        async for part in await asyncio.run(chat()):
            return (part['message']['content'], end='', flush=True)
            # response = client.chat(model="llama3.2:3b-instruct-q5_K_S", messages=[
            #     {"role":"user",
            #     "content":request["prompt"] 
            #     }],
            #     stream=True)
            # logging.info("AFter talking to ollama")
    except Exception as e:
        logging.info("Exception in generate text")
        raise HTTPException(status_code=500, detail=str(e))

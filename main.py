import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    response = requests.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [{"role": "user", "content": user_text}],
        },
        timeout=4,
    )

    if response.status_code != 200:
        print("Ошибка API:", response.status_code, response.text)
        return {
            "version": body["version"],
            "session": body["session"],
            "response": {
                "end_session": False,
                "text": "Извините, сервис временно недоступен.",
            },
        }

    data = response.json()

    if "error" in data:
        print("Ошибка OpenRouter:", data["error"])
        answer = "Извините, произошла ошибка при обработке запроса."
    else:
        answer = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Нет ответа")
        )

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {"end_session": False, "text": answer},
    }

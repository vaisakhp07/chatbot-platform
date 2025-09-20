import httpx
from app.core.config import settings

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"

async def call_openai_response(prompt: str, history: list):
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "input": prompt
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(OPENAI_RESPONSES_URL, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        # You may need to adjust parsing depending on API format
        return data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
async def ask_gpt(user_input, language="en"):
    messages = [
        {"role": "system", "content": f"You are a helpful movie expert chatbot. Answer in {language}."},
        {"role": "user", "content": user_input}
    ]
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        return {"success": True, "message": response.choices[0].message.content}
    except Exception as e:
        return {"success": False, "error": str(e)}
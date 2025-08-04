from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend_movie
from chatbot_gpt import ask_gpt
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ควรปรับให้จำกัดเฉพาะ domain ที่ใช้งานจริงใน production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# req (ส่งไปที่ /recommend)
@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    form = await request.form()
    movie = form.get('movie')
    recs = recommend_movie(movie)
    return templates.TemplateResponse("home.html", {"request": request, "recommendations": recs})

# API chat (จาก JavaScript)
@app.post("/chat")
async def chat_with_bot(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    language = data.get("language", "en")
    result = await ask_gpt(user_input, language)  # await
    # ถ้า sync ใช้แบบนี้:
    # result = ask_gpt(user_input, language)  # sync
    # เวอร์ชันใหม่ ควรเป็น async 

    if result["success"]:
        reply_text = result["message"]
    else:
        reply_text = f"Error: {result['error']}"

    recommendations = recommend_movie(user_input)
    return JSONResponse(content={"reply": reply_text, "recommendations": recommendations})


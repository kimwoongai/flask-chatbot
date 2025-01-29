from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# ✅ OpenAI API 키 설정
import os

API_KEY = os.getenv("OPENAI_API_KEY")
client=openai.OpenAI(api_key=API_KEY)

# ✅ GPT API를 호출하는 함수
def process_input(user_input):
    """GPT API를 호출하여 응답을 반환"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT 응답에 실패했습니다: {e}"

# ✅ API 엔드포인트 설정
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json  # JSON 데이터를 받아오기
    user_message = data.get("message", "")

    if user_message.lower().startswith("질문"):
        reply = process_input(user_message[3:].strip())  # GPT API 호출
    else:
        reply = "질문을 입력하거나 적절한 데이터를 입력하세요."

    return jsonify({"reply": reply})

# ✅ 서버 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)

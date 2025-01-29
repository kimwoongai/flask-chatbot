import openai
import os
import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/prompt', methods=['POST'])
def generate_answer():
    try:
        prompt = request.json.get('prompt', '')  # KeyError 방지
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400  # 요청에 'prompt'가 없을 경우

        openai.api_key = os.getenv("API_KEY")  # 환경 변수에서 API 키 가져오기
        if not openai.api_key:
            return jsonify({"error": "API key is missing"}), 500  # API 키 없을 때

        # ✅ 최신 openai 라이브러리 사용 방식으로 변경
        client = openai.OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )

        answer = response.choices[0].message.content.strip()

        # 한글 깨짐 방지를 위해 Response + json.dumps() 사용
        return Response(
            json.dumps({'answer': answer}, ensure_ascii=False), 
            content_type="application/json; charset=utf-8"
        )

    except openai.AuthenticationError:
        return jsonify({"error": "Invalid API key"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Flask 오류 디버깅 용도

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)  # debug=True로 변경해서 오류 메시지 확인


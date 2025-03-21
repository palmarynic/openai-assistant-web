import os
from flask import Flask, request, jsonify, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# 設定 OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

@app.route('/api/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()

        if not user_question:
            return jsonify({"error": "請輸入問題"}), 400

        # 建立對話 Thread
        thread = openai.beta.threads.create()
        thread_id = thread.id

        # 發送問題
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_question
        )

        # 執行 Assistant
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # 取得 AI 回應
        messages = openai.beta.threads.messages.list(thread_id=thread_id)

        response_text = "抱歉，我找不到相關答案。"
        if messages.data:
            first_message = messages.data[0]
            text_blocks = []
            if hasattr(first_message, 'content') and isinstance(first_message.content, list):
                for block in first_message.content:
                    if hasattr(block, 'text') and hasattr(block.text, 'value'):
                        text_blocks.append(block.text.value.strip())

            if text_blocks:
                response_text = "\n".join(text_blocks)

        return jsonify({"answer": response_text})

    except Exception as e:
        print(f"伺服器錯誤: {str(e)}")
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500
    
    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')

# **讓 Flask 綁定正確 Port**
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

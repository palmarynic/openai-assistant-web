from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)
CORS(app)

# 設定 OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

@app.route('/')
def index():
    #return render_template('index.html')
    return jsonify({"message": "Flask API is running. Use /ask to communicate with OpenAI Assistant."})

@app.route('/ask', methods=['POST'])
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

            # **解析 `content`，提取 `text.value`**
            if hasattr(first_message, 'content') and isinstance(first_message.content, list):
                for block in first_message.content:
                    if hasattr(block, 'text') and hasattr(block.text, 'value'):
                        text_blocks.append(block.text.value.strip())  # ✅ 取得 `text.value`

            if text_blocks:
                response_text = "\n".join(text_blocks)

        return jsonify({"answer": response_text})

    except Exception as e:
        print(f"伺服器錯誤: {str(e)}")  # ✅ **讓錯誤訊息出現在終端機**
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

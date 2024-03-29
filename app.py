from flask import Flask,request
from gpt_auto_finetuning import chat_service
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def hello():
    message = request.json.get('message', '')
    response_message = chat_service(message)
    return response_message

if __name__ == '__main__':
    app.run(debug=True)
# 챗봇은 gpt_auto_finetuning.py 에서 마지막 부분인

# completion = client.chat.completions.create(
#     model = "finetuned model",
#     messages = [
#         {"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"},
#         {"role": "user", "content": "오파테크란?"}
#     ]
# )

# print(completion.choices[0].message)

# 이 코드에서 사용자가 입력한 질문은 "오파테크란?" 이 자리에 넣어주시면 되고 그에 따른 챗봇의 답변은 completion.choices[0].message 이걸로 반환됩니다!
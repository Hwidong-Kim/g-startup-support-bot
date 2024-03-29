from flask import Flask,request, render_template
from flask_restx import Api, Resource, reqparse,fields
#from gpt_auto_finetuning import chat_service

app = Flask(__name__)

# Swagger를 위한 설정
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

test_api = api.namespace('', description='CHAT API')
chat_parser = reqparse.RequestParser()
chat_parser.add_argument('message', type=str, required=True, help='메시지 필드가 필요합니다.')
chat_model = api.model('Chat Model', {
    'message': fields.String(required=True, description='채팅 메시지')
})
@test_api.route("/chat", methods=["POST"])
class Chat(Resource):
    @test_api.expect(chat_model, validate=True)  # 요청 모델 적용
    def post(self):
        args = chat_parser.parse_args()
        message = args['message']

        #response_message = chat_service(message)
        return {'response_message': "response_message"}, 200

# Swagger 문서 라우트 등록

if __name__ == '__main__':
    app.run(debug=True)

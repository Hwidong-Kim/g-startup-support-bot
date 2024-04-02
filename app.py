from flask import Flask,request, render_template
from flask_restx import Api, Resource, reqparse,fields
from kChatBot import kChatBot
#from flask_cors import CORS, cross_origin
import ssl
import json


# Loading cert
#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#ssl_context.load_cert_chain(certfile='C:/nginx-1.25.3/conf/certificate.crt', keyfile='C:/nginx-1.25.3/conf/private.key')
    

all_path = "./all_data.jsonl"
update_path = "./update_data.jsonl"

chatbot = kChatBot()
OPENAI_API_KEY = "keyyy"
chatbot.initialize_openai(OPENAI_API_KEY)
#chatbot.initialize_finetuning_data("./data/data.json")
#chatbot.set_save_path(all_path)
#chatbot.set_save_path(update_path)
#chatbot.auto_text_to_finetuning_data()

with jsonlines.open(all_path, 'r') as all_file:
        with jsonlines.open(update_path, 'w') as update_file:
            for item in all_file:
                update_file.write(item)
           
for _ in range(2):
    auto_text_to_finetuning_data(raw_data, update_path)
    
#chatbot.finetune_model()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app)


@app.route('/chat', methods=['POST'])
#@cross_origin()
def chat():
    ret = {}
    global chatbot
    try:
        ret['msg'] = chatbot.chat_service(str(request.form['msg']))
    except:
        ret['msg'] = 'shut up and dance'
    return json.dumps(ret, ensure_ascii=False)
    

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=443, threaded=True, debug=False, ssl_context=ssl_context)
    app.run(host='0.0.0.0', port=80, threaded=True, debug=False)

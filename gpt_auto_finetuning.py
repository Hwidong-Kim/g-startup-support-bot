
import json
import os
import time
import re

from openai import OpenAI
from pathlib import Path
def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

save_path = "./auto_data.jsonl"

raw_data = load_from_json("./data/data.json")

#print(len(raw_data))

def createJson_chat(conversation, file_path):
    data = {"messages": []}
    for question, answer in conversation:
        data["messages"].append({"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"})
        data["messages"].append({"role": "user", "content": question})
        data["messages"].append({"role": "assistant", "content": answer})

    with open(file_path, "a", encoding="utf-8") as jsonl_file:
        jsonl_file.write(json.dumps(data, ensure_ascii=False) + "\n")


def auto_text_to_finetuning_data(text, save_path):

    keywords = []
    contents = []
    for i in range(len(raw_data)):
        for j in range(len(raw_data[i]["contents"])):
            
            text = raw_data[i]["contents"][j]

            match = re.search(r'<(.*?)>', text)

            if match:
                keyword = re.findall(r'<(.*?)>', text)[0]

                first_index = text.find(keyword)
                second_index = text.find("\n", first_index + 1)

                content = text[second_index+1:]

                if keyword not in keywords:
                    keywords.append(keyword)
                    contents.append(content)


    if len(keywords) != len(contents):
        print("data extractoin failed")
        
    for i in range(len(keywords)):

        keyword, content = keywords[i], contents[i]

        last_char = keyword[-1]  
        jongsung = (ord(last_char) - 0xAC00) % 28  

        if jongsung == 0: 
            keyword_aug_list = [
                keyword,
                keyword + "가 뭐야?",
                keyword + "에 대해 설명해줘",
                keyword + "란?"
            ]
        else:  
            keyword_aug_list = [
                keyword,
                keyword + "이 뭐야?",
                keyword + "에 대해 설명해줘",
                keyword + "이란?"
            ]

        for keyword_aug in keyword_aug_list:
            createJson_chat([(keyword_aug, content)], save_path)
            
            

auto_text_to_finetuning_data(raw_data, save_path)

OPENAI_API_KEY = "put API KEY"
client = OpenAI(
    api_key= OPENAI_API_KEY
)



train_file = client.files.create(
    file=Path(save_path),
    purpose="fine-tune",
)



client.fine_tuning.jobs.create(
    training_file=train_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={
    "n_epochs":13
  }
)
def chat_service(content):
    completion = client.chat.completions.create(
        model = "finetuned model",
        messages = [
            {"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"},
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message

#input   {"role": "user", "content": "오파테크란?"}
# completion = client.chat.completions.create(
#     model = "finetuned model",
#     messages = [
#         {"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"},
#         {"role": "user", "content": "오파테크란?"}
#     ]
# )
#input   {"role": "user", "content": "오파테크란?"}
# completion = client.chat.completions.create(
#     model = "finetuned model",
#     messages = [
#         {"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"},
#         {"role": "user", "content": "오파테크란?"}
#     ]
# )
#
# output rs
#print(completion.choices[0].message)
#print(completion.choices[0].message)

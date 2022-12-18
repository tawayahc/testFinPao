from flask import Flask, render_template, request, send_from_directory
import os
import re
import requests

app = Flask(__name__)
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/CH0KUN/GPT2-base-Thai-Fiction"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def clean_text(text): return re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,…]", "", text)
def isContainSPC(string):
    regex = re.compile(r'[a-zA-Z]')
    if(regex.search(string) == None):
        return False
    else:
        return True

def filter(LST):
    result = []
    for gentext in LST:
        customRudeword = [
                          "เหี้ย","เงื่ยน","ควย","หี","เย็ด","โป๊","ควE",
                          "กระโปรง","กางเกงใน","เซ็ก","หำ","จิ๋ม","ว่าว",
                          "เสี่ยว","แฉะ","พนัน","งวดที่","ฉบับที่"
                          ]
        if not isContainSPC(gentext):
        #   gentext = gentext[:gentext.rfind(" ")]
            if any(rudeWord in gentext for rudeWord in  customRudeword):
                continue
            result.append(clean_text(gentext).replace("\n", ""))
    return result

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/image'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/finPao', methods=['POST'])
def finPao():
    return render_template('finPao.html')

@app.route('/finPaoResult', methods=['POST'])
def finPaoResult():
    INPUT_TEMPERATURE = request.form.get("INPUT_TEMPERATURE")
    GEN_NUM = int(request.form.get("GEN_NUM"))
    MAX_TOKEN = int(request.form.get("MAX_TOKEN"))
    text_input = request.form.get("text_input")

    
    result = query({
        "inputs": text_input,
        "parameters":{
            "temperature":INPUT_TEMPERATURE,
            "num_return_sequences":GEN_NUM,
            "max_new_tokens":MAX_TOKEN,
        },
        "options":{
            "use_cache":False,
            "wait_for_model":True,
        }   
    })

    result = [Dict['generated_text'] for Dict in result]
    result = filter(result)

    return render_template('finPaoResult.html', result=result, text_input=text_input)

if __name__ == '__main__':
    app.run(debug = True)
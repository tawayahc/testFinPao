from flask import Flask, render_template, request, send_from_directory
import os
import re
import requests

app = Flask(__name__)
API_TOKEN = "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"
APIKEY_ = "IjeNNsjc09MngydXCBsO9BpP6n7vOjTI"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload,API_URL):
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
                          "เสี่ยว","แฉะ","พนัน","งวดที่","ฉบับที่","หน้าแรก","นม","หน้าอก"
                          ]
        if not isContainSPC(gentext):
        #   gentext = gentext[:gentext.rfind(" ")]
            if any(rudeWord in gentext for rudeWord in  customRudeword):
                continue
            result.append(clean_text(gentext).replace("\n", ""))
    return result

def get_vaja_bytes(text):
  url = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
  headers = {'Apikey':APIKEY_ ,'Content-Type' : 'application/json'}
  data = {'input_text':text,'speaker': 0, 'phrase_break':0, 'audiovisual':0}
  response = requests.post(url, json=data, headers=headers)
  sWav_url = response.json()['wav_url']
  audio_response = requests.get(sWav_url,headers={'Apikey':APIKEY_ })
  if audio_response.status_code:
    return audio_response.content 
  else:
    return False 

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
    API_URL = "https://api-inference.huggingface.co/models/CH0KUN/GPT2-base-Thai-Fiction"
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
    }, API_URL)

    result = [Dict['generated_text'] for Dict in result]
    result = filter(result)

    if len(result):
        bytes_array = list(get_vaja_bytes(result[0]))
    else:
        bytes_array = []
    if len(bytes_array) > 200:
     bytes_status = "✅Ready"
    else:
     bytes_status = "⚠️Not Ready"

    return render_template('finPaoResult.html', result=result, text_input=text_input, bytes_array = bytes_array, bytes_status = bytes_status,
                            INPUT_TEMPERATURE=INPUT_TEMPERATURE, GEN_NUM=GEN_NUM, MAX_TOKEN=MAX_TOKEN)

@app.route('/siaoPao', methods=['POST'])
def siaoPao():
    return render_template('siaoPao.html')

@app.route('/siaoPaoResult', methods=['POST'])
def siaoPaoResult():
    API_URL = "https://api-inference.huggingface.co/models/CH0KUN/gpt2-base-thai-siaojoke"
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
    }, API_URL)

    result = [Dict['generated_text'] for Dict in result]
    result = filter(result)

   
    if len(result):
        bytes_array = list(get_vaja_bytes(result[0]))
    else:
        bytes_array = []
    if len(bytes_array) > 200:
     bytes_status = "✅Ready"
    else:
     bytes_status = "⚠️Not Ready"
    
    return render_template('siaoPaoResult.html', result=result, text_input=text_input, bytes_array = bytes_array, bytes_status = bytes_status,
                            INPUT_TEMPERATURE=INPUT_TEMPERATURE, GEN_NUM=GEN_NUM, MAX_TOKEN=MAX_TOKEN)

@app.route('/khumPao', methods=['POST'])
def khumPao():
    return render_template('khumPao.html')

@app.route('/khumPaoResult', methods=['POST'])
def khumPaoResult():
    API_URL = "https://api-inference.huggingface.co/models/CH0KUN/gpt2-base-thai-typical-joke"
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
    }, API_URL)

    result = [Dict['generated_text'] for Dict in result]
    result = filter(result)

   
    if len(result):
        bytes_array = list(get_vaja_bytes(result[0]))
    else:
        bytes_array = []
    if len(bytes_array) > 200:
     bytes_status = "✅Ready"
    else:
     bytes_status = "⚠️Not Ready"

    return render_template('khumPaoResult.html', result=result, text_input=text_input,bytes_array=bytes_array, bytes_status=bytes_status,
                            INPUT_TEMPERATURE=INPUT_TEMPERATURE, GEN_NUM=GEN_NUM, MAX_TOKEN=MAX_TOKEN)

if __name__ == '__main__':
    app.run(debug = False)
import openai
import json as js
import datetime
import re
#--------------initial----------------#
API_PATH = "./API-key.json"
#------------------------------#
LOGS_PATH = './logs/'
#------------------------------#
MODEL = "gpt-3.5-turbo"
MESSAGES = [
    {"role":"system",
     "content":""}
    ]
#--------------initial----------------#
#json.dump(data, f, indent=4, ensure_ascii=False)
def sendingMessages(MODEL,MESSAGES):
    response = openai.ChatCompletion.create(model=MODEL,messages=MESSAGES)
    response_role = response.choices[0].message.role
    response_result = ''
    for choice in response.choices:
        response_result += choice.message.content
    return response_role,response_result


with open(API_PATH, "r", encoding="utf-8") as key_file:
    
    openai.api_key = js.load(key_file)["key1"]
    #print("openai.api_key:"+str(openai.api_key))
    #------------------------------#
    logs_file = LOGS_PATH + re.sub(r'[^a-zA-Z0-9]', '', str(datetime.datetime.now())) + ".json"
    #print("logs_file:"+str(logs_file))
    #------------------------------#
    
    with open(logs_file, "w", encoding="utf-8") as logs:
        #--------------initialize----------------#
        sys_content = input("define system:")
        if sys_content == "":
            sys_content =  "现在你是一个机器人顾问。"
        MESSAGES[0]["content"] = sys_content
        
        user_content = input("user content:")
        if user_content == "":
            user_content =  "你觉得是先有鸡还是先有蛋。"
        tmp_content = {"role":"user","content":user_content}
        MESSAGES.append(tmp_content)
        
        response_role,response_result = sendingMessages(MODEL,MESSAGES)
        print("response_result:\t\t"+str(response_result))
        response_json = {"role":response_role,
                    "content":response_result}
        #print("tmp_json:"+str(response_json))
        MESSAGES.append(response_json)
        #--------------initialize----------------#
        content = input("user content:")
        
        while content!="new chat 2887":#exit with "new chat 2887"
            if content[0:6] == "system":
                role = "system"
            else:
                role = "user"
            user_message = {"role":role,"content":content}
            MESSAGES.append(user_message)
            #print("MESSAGES:"+str(MESSAGES))
            #------------------------------#
            #response = openai.ChatCompletion.create(model=MODEL,messages=MESSAGES)
            #print("response:"+str(response))
            #------------------------------#
            response_role,response_result = sendingMessages(MODEL,MESSAGES)
            
            print("response_result:\t\t"+str(response_result))
            #------------------------------#
            response_json = {"role":response_role,
                        "content":response_result}
            #print("tmp_json:"+str(response_json))
            MESSAGES.append(response_json)
            #------------------------------#
            content = input("user content:")
            
        else:
            print("---------BIGBANG----------")
        js.dump(MESSAGES, logs, indent=4, ensure_ascii=False)
        

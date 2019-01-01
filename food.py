import json
import uuid

def addFood(request):
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)
    request["uuid"] = str(uuid.uuid4())
    data.append(request)
    for i in range(len(data)):
        data[i]["id"] = i
    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
    return {"result":"add food success"}

def updateFood(request):
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)
    for i in range(len(data)):
        if data[i]["uuid"] == request["uuid"]:
            request["id"] = data[i]["id"]
            data[i] = request
    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)      
    return {"result":"update food success"}
    
def removeFood(request):
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)
    index = -1
    for i in range(len(data)):
        if data[i]["uuid"] == request["uuid"]:
            index = i
    if index != -1:
        del data[index]
    for i in range(len(data)):
        data[i]["id"] = i
    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
    return {"result":"remove food success"}

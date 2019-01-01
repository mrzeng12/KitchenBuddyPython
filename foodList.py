import json
def getFoodList(request):
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)
    if len(request) is 0: 
        return data
    result = [data[i] for i in range(len(data)) if data[i]["uuid"] in request]
    return result
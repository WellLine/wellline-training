import requests, uuid, json

def translate_event(config, event):
  print("Translating event - id:{}".format(event["id"]))

  newEvent = event

  params = '&from=' + config["source_lang_id"] + '&to=' + config["target_lang_id"]
  constructed_url = config["url"] + config["path"] + params

  headers = {
      'Ocp-Apim-Subscription-Key': config["subscription_key"],
      'Content-type': 'application/json',
      'X-ClientTraceId': str(uuid.uuid4())
  }

  # You can pass more than one object in body.
  body = [{
    "text" : event["content"]
  }]

  request = requests.post(constructed_url, headers=headers, json=body)
  response = request.json()

  # print(response[0]['translations'][0]['text'])
  print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
        
  return newEvent
    

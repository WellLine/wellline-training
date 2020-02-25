import os, json, requests, datetime
import azure.functions as func
from .event_translator import event_translator
from .timeline_svc import timeline_svc

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

# JWT to authenticate against timeline service
env_auth_token = os.getenv('TIMELINE_AUTH_TOKEN', '')

# Configuration of notification subscriber
notification_config = {
  'tenant_ids': ["shell", "allen"],
  'notification_types': ["created", "updated", "deleted"]
}

# Configuration to access source events
src_timeline_svc_config = {
  'url': "https://dev-timeline.wellline.com/graphql",
  'auth_token': env_auth_token
}

# Configuration to publish translated events 
dest_timeline_svc_config = {
  "url": "https://dev-timeline.wellline.com/graphql",
  "auth_token": env_auth_token
}
dest_tenant_id = "asea" 

# Configuration for translation service 
# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
translator_config = {
  "subscription_key": "028b6721f9f84263ac6f0a2ac70ef617",
  "url": "https://api.cognitive.microsofttranslator.com",
  "path": '/translate?api-version=3.0',
  "source_lang_id": 'en',
  "target_lang_id": 'es'
}

def parseEventGridEvent(event):
  
  notification = {}

  event_type_parts = event.event_type.split(".")
  notification["element_type"] = event_type_parts[0]
  notification["notification_type"] = event_type_parts[1]

  subject_parts = event.subject.split("/")
  notification["tenant_id"] = subject_parts[1]
  notification["element_id"] = subject_parts[3]

  return notification

def main(eventGridEvent: func.EventGridEvent):

  notification = parseEventGridEvent(eventGridEvent)
  print("Notification: {}".format(notification))

  # Ensure tenant is valid and the notification is an add/update event notification
  if (notification["tenant_id"] in notification_config["tenant_ids"]) and (notification["element_type"] == "Event") and (notification["notification_type"] in notification_config["notification_types"]):    
    print("Processing Event notification - tenant_id:{}, notification_type:{}, id:{}".format(notification["tenant_id"], notification["notification_type"], notification["element_id"]))

    event = timeline_svc.getEvent(src_timeline_svc_config, notification["tenant_id"], notification["element_id"])
    print("Event: {}".format(event))

    if event:
      # updateEvent = False
      # addEvent = False

      # eventAdd = []

      # eventUpdate = { "id": element_id, "addQuantities": [], "addMeasures": [], "addProperties": [], "addReferences": [], 
      # "deleteQuantities": [], "deleteMeasures": [], "deleteProperties": [], "deleteReferences": [] }

      # Translate Event
      new_event = event_translator.translate_event(translator_config, event)

      # if new_event:
      #   addEvents(tenant_id, [new_event])

    else:
      # TODO: Log error
      print("Unable to read Event - tenant_id:{}, id:{}".format(notification["tenant_id"], notification["element_id"]))

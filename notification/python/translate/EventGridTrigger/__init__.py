import os
import json
import logging
import requests
import datetime
import azure.functions as func
from .event_translator import event_translator

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

acceptTenantIds = ["allen", "arul"]
acceptNotificationTypes = ["created", "updated"]
timeline_svc_url = "http://dev-timeline.wellline.com/graphql"
env_auth_token = os.getenv('TIMELINE_AUTH_TOKEN', '')

# Translation Config
translatorConfig = {}

# GraphQL Queries and Mutations
getEventQuery = """
    query($tenantId: ID!, $id: ID!) {
      event(tenantId: $tenantId, id: $id) 
      { id, content, links { uri, description, typeId }, properties { name, value}, quantities {unit, value}, measures { type { id, name, units }, value}, subjectEntityIds, referenceEntityIds }
    }
  """

updateEventsMutation = """
    mutation($tenantId: ID!, $batchId: ID, $input: [UpdateEventInput!]!, $eepConfig: EepConfigInput, $async: Boolean) {
      updateEvents(tenantId: $tenantId, batchId: $batchId, input: $input, eepConfig: $eepConfig, async: $async)
      { batchId, actionCount, validationErrorCount, indexErrorCount, submitted, duration, isAsync, actionResults { status, result, id, errors { type, reason } } }
    }
  """

addEventsMutation = """
    mutation($tenantId: ID!, $batchId: ID, $input: [AddEventInput!]!, $eepConfig: EepConfigInput) {
      addEvents(tenantId: $tenantId, batchId: $batchId, input: $input, eepConfig: $eepConfig)
      { batchId, actionCount, duration, actionResults { status, result, id, errors { type, reason } } }
    }
  """

def getEvent(tenantId, eventId):
  headers = {"Authorization": "Bearer {}".format(env_auth_token)}
  variables = {"tenantId": tenantId, "id": eventId}

  # print(variables)

  response = requests.post(timeline_svc_url, json={'query': getEventQuery, 'variables': variables}, headers=headers)

  if response.status_code == 200:
    return response.json()["data"]["event"]
  else:
    print(bcolors.FAIL + "TimeLine Service call failed with code: {}".format(response.status_code) + bcolors.ENDC)
    print(bcolors.BOLD + "Query:" + bcolors.ENDC)
    print(getEventQuery)
    try:
      print(bcolors.BOLD + "GraphQL Errors ({}):".format(len(response.json()["errors"])) + bcolors.ENDC)
      print(*response.json()["errors"], sep="\n")
    except:
      print(bcolors.BOLD + "Errors:" + bcolors.ENDC)
      print(response.text)
    exit()

def updateEvents(tenantId, eventUpdates):

  headers = {"Authorization": "Bearer {}".format(env_auth_token)}
  variables = {"tenantId": tenantId, "input": eventUpdates}
  # print(variables)

  response = requests.post(timeline_svc_url, json={'query': updateEventsMutation, 'variables': variables}, headers=headers)
  # print (response.text)

  if response.status_code == 200:
    return response.json()['data']
  else:
    print(bcolors.FAIL + "TimeLine Service call failed with code: {}".format(response.status_code) + bcolors.ENDC)
    print(bcolors.BOLD + "Query:" + bcolors.ENDC)
    print(getEventQuery)
    try:
      print(bcolors.BOLD + "GraphQL Errors ({}):".format(len(response.json()["errors"])) + bcolors.ENDC)
      print(*response.json()["errors"], sep="\n")
    except:
      print(bcolors.BOLD + "Errors:" + bcolors.ENDC)
      print(response.text)
    exit()

def addEvents(tenantId, eventsAdd):
  headers = {"Authorization": "Bearer {}".format(env_auth_token)}

  variables = {"tenantId": tenantId, "input": eventsAdd}

  print ("*******************")
  print(variables)
  print ("*******************")
  response = requests.post(timeline_svc_url, json={'query': addEventsMutation, 'variables': variables}, headers=headers)

  # print (response.text)

  if response.status_code == 200:
    print (response.text)
    return response.json()['data']
  else:
    print(bcolors.FAIL + "TimeLine Service call failed with code: {}".format(response.status_code) + bcolors.ENDC)
    print(bcolors.BOLD + "Query:" + bcolors.ENDC)
    print(getEventQuery)
    try:
      print(bcolors.BOLD + "GraphQL Errors ({}):".format(len(response.json()["errors"])) + bcolors.ENDC)
      print(*response.json()["errors"], sep="\n")
    except:
      print(bcolors.BOLD + "Errors:" + bcolors.ENDC)
      print(response.text)
    exit()


def main(notification: func.EventGridEvent):

  notificationTypeParts = notification.event_type.split(".")
  # print("******* notificationTypeParts: {}".format(notificationTypeParts))
  elementType = notificationTypeParts[0]
  # print("elementType: {}".format(elementType))
  notificationType = notificationTypeParts[1]
  # print("notificationType: {}".format(notificationType))

  subjectParts = notification.subject.split("/")
  # print("******* subjectParts: {}".format(subjectParts))
  tenantId = subjectParts[1]
  # print("tenantId: {}".format(tenantId))
  elementId = subjectParts[3]
  # print("eventId: {}".format(elementId))

  # Ensure tenant is valid and the notification is an add/update event notification
  if (tenantId in acceptTenantIds) and  (elementType == "Event") and notificationType in acceptNotificationTypes:    
    print("Processing Event notification - tenantId:{}, notificationType:{}, id:{}".format(tenantId, notificationType, elementId))

    event = getEvent(tenantId, elementId)
    print("event: {}".format(event))
    # print("event.id: {}".format(event['id']))
    # print("event.content: {}".format(event['content']))
    # print("event.links: {}".format(event['links']))

    if event:
      updateEvent = False
      addEvent = False

      # eventAdd = []

      eventUpdate = { "id": elementId, "addQuantities": [], "addMeasures": [], "addProperties": [], "addReferences": [], 
      "deleteQuantities": [], "deleteMeasures": [], "deleteProperties": [], "deleteReferences": [] }

      # Translate Event
      new_event = event_translator(translatorConfig, event)

      if new_event:
        addEvents(tenantId, [newEvent])

    else:
      # TODO: Log error
      print("Unable to read Event - tenantId:{}, id:{}".format(tenantId, elementId))

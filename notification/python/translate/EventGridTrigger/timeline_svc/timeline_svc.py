import os
import json
import requests

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

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

def getEvent(svc_config, tenantId, eventId):
  headers = {"Authorization": "Bearer {}".format(svc_config["auth_token"])}
  variables = {"tenantId": tenantId, "id": eventId}

  # print(variables)

  response = requests.post(svc_config["url"], json={'query': getEventQuery, 'variables': variables}, headers=headers)

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

def updateEvents(svc_config, tenantId, eventUpdates):

  headers = {"Authorization": "Bearer {}".format(svc_config["auth_token"])}
  variables = {"tenantId": tenantId, "input": eventUpdates}
  # print(variables)

  response = requests.post(svc_config["url"], json={'query': updateEventsMutation, 'variables': variables}, headers=headers)
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

def addEvents(svc_config, tenantId, eventsAdd):
  headers = {"Authorization": "Bearer {}".format(svc_config["auth_token"])}

  variables = {"tenantId": tenantId, "input": eventsAdd}

  print ("*******************")
  print(variables)
  print ("*******************")
  response = requests.post(svc_config["url"], json={'query': addEventsMutation, 'variables': variables}, headers=headers)

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


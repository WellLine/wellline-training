import getpass 
import requests # pip install requests

# TODO: Remove staging defaults once cloud supports this authentication
# Default Values for authenticating against WellLine public cloud
def_tenant_id = "76648a49-7e8a-4b11-9aed-e3852b2f4295"
# def_client_id = "738df55d-a717-443f-9817-bf915be34c8c"
# def_wellline_url = "https://cloud.wellline.com"
def_client_id = "6617ddfd-68f6-4452-8259-e906147e0c25"
def_wellline_url = "https://staging.wellline.com"

# Templates for the Authentication request
headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "cache-control": "no-cache"}
urlTemplate = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
bodyTemplate = "grant_type=password&client_id={}&scope={}/user_impersonation&username={}&password={}"

# Get user input or use defualt values
print("\nEnter parameters for WellLine Authentication:")
tenant_id = input("Tenant Id [{}]: ".format(def_tenant_id))
tenant_id = tenant_id or def_tenant_id

client_id = input("Client Id [{}]: ".format(def_client_id))
client_id = client_id or def_client_id

wellline_url = input("WellLine URL [{}]: ".format(def_wellline_url))
wellline_url = wellline_url or def_wellline_url

user_id = input("User Id: ") 
password = getpass.getpass() 

# Construct the Authentication request
url = urlTemplate.format(tenant_id)
body = bodyTemplate.format(client_id, wellline_url, user_id, password)

# Issue the Authenticaiton request and get the reesponse
response = requests.post(url, data=body, headers=headers)

# Display the Authentication Token
if (response.status_code == 200):
    print("\nAccess Token:")
    print(response.json()["access_token"])
else:
    print("\nError: {}".format(response.status_code))
    print(response.json())


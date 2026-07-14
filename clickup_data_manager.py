# Wangchuk added, 08-07-2026

# API key note: 
# The "Authorization" key or the API key is generated from Factory's clickup account. 
# Anyone who has access to Cabtek Clickup can generate the key from their account and update it here.
import copy
import json
import requests

#CLICKUP APP DETAILS ----------------------------------------------------------------------------------------------------------------------------#

# API_KEY = "pk_88871404_IHEVPKK04HER89DOEKW29KQGNMGHQAIC"    # For Testing, generated from Jesse's account
# API_KEY = 'pk_88879098_D11LHGTDFN87IUU864BM4Z7QH8V39IQ5'    # For Testing, generated from Wangchuk's account

API_KEY = "pk_88895266_ER73ZDCGD3DBZ6C5N1ELL7SOYFGH8JDW"    # For Release, generated from factory clickup account (email id : cabtek87@gmail.com : , password: pDmh1wtw?xr )
TEAM_ID_CABTEK = "9003205324"
HEADERS = { "Content-Type": "application/json", "Authorization": API_KEY }
QUERY  = { "custom_task_ids": "true", "team_id": TEAM_ID_CABTEK }

# Space
SPACE_ID_CONTACTS               = "90160459168"   

# List
LIST_ID_CONTACTS_SALES          = '901601318067'

# Custom Field 
CUSTOM_FIELD_ID_CLIENT_CATEGORY = "d18634da-38e1-42f1-a808-5352bd110d40"

CUSTOM_FIELD_ID_CONTACT_NAME = "c846b599-4dd8-470d-b13b-d1a1ec6fce92" 
CUSTOM_FIELD_ID_COMPANY = "7144789a-4090-4091-a7e8-ded6ed74ddfe" 
CUSTOM_FIELD_ID_EMAIL_T = "054776b3-4d70-4cd1-a51c-9fb3245bb260" 
CUSTOM_FIELD_ID_PHONE = "25681e1a-571d-4fa2-ae2a-f5687de83aef"

# Custom Field Option
CLIENT_CATEGORY_OPTION_ID_TRADE         = "faed4cd8-5bd3-4204-ba82-61f02a17984a"
CLIENT_CATEGORY_OPTION_ID_PUBLIC        = "1a309086-1c84-4438-a914-9673f15a7342"

#----------------------------------------------------------------------------------------------------------------------------#

def get_filtered_tasks_from_clickup(list_id, query={}):
    all_tasks = []
    
    try:
        url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"
        api_query = copy.deepcopy(query)
        current_page = 0

        while True:
            api_query["page"] = current_page
            response = requests.get(url, headers = HEADERS, params = api_query)

            if response.status_code == 200:
                data = response.json()
                page_tasks = data['tasks']

                # Exit if no tasks found on the current page.
                if not page_tasks:
                    break

                # Add tasks to all_tasks
                all_tasks.extend(page_tasks)

                # Move to next page
                current_page += 1
            else:
                print(f"API Error {response.status_code}: {response.text}")
                break

        return all_tasks

    except Exception as ex:
        print(ex)
        return []


def get_clickup_trade_contacts():
    trade_contacts = []
    try:
        query = {
            "custom_fields":  json.dumps([ 
                                            {
                                                "field_id":CUSTOM_FIELD_ID_CLIENT_CATEGORY, 
                                                "operator":"ANY", 
                                                "value":[CLIENT_CATEGORY_OPTION_ID_TRADE]
                                            } 
                                        ]) 
        }

        tasks =  get_filtered_tasks_from_clickup(LIST_ID_CONTACTS_SALES, query)

        if tasks:
            for task in tasks:
                task_info = {
                    "id":task['id'],
                    "name":"",
                    "company":"",
                    "email":"",
                    "phone":""
                }

                for field in task['custom_fields']:
                    if field['id'] == CUSTOM_FIELD_ID_CONTACT_NAME and "value" in field:
                        task_info['name'] = str(field['value']).strip() 

                    elif field['id'] == CUSTOM_FIELD_ID_COMPANY and "value" in field:
                        task_info['company'] = str(field['value']).strip() 

                    elif field['id'] == CUSTOM_FIELD_ID_EMAIL_T and "value" in field:
                        task_info['email'] = str(field['value']).strip() 

                    elif field['id'] == CUSTOM_FIELD_ID_PHONE and "value" in field:
                        task_info['phone'] = str(field['value']).strip()

                trade_contacts.append(task_info)

        return trade_contacts
      
    except Exception as ex:
        print(ex)
        return []






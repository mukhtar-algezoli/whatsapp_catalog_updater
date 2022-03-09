from re import X
from pymongo import MongoClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bson.objectid import ObjectId
import requests
import re
from datetime import datetime


client = MongoClient("mongodb+srv://enigma:A_pass2mongo@sme-platform.pkbgh.mongodb.net")

whatsapp_users = client.backend.users.find({ "whatsapp_update_file" : { "$exists" : True } })


def get_khodorgy_categories(lang):
    endpoint = "https://khodorgy.com/api/categories"
    headers = {
    'accept': 'application/json',
    'api_token': "u5XON0EPMNlKCehRvIT",
    'lang': lang
        }
    res = requests.get(endpoint,
                            headers=headers)

    res_data =  res.json()["data"]
    
    return res_data


cats_ar = get_khodorgy_categories("ar")
cats_en = get_khodorgy_categories("en")
print(cats_ar)

for i in range(0,4):
        user_dict = {}
        user_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
        user_dict["name"] = cats_en[i]["name"]
        user_dict["desc"] = "khodorgy category"
        user_dict["arabicName"] = cats_ar[i]["name"]
        user_dict["arabicDesc"] = "khodorgy category"
        user_dict["root"] = True
        user_dict["children"]= []
        user_dict["thumbnail"] = None
        user_dict["images"] = []
        user_dict["createdAt"] = datetime.now()
        user_dict["updatedAt"] = datetime.now()
        user_dict["__v"]= 0
        
        # client.backend.categories.insert_one(user_dict)


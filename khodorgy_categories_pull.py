from re import X
from pymongo import MongoClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import re

from bson.objectid import ObjectId

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

for i in range(0,3):
    print(i)


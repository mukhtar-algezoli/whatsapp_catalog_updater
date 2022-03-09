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

def get_khodorgy_products(lang):
    endpoint = "https://khodorgy.com/api/products"
    headers = {
    'accept': 'application/json',
    'api_token': "u5XON0EPMNlKCehRvIT",
    'lang': lang
        }
    res = requests.get(endpoint,
                            headers=headers)

    res_data =  res.json()["data"]
    
    return res_data


# print(get_khodorgy_products("en"))


# cats_ar = get_khodorgy_categories("ar")
# cats_en = get_khodorgy_categories("en")

# for i in range(0,4):
#         user_dict = {}
#         user_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
#         user_dict["name"] = cats_en[i]["name"]
#         user_dict["desc"] = "khodorgy category"
#         user_dict["arabicName"] = cats_ar[i]["name"]
#         user_dict["arabicDesc"] = "khodorgy category"
#         user_dict["root"] = True
#         user_dict["children"]= []
#         user_dict["thumbnail"] = None
#         user_dict["images"] = []
#         user_dict["createdAt"] = datetime.now()
#         user_dict["updatedAt"] = datetime.now()
#         user_dict["__v"]= 0
        
#         client.backend.categories.insert_one(user_dict)

products_ar = get_khodorgy_products("ar")
products_en = get_khodorgy_products("en")

for i in range(len(products_ar)):
    product_dict = {}
    product_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
    product_dict["name"] = products_en[i]["name"]
    product_dict["desc"] = products_en[i]["description"]
    product_dict["arabicName"] = products_ar[i]["name"]
    product_dict["arabicDisc"] = products_ar[i]["description"]
    product_dict["url"] = products_ar[i]["image_full_path"]
    product_dict["price"] = products_ar[i]["price"]
    product_dict["categories"] = [ObjectId("620ce3dc422c0f83d7740591")]
    product_dict["variants"] = []
    product_dict["thumbnail"] = products_ar[i]["image_full_path"]
    product_dict["images"] = []
    product_dict["createdAt"] = datetime.now()
    product_dict["updatedAt"] = datetime.now()
    product_dict["__v"]= 0
    
    # print(product_dict)
        
    # client.backend.products.insert_one(product_dict)


cats_ar = get_khodorgy_categories("ar")
cats_en = get_khodorgy_categories("en")

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
        
        output = client.backend.categories.insert_one(user_dict)
        print(output.inserted_id )
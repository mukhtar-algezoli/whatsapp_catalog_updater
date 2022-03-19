from re import X
from pymongo import MongoClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bson.objectid import ObjectId
import requests
import re
from datetime import datetime
import pandas
import gspread
import pandas as pd
import gspread_dataframe as gd
import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

client = MongoClient("mongodb+srv://enigma:A_pass2mongo@sme-platform.pkbgh.mongodb.net")



# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./semiotic-bloom-334320-53016b79b117.json', scope)

gsheets_client = gspread.authorize(creds)
df = pd.DataFrame()

def khodorgy_unit_value(unit_id):
    return {
            "1": 1,
            "2": 0.5,
            "3": 0.25,
        }[unit_id]


def khodorgy_unit_name(unit_id):
    return {
            "1": " ",
            "2": "نصف",
            "3": "ربع",
        }[unit_id]

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



# for i in range(len(products_ar)):
#     product_dict = {}
#     product_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
#     product_dict["name"] = products_en[i]["name"]
#     product_dict["desc"] = products_en[i]["description"]
#     product_dict["arabicName"] = products_ar[i]["name"]
#     product_dict["arabicDisc"] = products_ar[i]["description"]
#     product_dict["url"] = products_ar[i]["image_full_path"]
#     product_dict["price"] = products_ar[i]["price"]
#     product_dict["categories"] = [ObjectId("620ce3dc422c0f83d7740591")]
#     product_dict["variants"] = []
#     product_dict["thumbnail"] = products_ar[i]["image_full_path"]
#     product_dict["images"] = []
#     product_dict["createdAt"] = datetime.now()
#     product_dict["updatedAt"] = datetime.now()
#     product_dict["__v"]= 0
    
    # print(product_dict)
        
    # client.backend.products.insert_one(product_dict)

# time.sleep(3300)

while True:
    products_ar = get_khodorgy_products("ar")
    products_en = get_khodorgy_products("en")

    cats_ar = get_khodorgy_categories("ar")
    cats_en = get_khodorgy_categories("en")

    index = 1


    for j in range(len(cats_ar)):
            category = client.backend.categories.find_one({'name': cats_en[index - 1]["name"], "owner": ObjectId("620ce3dc422c0f83d7740591")})
            if category is not None:
                print("category found")
            
            else:
                print("category not found")
                user_dict = {}
                user_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
                user_dict["name"] = cats_en[index - 1]["name"]
                user_dict["desc"] = "khodorgy category"
                user_dict["arabicName"] = cats_ar[index - 1]["name"]
                user_dict["arabicDesc"] = "khodorgy category"
                user_dict["root"] = True
                user_dict["children"]= []
                user_dict["thumbnail"] = None
                user_dict["images"] = []
                user_dict["createdAt"] = datetime.now()
                user_dict["updatedAt"] = datetime.now()
                user_dict["__v"]= 0
                
                output = client.backend.categories.insert_one(user_dict)
            for i in range(len(products_ar)):
                if products_en[i]["category_id"] == str(index):
                    product = client.backend.products.find_one({'name': products_ar[i]["name"] + "\\"+ khodorgy_unit_name(products_ar[i]["unit_id"])+ " " +products_ar[i]["weight_unit"]["title"], "owner": ObjectId("620ce3dc422c0f83d7740591")})
                    if category is not None:
                        print("product found")
                        user = client.backend.products.find_one_and_update({'name': products_ar[i]["name"] + "\\"+ khodorgy_unit_name(products_ar[i]["unit_id"])+ " " +products_ar[i]["weight_unit"]["title"], "owner": ObjectId("620ce3dc422c0f83d7740591")},{'$set': {"price": float(products_ar[i]["price"]) * khodorgy_unit_value(products_ar[i]["unit_id"])}}, upsert=False)
                        user = client.backend.products.find_one_and_update({'name': products_ar[i]["name"] + "\\"+ khodorgy_unit_name(products_ar[i]["unit_id"])+ " " +products_ar[i]["weight_unit"]["title"], "owner": ObjectId("620ce3dc422c0f83d7740591")},{'$set': {"khodorgy_id": products_ar[i]["id"]}}, upsert=False)  
                        print("product price updated")
                    else:
                        print("product not found")
                        product_dict = {}
                        product_dict["owner"] = ObjectId("620ce3dc422c0f83d7740591")
                        product_dict["name"] = products_ar[i]["name"] + "\\"+ khodorgy_unit_name(products_ar[i]["unit_id"])+ " " +products_ar[i]["weight_unit"]["title"]
                        product_dict["desc"] = "سيتم اضافة " + khodorgy_unit_name(products_ar[i]["unit_id"])+" "+ products_ar[i]["weight_unit"]["title"] + " لكل وحدة"
                        product_dict["arabicName"] = products_ar[i]["name"] + "/"+ products_ar[i]["weight_unit"]["title"]
                        product_dict["arabicDisc"] = "سيتم اضافة " + khodorgy_unit_name(products_ar[i]["unit_id"]) + " لكل وحدة"
                        product_dict["weight_unit_title"] = products_ar[i]["weight_unit"]["title"]
                        product_dict["url"] = products_ar[i]["image_full_path"]
                        product_dict["price"] = float(products_ar[i]["price"]) * khodorgy_unit_value(products_ar[i]["unit_id"])
                        product_dict["id"] = products_ar[i]["id"]
                        product_dict["khodorgy_id"] = products_ar[i]["id"]
                        product_dict["unit_id"] = products_ar[i]["unit"]["id"]
                        product_dict["categories"] = category.id if category else [ObjectId(str(output.inserted_id))]
                        product_dict["variants"] = []
                        product_dict["thumbnail"] = products_ar[i]["image_full_path"] if str(index) != "3" else  "https://i.imgur.com/RKl8LpW.png"
                        product_dict["images"] = []
                        product_dict["createdAt"] = datetime.now()
                        product_dict["updatedAt"] = datetime.now()
                        product_dict["__v"]= 0
                        print(product_dict["name"] + " product created")

                        client.backend.products.insert_one(product_dict)
            
            index += 1

    sheet = gsheets_client.open("khodorgy_catalog_update")
    sheet_instance = sheet.get_worksheet(0)
    df = pd.DataFrame()  
    sheet_instance.resize(rows=1)
    products = client.backend.products.find({"owner": ObjectId("620ce3dc422c0f83d7740591")})
    for product in products:
        additional_images = joined_string = ",".join(product["images"])
        data = {"id":str(product["_id"]),	"title":product["name"],	"description":product["desc"],	"google_product_category":"Food, Beverages & Tobacco > Food Items > Fruits & Vegetables",	"link":"https://khodorgy.com/",	"image_link":product["thumbnail"] if product["thumbnail"]!=None else "https://i.imgur.com/RKl8LpW.png",	"condition":"new",	"availability":"in stock",	"price":product["price"],	"sale_price":" ",	"sale_price_effective_date":" ",		"brand":"no brand",	"item_group_id":str(product["categories"][0]),	"gender":" ",	"age_group":" ",	"color":" ",	"size":" ",	"shipping":" ",	"custom_label_0":" ", "additional_image_link":additional_images}
        # data = {"id":str(product["_id"]),	"title":product["name"],	"description":"some description",	"google_product_category":"product",	"product_type":"product",	"link":"https://khodorgy.com/",	"image_link":"https://i.imgur.com/RKl8LpW.png",	"condition":"new",	"availability":"in stock",	"price":product["price"],	"sale_price":" ",	"sale_price_effective_date":" ",	"gtin":str(product["categories"][0]),	"brand":"no brand",	"item_group_id":str(product["categories"][0]),	"gender":" ",	"age_group":" ",	"color":" ",	"size":" ",	"shipping":" ",	"custom_label_0":" ", "additional_image_link":additional_images}
        df = df.append(data, ignore_index=True)
    # Connecting with `gspread` here
    ws = gsheets_client.open("khodorgy_catalog_update").get_worksheet(0)
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(df)
    gd.set_with_dataframe(ws, updated)

    print("khodorgy catalog updated at time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    time.sleep(3600)
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas
import gspread
import pandas as pd
import gspread_dataframe as gd
import time

from oauth2client.service_account import ServiceAccountCredentials
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./semiotic-bloom-334320-53016b79b117.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
df = pd.DataFrame()
mongo = MongoClient("mongodb+srv://enigma:A_pass2mongo@sme-platform.pkbgh.mongodb.net")
while True:
    users = mongo.backend.users.find({"whatsapp.catalog_feed_name": { "$exists": True } } )
    for user in users:
        sheet = client.open(user["whatsapp"]["catalog_feed_name"])
        sheet_instance = sheet.get_worksheet(0)
        df = pd.DataFrame()  
        sheet_instance.resize(rows=1)
        products = mongo.backend.products.find({"owner": user["_id"]})
        for product in products:
            additional_images = joined_string = ",".join(product["images"])
            data = {"id":str(product["_id"]),	"title":product["name"],	"description":product["name"],	"google_product_category":"product",	"product_type":"product",	"link":"https://khodorgy.com/",	"image_link":product["thumbnail"] if product["thumbnail"]!=None else "https://i.imgur.com/RKl8LpW.png",	"condition":"new",	"availability":"in stock",	"price":product["price"],	"sale_price":" ",	"sale_price_effective_date":" ",	"gtin":str(product["categories"][0]),	"brand":"no brand",	"item_group_id":str(product["categories"][0]),	"gender":" ",	"age_group":" ",	"color":" ",	"size":" ",	"shipping":" ",	"custom_label_0":" ", "additional_image_link":additional_images}
            # data = {"id":str(product["_id"]),	"title":product["name"],	"description":"some description",	"google_product_category":"product",	"product_type":"product",	"link":"https://khodorgy.com/",	"image_link":"https://i.imgur.com/RKl8LpW.png",	"condition":"new",	"availability":"in stock",	"price":product["price"],	"sale_price":" ",	"sale_price_effective_date":" ",	"gtin":str(product["categories"][0]),	"brand":"no brand",	"item_group_id":str(product["categories"][0]),	"gender":" ",	"age_group":" ",	"color":" ",	"size":" ",	"shipping":" ",	"custom_label_0":" ", "additional_image_link":additional_images}
            df = df.append(data, ignore_index=True)
        # Connecting with `gspread` here
        ws = client.open(user["whatsapp"]["catalog_feed_name"]).get_worksheet(0)
        existing = gd.get_as_dataframe(ws)
        updated = existing.append(df)
        gd.set_with_dataframe(ws, updated)
    print("catalogs updated at time: " + str(time.time()))
    time.sleep(60)
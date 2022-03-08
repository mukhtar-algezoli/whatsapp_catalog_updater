from re import X
from pymongo import MongoClient

from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://enigma:A_pass2mongo@sme-platform.pkbgh.mongodb.net")

whatsapp_users = client.backend.users.find({ "whatsapp_update_file" : { "$exists" : True } })
for user in whatsapp_users:
    products = client.backend.products.find({"owner":user["_id"]})
    products = list(products)
    print(products)


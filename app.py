from re import X
from pymongo import MongoClient

from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://enigma:A_pass2mongo@sme-platform.pkbgh.mongodb.net")
products = client.backend.products.find({"owner":ObjectId(str("61f96cbffa391f211a7dd540"))})
products = list(products)
print(products)
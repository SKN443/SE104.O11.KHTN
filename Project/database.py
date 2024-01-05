from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from model import img2byte

@st.cache_resource
class Database:
    def __init__(self):
        uri = "mongodb+srv://anothernhan:trongnhan258@sebruh.7itle96.mongodb.net/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = client.test


    def query(self, vector, limit):
        '''
        inp:
        - vector: image embedding
        - limit: number of dicts return
        out:
        - list of dicts
        '''
        results = self.db.database.aggregate([
          {
            "$vectorSearch": {
              "index": "vector_index",
              "path": "vector",
              "queryVector": vector,
              "numCandidates": 1500,
              "limit": limit
              }
          }, {"$match": {"flag": 1}}
        ])
        return results

    def check_exist(self, product_id):
        return bool(self.db.database.count_documents({'product_id': product_id})) and bool(list(self.db.database.find({'product_id': product_id}))[0]['flag'])

    def find(self, product_id):
        return list(self.db.database.find({'product_id': product_id}))[0]
    
    def erase(self, product_id):
        if bool(self.db.database.count_documents({'product_id': product_id})):
            self.db.database.update_one({'product_id': product_id}, {'$set':{'flag': 0}})

    def unerase(self, product_id):
        if bool(self.db.database.count_documents({'product_id': product_id})):
            self.db.database.update_one({'product_id': product_id}, {'$set':{'flag': 1}})

    def insert(self, product_id, image, vector, category):
            self.db.database.insert_one({
                'product_id' : product_id,
                'image' : img2byte(image),
                'vector': vector,
                'category' : category,
                'flag' : 1
            })

    def update(self, product_id, image=None, vector = None, category=None):
        if image is not None:
            image = img2byte(image)
        dned = {
            'image' : image,
            'category' : category,
            'vector': vector,
            'flag' : 1
        }
        dned = {k: v for k, v in dned.items() if v is not None}
        #if check_exist(db, product_id):
        self.db.database.update_one({'product_id': product_id}, {'$set': dned})

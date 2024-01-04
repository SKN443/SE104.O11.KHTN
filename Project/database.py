from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from PIL import Image
import io

@st.cache_resource
def Init():
    uri = "mongodb+srv://anothernhan:trongnhan258@sebruh.7itle96.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client.test
    return db


def query(db, vector, limit):
    '''
    inp:
    - vector: image embedding
    - limit: number of dicts return
    out:
    - list of dicts
    '''
    results = db.database.aggregate([
      {
        "$vectorSearch": {
          "index": "vector_index",
          "path": "vector",
          "queryVector": vector,
          "numCandidates": 1500,
          "limit": limit
          }
      }
    ])
    return results

def img2byte(img):
    image_bytes = io.BytesIO()
    img.save(image_bytes, format='JPEG')
    return image_bytes.getvalue()

def byte2img(image_bytes):
    pil_img = Image.open(io.BytesIO(image_bytes))
    return pil_img

def check_exist(db, product_id):
    return bool(db.database.count_documents({'product_id': product_id})) and bool(list(db.database.find({'product_id': product_id}))[0]['flag'])

def erase(db, product_id):
    if bool(db.database.count_documents({'product_id': product_id})):
        db.database.update_one({'product_id': product_id}, {'$set':{'flag': 0}})

def unerase(db, product_id):
    if bool(db.database.count_documents({'product_id': product_id})):
        db.database.update_one({'product_id': product_id}, {'$set':{'flag': 1}})

def insert_beta(db, product_id, image, vector, category):
    if not bool(db.database.count_documents({'product_id': product_id})):
        db.database.insert_one({
            'product_id' : product_id,
            'image' : img2byte(image),
            'vector': vector,
            'category' : category,
            'flag' : 1
        })
    elif not list(db.database.find({'product_id': product_id}))[0]['flag']:
        update(db, product_id, image, category)
        unerase(db, product_id)


def insert(db, product_id, image, vector, category):
        db.database.insert_one({
            'product_id' : product_id,
            'image' : img2byte(image),
            'vector': vector,
            'category' : category,
            'flag' : 1
        })

def update(db, product_id, image=None, vector = None, category=None):
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
    db.database.update_one({'product_id': product_id}, {'$set': dned})

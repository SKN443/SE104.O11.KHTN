from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



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

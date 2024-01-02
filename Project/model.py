from imgbeddings import imgbeddings
from PIL import Image
from database import *
import io

def init_emb():
    embedding_model = imgbeddings()
    return embedding_model

def get_emb(model, img):
    if type(img) == str:
        img = Image.open(img)
    embedding = model.to_embeddings(img).flatten().tolist()
    return embedding

def byte2img(img):
    pil_img = Image.open(io.BytesIO(img))
    return pil_img

def pipeline(db, embeding_model, img, limit):
    '''
    inp:
    - img: an image (PIL image) or path to image
    - limit: number of images return
    out:
    - list of images
    '''
    emb = get_emb(embeding_model, img)
    dcts = query(db, emb, limit)
    return_imgs = [byte2img(dct['image']) for dct in dcts]
    return return_imgs

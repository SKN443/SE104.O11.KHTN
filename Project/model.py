from imgbeddings import imgbeddings
from PIL import Image
from database import *
import io

def get_emb(img):
    if type(img) == str:
        img = Image.open(img)
    embedding = imgbeddings().to_embeddings(img).flatten().tolist()
    return embedding

def byte2img(img):
    pil_img = Image.open(io.BytesIO(img))
    return pil_img

def pipeline(db, img, limit):
    '''
    inp:
    - img: an image (PIL image) or path to image
    - limit: number of images return
    out:
    - list of images
    '''
    emb = get_emb(img)
    dcts = query(db, emb, limit)
    return_imgs = [byte2img(dct['image']) for dct in dcts]
    return return_imgs
import pandas as pd
import requests
import shutil
import ast
import os

df = pd.read_csv('img_drop_measurement_final.csv')

for ids,links in enumerate(df['image_link']):
	if (ids < 0): 
		continue
	links = ast.literal_eval(links)
	for url in links:
		res = requests.get(url, stream=True)
		file_name = 'imgdata/'+str(ids)+'_'+url[url.rfind("/")+1:-4]
		if (res.status_code == 200) and (os.path.isfile(file_name)==False):
		    with open(file_name,'wb') as f:
		        shutil.copyfileobj(res.raw, f)
		    print('Image sucessfully Downloaded: ',file_name)
		else:
		    print('Image Couldn\'t be retrieved')
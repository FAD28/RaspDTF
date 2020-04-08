from txtanalysis import DataCleaner as DC
from txtanalysis.emotion import Emotionen_nrc as nrc
import pandas as pd
import time, os

def get_all_paths(x):
	"""
	Returns list of all paths

	use -> get_all_paths(os.getcwd()) 
	__________________________________
	:param:	 <str> x: 	os.getcwd()
	:Returns: list with all paths that ends with '.csv' 

	"""
	paths_liste = []
	#x = os.getcwd()
	for r, d, f in os.walk(x):
		for file in f:
			if '.csv' in file:
				paths_liste.append(os.path.join(r,file))
	return paths_liste

paths_liste = get_all_paths(os.getcwd())

def processing_sued(path_list):
	#os.chdir('')
	counter = 1
	for path in path_list:
		file = open(path)
		data = [i for i in file]

		article = DC.soft_clean([data[6]])
		headline = DC.clean_list([data[2]])
		time = DC.soft_clean([data[4]])
		summary = DC.soft_clean([data[5]])
		tags = DC.soft_clean([data[7]])
		author = DC.soft_clean([data[3]])
		headkicker = DC.soft_clean([data[1]])
		filename = DC.clean_filename(headline)
		version_name = f"{counter}-{filename}.csv"

		data_frame = pd.DataFrame({'headline': headline, 'time': time, 'tags': tags, 'article': article, 'author':author, 'headkicker': headkicker})
		# pd.set_option("display.max_rows", None, "display.max_columns", None)
		# print(data_frame)
		data_frame.to_csv(version_name, sep=';')
		print(f"FILE SUCCESSFULLY CREATED {headline} ---> {filename}.csv")
		counter += 1
	return data_frame

processing_sued(paths_liste)































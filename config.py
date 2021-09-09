import yaml

def load_config(file):
	file = open(file, 'r')
	resourse = yaml.safe_load(file)
	return resourse


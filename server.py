from bottle import request, response, run, post, get, put, delete, route
import copy
import json
import yaml


class Verwalter: #everything v2
	json_file = 'data.json'
	json_data = []
	data_by_name = dict()

	sorted = []
	sorted_up_to_date = False


	def __init__(self):

		#with open(self.json_file,'r') as file:
		#	self.json_data = json.loads(file.read())

		self.__write()

	def reset(self):
		self.json_data = []
		self.data_by_name = dict()
		self.__write()

	def __write(self):
		self.sorted_up_to_date=False
		with open(self.json_file,'w') as file:
			file.write(json.dumps(self.json_data))


	def __sort(self):
#		self.sorted = sorted(self.json_data, key=lambda k:k['name'])
		self.sorted = [self.data_by_name[key] for key in sorted(self.data_by_name.keys())]
		self.sorted_up_to_date=True


	def add(self, lagerplatz):
		#print('fuege hinzu: ' + str(lagerplatz))
		lagerplatz = copy.deepcopy(lagerplatz)

		self.json_data += [lagerplatz]
		self.data_by_name[calc_v0_name(lagerplatz)] = lagerplatz
		self.__write()

	def get(self, name):
		#print('ausgabe: ' + name)
		return copy.deepcopy(self.data_by_name[name])

	def delete(self, name):
		#print('loesche: ' + name)
		self.json_data.remove(self.data_by_name[name])
		del self.data_by_name[name]
		self.__write()

	def get_page(self, n,x=''):
		if not self.sorted_up_to_date:
			self.__sort()

		for index in range(0,len(self.sorted)):
			if calc_v0_name(self.sorted[index]) == x:
				return copy.deepcopy(self.sorted[index+1:min(index+n+1, len(self.sorted))])
			if calc_v0_name(self.sorted[index]) > x:
				return copy.deepcopy(self.sorted[index:min(index+n,len(self.sorted))])

	def get_places_with(self, articleID):
		result=[]
		return copy.deepcopy([entry for entry in self.data if entry['articleID']==articleID])


def calc_v1_id(v0_name):
	return {
		'standort':v0_name.split('-')[0],
		'lagerabschnitt':int(v0_name.split('-')[1].split(';')[0]),
		'reihe':int(v0_name.split('-')[1].split(';')[1]),
		'platz':int(v0_name.split('-')[1].split(';')[2]),
		'hoehe':int(v0_name.split('-')[1].split(';')[3]),
	}

def calc_v0_name(v1_id):
	return v1_id['standort'] + '-' + str(v1_id['lagerabschnitt']) + ';' + str(v1_id['reihe']) + ';' + str(v1_id['platz']) + ';' + str(v1_id['hoehe'])

def convert_v0_to_v1(lagerplatz):
	name_replaced = calc_v1_id(lagerplatz['name'])
	lagerplatz = {**lagerplatz, **name_replaced} #merge 2 dicts 
	del lagerplatz['name']
	return lagerplatz

def convert_v1_to_v2(lagerplatz):
	lagerplatz['kapazitaet']=lagerplatz['bestand']
	return lagerplatz

def convert_v1_to_v0(lagerplatz):
	lagerplatz['name'] = lagerplatz['standort'] + '-' + str(lagerplatz['lagerabschnitt']) + ';' + str(lagerplatz['reihe']) + ';' + str(lagerplatz['platz']) + ';' + str(lagerplatz['hoehe'])
	del lagerplatz['standort']
	del lagerplatz['lagerabschnitt']
	del lagerplatz['reihe']
	del lagerplatz['platz']
	del lagerplatz['hoehe']

	return lagerplatz

def convert_v2_to_v1(lagerplatz):
	del lagerplatz['kapazitaet']
	return lagerplatz


verwalter=Verwalter()


@get('/reset')
def reset():
	verwalter.reset()
	return 'done'


#============V0=============00

#v0
@post('/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	lagerplatz = convert_v1_to_v2(convert_v0_to_v1(lagerplatz))

	verwalter.add(lagerplatz)
	return 'done'

#v0
@get('/storagePlace')
def storage_place():
	name = str(request.query['x'])
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(convert_v1_to_v0(convert_v2_to_v1(verwalter.get(name))))


#v0
@put('/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(lagerplatz['name'])
	verwalter.add(convert_v1_to_v2(convert_v0_to_v1(lagerplatz)))

	return 'done'

#v0
@delete('/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(name)

	return 'done'

#v0
@get('/storagePlaces')
def storage_places():
	n = int(request.query['n'])
	if 'x' in request.query:
		x = request.query['x']
	else:
		x = ''

	page_v2 = verwalter.get_page(n, x)
	page_v0 = [convert_v1_to_v0(convert_v2_to_v1(entry)) for entry in page_v2]
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(page_v0)
	
#====V1===================00


#v1
@post('/v1/storagePlace')
def storagePlace():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	lagerplatz = convert_v1_to_v2(lagerplatz)

	verwalter.add(lagerplatz)
	return 'done'

#v1 (but v0 input)
@get('/v1/storagePlace')
def storage_place():
	name = str(request.query['x'])
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(convert_v2_to_v1(verwalter.get(name)))

#v1
@put('/v1/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(lagerplatz['name'])
	verwalter.add(convert_v1_to_v2(lagerplatz))

	return 'done'

#v1 (but v0 input)
@delete('/v1/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(name)

	return 'done'

#v1
@get('/v1/storagePlaces')
def storage_places():
	n = int(request.query['n'])
	if 'x' in request.query:
		x = request.query['x']
	else:
		x = ''

	page_v2 = verwalter.get_page(n, x)
	page_v1 = [convert_v2_to_v1(entry) for entry in page_v2]
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(page_v1)


#===V2================================

#v2
@post('/v2/storage_place')
def storagePlace():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.add(lagerplatz)
	return 'done'

#v2 (but v0 input)
@get('/v2/storagePlace')
def storage_place():
	name = str(request.query['x'])
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(verwalter.get(name))

#v2
@put('/v2/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(calc_v0_name(lagerplatz))
	verwalter.add(lagerplatz)

	return 'done'

#v2 (but v0 input)
@delete('/v2/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(name)
	return 'done'

#v2
@get('/v2/storagePlaces')
def storage_places():
	n = int(request.query['n'])
	if 'x' in request.query:
		x = request.query['x']
	else:
		x = ''

	page_v2 = verwalter.get_page(n, x)
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(page_v2)

#v2
@get('/v2/storagePlacesForArticlID')
def storage_places_for_article_id():
	x = int(request.query['x'])
	lagerplaetze = verwalter.get_places_with(x)
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(lagerplaetze)


#==SWAGGER======

global swagger_json
swagger_json = None
with open('swagger.yaml') as file:
	swagger_json = yaml.safe_load(file)

@route('/swagger')
def swagger():
	return swagger_json


run(host='0.0.0.0', port=8080)
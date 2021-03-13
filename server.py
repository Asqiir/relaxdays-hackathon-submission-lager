from bottle import request, response, run, post, get, put, delete
import json


class Verwalter:
	json_file = 'data.json'
	json_data = []
	data_by_name = dict()

	sorted = []
	sorted_up_to_date = False


	def __init__(self):

		#with open(self.json_file,'r') as file:
		#	self.json_data = json.loads(file.read())

		self.__write()

		for entry in self.json_data:
			self.data_by_name[entry['name']] = entry


	def __write(self):
		self.sorted_up_to_date=False
		with open(self.json_file,'w') as file:
			file.write(json.dumps(self.json_data))


	def __sort(self):
		self.sorted = sorted(self.json_data, key=lambda k:k['name'])
		self.sorted_up_to_date=True


	def add(self, lagerplatz):
		print('fuege hinzu: ' + str(lagerplatz))

		self.json_data += [lagerplatz]
		self.data_by_name[lagerplatz['name']] = lagerplatz
		self.__write()


	def get(self, name):
		print('ausgabe: ' + name)
		return self.data_by_name[name]

	def delete(self, name):
		print('loesche: ' + name)
		self.json_data.remove(self.data_by_name[name])
		del self.data_by_name[name]
		self.__write()

	def get_page(self, n,x=''):
		if not self.sorted_up_to_date:
			self.__sort()

		for index in range(0,len(self.sorted)):
			print(x)
			print(n)

			if self.sorted[index]['name'] == x:
				return self.sorted[index+1:min(index+n+1, len(self.sorted))]
			if self.sorted[index]['name'] > x:
				return self.sorted[index:min(index+n,len(self.sorted))]



def calc_new_id(v0_name):
	return {
		'standort':v0_name.split('-')[0],
		'lagerplatz':v0_name.split('-')[1].split(';')[0],
		'reihe':v0_name.split('-')[1].split(';')[1],
		'platz':v0_name.split('-')[1].split(';')[2],
		'hoehe':v0_name.split('-')[1].split(';')[3],
	}

def convert_v0_to_v1(lagerplatz):
	name_replaced = calc_v1_id(lagerplatz['name'])
	lagerplatz = lagerplatz | name_replaced
	del lagerplatz['name']
	return lagerplatz

def convert_v1_to_v2(lagerplatz):
	lagerplatz['kapazitaet']=lagerplatz['bestand']
	return lagerplatz

verwalter=Verwalter()


		


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
	return json.dumps(convert_v2_to_v1(convert_v1_to_v0(verwalter.get(calc_new_id(name)))))


#v0
@put('/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(calc_new_id(lagerplatz['name']))
	verwalter.add(convert_v1_to_v2(convert_v0_to_v1(lagerplatz)))

	return 'done'

#v0
@delete('/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(calc_new_id(name))

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
	return page_v0
	
#====V1===================00


#v1
@post('/v1/storage_place')
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
	return json.dumps(convert_v2_to_v1(verwalter.get(calc_new_id(name))))

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
	verwalter.delete(calc_new_id(name))

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
	return page_v1


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
	return json.dumps(verwalter.get(calc_new_id(name)))

#v2
@put('/v2/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(lagerplatz['name'])
	verwalter.add(lagerplatz)

	return 'done'

#v2 (but v0 input)
@delete('/v2/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(calc_new_id(name))
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
	return page_v2


run(host='0.0.0.0', port=8080)
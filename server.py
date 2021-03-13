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



verwalter=Verwalter()

@post('/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.add(lagerplatz)
	return 'done'

@get('/storagePlace')
def storage_place():
	if 'n' in request.query:
		#paginated
		n = int(request.query['n'])
		if 'x' in request.query:
			x = request.query['x']
		else:
			x = ''

		page = verwalter.get_page(n, x)
		return json.dumps(page)
	else:
		#simple get
		name = str(request.query['x'])
		response.headers['Content-Type'] = 'application/json'
		return json.dumps(verwalter.get(name))
	
@put('/storagePlace')
def storage_place():
	lagerplatz = json.loads(request.body.read().decode('utf-8'))
	verwalter.delete(lagerplatz['name'])
	verwalter.add(lagerplatz)

	return 'done'

@delete('/storagePlace')
def storage_place():
	name = str(request.query['x'])
	verwalter.delete(name)

	return 'done'


run(host='0.0.0.0', port=8080)
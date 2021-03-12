from bottle import request, response, run, post, get, put, delete
import json


class Verwalter:
	json_file = 'data.json'
	json_data = ''
	data_by_name = dict()

	def __init__(self):
		with open(self.json_file,'r') as file:
			self.json_data = json.loads(file.read())

		for entry in self.json_data:
			self.data_by_name[entry['name']] = entry


	def __write(self):
		with open(self.json_file,'w') as file:
			file.write(json.dumps(self.json_data))


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

verwalter=Verwalter()

@post('/')
def storage_place():
	lagerplatz = request.json
	verwalter.add(lagerplatz)
	return 'done'

@get('/')
def storage_place():
	name = str(request.body.read().decode('utf-8'))
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(verwalter.get(name))

@put('/')
def storage_place():
	lagerplatz = request.json
	verwalter.delete(lagerplatz['name'])
	verwalter.add(lagerplatz)

	return 'done'

@delete('/')
def storage_place():
	name = str(request.body.read().decode('utf-8'))
	verwalter.delete(name)

	return 'done'


run(host='0.0.0.0', port=8080)
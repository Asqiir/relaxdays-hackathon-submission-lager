from bottle import route, request, run, template, post, get, put, delete, request, response
import json


class Verwalter:
	json_file = 'data.json'
	json_data = ''
	data_by_name = ''

	def __init__(self):
		with open(json_file;'r') as file:
			json_data = json.loads(file.read())

		for entry in json_data:
			data_by_name[entry['name']] = entry


	def __write(self):
		with open(json_file,'w') as file:
			json_file.write(json.dumps(json_data))


	def add(self, lagerplatz):
		print('fuege hinzu: ' + str(lagerplatz))
		json_data += lagerplatz
		data_by_name[lagerplatz['name']] = lagerplatz
		self.__write()


	def get(self, name):
		print('ausgabe: ' + name)
		return data_by_name[name]

	def delete(self, name):
		print('loesche: ' + name)
		json_data.remove(data_by_name[name])
		del data_by_name[name]
		self.__write()

verwalter=Verwalter()

@post('/')
def storage_place():
	lagerplatz = request.json
	verwalter.add(lagerplatz)
	return 'done'

@get('/')
def storage_place():
	name = str(request.body.read())
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
	name = str(request.body.read())
	verwalter.delete(name)

	return 'done'


run(host='0.0.0.0', port=8080)
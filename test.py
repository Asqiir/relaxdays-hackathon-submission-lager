import requests
import json
from collections import Counter

def dict_to_list(d):
	return [d['name'],d['articleID'],d['bestand']]

def compare_lists(list1, list2): 
    #return Counter(list1) == Counter(list2)
    #return sorted([dict_to_list(entry) for entry in list1])==sorted([dict_to_list(entry) for entry in list2])
    return sorted(list1, key=lambda k:k['name'])==sorted(list2, key=lambda k:k['name'])

with open('data.json','w') as file:
	file.write('[]')

o1 = {'name':'a','articleID':3,'bestand':17}
o2 = {'name':'f','articleID':17,'bestand':17}
o3 = {'name':'d','articleID':5,'bestand':17}
o4 = {'name':'b','articleID':1,'bestand':17}
o5 = {'name':'e','articleID':1,'bestand':17}


requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o1))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o2))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o3))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o4))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o5))


with open('data.json','r') as file:
	data = json.loads(file.read())
	if not compare_lists(data,[o1,o2,o3,o4,o5]):
		print(data)
		print('wrong data POST')


r1 = requests.get("http://0.0.0.0:8080/storagePlace", params={'x':'a'})
r2 = requests.get("http://0.0.0.0:8080/storagePlace", params={'x':'f'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if r1.json() != o1 or r2.json() != o2:
		print(r1.json())
		print(r2.json())
		print('wrong data GET')

r3 = requests.get("http://0.0.0.0:8080/storagePlace", params={'n':2})
r4 = requests.get("http://0.0.0.0:8080/storagePlace", params={'n':1,'x':'b'})
r5 = requests.get("http://0.0.0.0:8080/storagePlace", params={'n':2,'x':'c'})


with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if r3.json() != [o1,o4] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r4.json() != [o3] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r5.json() != [o3,o5] :
		print(r3.json())
		print('wrong data GET PAGINATION')



o1b = {'name':'a','articleID':3,'bestand':18}
o4b = {'name':'b','articleID':0,'bestand':0}

requests.put("http://0.0.0.0:8080/storagePlace", data=json.dumps(o1b))
requests.put("http://0.0.0.0:8080/storagePlace", data=json.dumps(o4b))

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists(data,[o1b,o2,o3,o4b,o5]):
		print(data)
		print('wrong data PUT')


requests.delete("http://0.0.0.0:8080/storagePlace", params={'x':'f'})
requests.delete("http://0.0.0.0:8080/storagePlace", params={'x':'b'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists(data,[o1b,o3,o5]):
		print(data)
		print('wrong data DELETE')

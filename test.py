import requests
import json
from collections import Counter
import time

o1 = {'name':'a-1;2;3;4','articleID':3,'bestand':17}
o2 = {'name':'f-1;1;1;1','articleID':17,'bestand':17}
o3 = {'name':'d-1;1;1;1','articleID':5,'bestand':17}
o4 = {'name':'b-1;1;1;1','articleID':1,'bestand':17}
o5 = {'name':'e-1;1;1;1','articleID':1,'bestand':17}

o1v1 = {'standort':'a','lagerabschnitt':1,'reihe':2,'platz':3,'hoehe':4,'articleID':3,'bestand':17}
o2v1 = {'standort':'f','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':17,'bestand':17}
o3v1 = {'standort':'d','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':5,'bestand':17}
o4v1 = {'standort':'b','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':1,'bestand':17}
o5v1 = {'standort':'e','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':1,'bestand':17}

o1v2 = {'standort':'a','lagerabschnitt':1,'reihe':2,'platz':3,'hoehe':4,'articleID':3,'bestand':17,'kapazitaet':17}
o2v2 = {'standort':'f','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':17,'bestand':17,'kapazitaet':17}
o3v2 = {'standort':'d','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':5,'bestand':17,'kapazitaet':17}
o4v2 = {'standort':'b','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':1,'bestand':17,'kapazitaet':17}
o5v2 = {'standort':'e','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':1,'bestand':17,'kapazitaet':17}


o1b = {'name':'a-1;2;3;4','articleID':3,'bestand':18}
o4b = {'name':'b-1;1;1;1','articleID':0,'bestand':0}

o1bv1 = {'standort':'a','lagerabschnitt':1,'reihe':2,'platz':3,'hoehe':4,'articleID':3,'bestand':17}
o4bv1 = {'standort':'b','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':0,'bestand':0}

o1bv2 = {'standort':'a','lagerabschnitt':1,'reihe':2,'platz':3,'hoehe':4,'articleID':3,'bestand':17,'kapazitaet':18}
o4bv2 = {'standort':'b','lagerabschnitt':1,'reihe':1,'platz':1,'hoehe':1,'articleID':0,'bestand':0,'kapazitaet':0}



def dict_to_list(d):
	return [d['name'],d['articleID'],d['bestand']]

def compare_lists(list1, list2): 
    #return Counter(list1) == Counter(list2)
    #return sorted([dict_to_list(entry) for entry in list1])==sorted([dict_to_list(entry) for entry in list2])
    return sorted(list1, key=lambda k:k['name'])==sorted(list2, key=lambda k:k['name'])

def compare_lists2(list1, list2): 
    x1 = sorted(list1, key=lambda k:(k['standort'],k['lagerabschnitt'],k['reihe'],k['platz'],k['hoehe'],k['articleID'],k['bestand']))
    x2 = sorted(list2, key=lambda k:(k['standort'],k['lagerabschnitt'],k['reihe'],k['platz'],k['hoehe'],k['articleID'],k['bestand']))

    return all([all([x1[index][key]==x2[index][key] for key in (list(x1[index].keys()) + list(x2[index].keys()))] for index in range(0,min(len(x1),len(x2))))]) 

#    return x1==x2


#=====V0===================

with open('data.json','w') as file:
	file.write('[]')


requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o1))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o2))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o3))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o4))
requests.post("http://0.0.0.0:8080/storagePlace", data=json.dumps(o5))


with open('data.json','r') as file:
	data = json.loads(file.read())
	if not compare_lists2(data,[o1v2,o2v2,o3v2,o4v2,o5v2]):
		print(data)
		print('wrong data POST')


r1 = requests.get("http://0.0.0.0:8080/storagePlace", params={'x':'a-1;2;3;4'})
r2 = requests.get("http://0.0.0.0:8080/storagePlace", params={'x':'f-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if r1.json() != o1 or r2.json() != o2:
		print(r1.json())
		print(r2.json())
		print('wrong data GET')

r3 = requests.get("http://0.0.0.0:8080/storagePlaces", params={'n':2})
r4 = requests.get("http://0.0.0.0:8080/storagePlaces", params={'n':1,'x':'b-1;1;1;1'})
r5 = requests.get("http://0.0.0.0:8080/storagePlaces", params={'n':2,'x':'c-1;1;1;1'})


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





requests.put("http://0.0.0.0:8080/storagePlace", data=json.dumps(o1b))
requests.put("http://0.0.0.0:8080/storagePlace", data=json.dumps(o4b))

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o2v2,o3v2,o4bv2,o5v2]):
		print(data)
		print('wrong data PUT')


requests.delete("http://0.0.0.0:8080/storagePlace", params={'x':'f-1;1;1;1'})
requests.delete("http://0.0.0.0:8080/storagePlace", params={'x':'b-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o3v2,o5v2]):
		print(data)
		print('wrong data DELETE')


#========V1==============

time.sleep(0.1)
requests.get("http://0.0.0.0:8080/reset")


with open('data.json','w') as file:
	file.write('[]')


requests.post("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o1v1))
requests.post("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o2v1))
requests.post("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o3v1))
requests.post("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o4v1))
requests.post("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o5v1))
time.sleep(0.1)


with open('data.json','r') as file:
	data = json.loads(file.read())
	if not compare_lists2(data,[o1v2,o2v2,o3v2,o4v2,o5v2]):
		print(data)
		print('wrong data POST')


r1 = requests.get("http://0.0.0.0:8080/v1/storagePlace", params={'x':'a-1;2;3;4'})
r2 = requests.get("http://0.0.0.0:8080/v1/storagePlace", params={'x':'f-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if r1.json() != o1v1 or r2.json() != o2v1:
		print(r1.json())
		print(r2.json())
		print('wrong data GET')

r3 = requests.get("http://0.0.0.0:8080/v1/storagePlaces", params={'n':2})
r4 = requests.get("http://0.0.0.0:8080/v1/storagePlaces", params={'n':1,'x':'b-1;1;1;1'})
r5 = requests.get("http://0.0.0.0:8080/v1/storagePlaces", params={'n':2,'x':'c-1;1;1;1'})


with open('data.json','r') as file:
	data = json.loads(file.read())
	if r3.json() != [o1v1,o4v1] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r4.json() != [o3v1] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r5.json() != [o3v1,o5v1] :
		print(r3.json())
		print('wrong data GET PAGINATION')


requests.put("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o1bv1))
requests.put("http://0.0.0.0:8080/v1/storagePlace", data=json.dumps(o4bv1))

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o2v2,o3v2,o4bv2,o5v2]):
		print(data)
		print('wrong data PUT')


requests.delete("http://0.0.0.0:8080/v1/storagePlace", params={'x':'f-1;1;1;1'})
requests.delete("http://0.0.0.0:8080/v1/storagePlace", params={'x':'b-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o3v2,o5v2]):
		print(data)
		print('wrong data DELETE')


#============V2================================


time.sleep(0.1)
requests.get("http://0.0.0.0:8080/reset")
time.sleep(0.1)


with open('data.json','w') as file:
	file.write('[]')


requests.post("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o1v2))
requests.post("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o2v2))
requests.post("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o3v2))
requests.post("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o4v2))
requests.post("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o5v2))
time.sleep(0.1)


with open('data.json','r') as file:
	data = json.loads(file.read())
	if not compare_lists2(data,[o1v2,o2v2,o3v2,o4v2,o5v2]):
		print(data)
		print('wrong data POST')


r1 = requests.get("http://0.0.0.0:8080/v2/storagePlace", params={'x':'a-1;2;3;4'})
r2 = requests.get("http://0.0.0.0:8080/v2/storagePlace", params={'x':'f-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if r1.json() != o1v2 or r2.json() != o2v2:
		print(r1.json())
		print(r2.json())
		print('wrong data GET')

r3 = requests.get("http://0.0.0.0:8080/v2/storagePlaces", params={'n':2})
r4 = requests.get("http://0.0.0.0:8080/v2/storagePlaces", params={'n':1,'x':'b-1;1;1;1'})
r5 = requests.get("http://0.0.0.0:8080/v2/storagePlaces", params={'n':2,'x':'c-1;1;1;1'})


with open('data.json','r') as file:
	data = json.loads(file.read())
	if r3.json() != [o1v2,o4v2] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r4.json() != [o3v2] :
		print(r3.json())
		print('wrong data GET PAGINATION')
	if r5.json() != [o3v2,o5v2] :
		print(r3.json())
		print('wrong data GET PAGINATION')


requests.put("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o1bv2))
requests.put("http://0.0.0.0:8080/v2/storagePlace", data=json.dumps(o4bv2))

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o2v2,o3v2,o4bv2,o5v2]):
		print(data)
		print('wrong data PUT')


requests.delete("http://0.0.0.0:8080/v2/storagePlace", params={'x':'f-1;1;1;1'})
requests.delete("http://0.0.0.0:8080/v2/storagePlace", params={'x':'b-1;1;1;1'})

with open('data.json','r') as file:
	data = json.loads(file.read())
	
	if not compare_lists2(data,[o1bv2,o3v2,o5v2]):
		print(data)
		print('wrong data DELETE')


r = requests.get('http://0.0.0.0:8080/v2/storagePlacesForArticleID', params={'x':3})
if not r.json()==[o1bv2]:
	print(r.json())
	print('wrong ARTICLE GET')
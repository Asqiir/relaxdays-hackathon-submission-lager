This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information. My participant ID in the challenge was: CC-VOL1-37.

# How to run this project

## Prerequisites

* Docker
* Port 8080 is used here, so it shouldn't be already used
* This program uses the file `data.json`. (So this name shouldn't be used for anything else in the same direction.)

## Commands to run

```bash
git clone https://github.com/Asqiir/relaxdays-hackathon-submission-lager.git
cd relaxdays-hackathon-submission-lager
docker build -t lager .
docker run -p 8080:8080 lager
```

# How to send requests 

There are many ways to do this, here is one of them.

* the python module `requests` is needed

`<data>` has to look like this:
```json
{

	"name": <any string>,

	"articleID": <integer>,

	"bestand": <nonnegative integer>

}
```

and `<name>` is a atring without any of the following characters: ? % /


## POST
```python3
import requests
requests.post("http://0.0.0.0:8080/storagePlace", data='<data>')
```
## GET
```python3
import requests
requests.get("http://0.0.0.0:8080/storagePlace", params={'x':'<name>'})
```

## GET with pagination

```python3
import requests
requests.get("http://0.0.0.0:8080/storagePlace", params={'n':<nonnegative integer>})
requests.get("http://0.0.0.0:8080/storagePlace", params={'n':<nonnegative integer>,'x':'<name>'})
```

* both requests are valid 
* please note that `<name>` in this context can be any string that *could* be a name, but it needn't be one that actually *is* a name of one of the saved entries.
* This returns the `<nonnegative integer>` entries that are after `<name>` when sorted by name.


## PUT
```python3
import requests
requests.put("http://0.0.0.0:8080/storagePlace", data='<data>')
```

## DELETE
```python3
import requests
requests.delete("http://0.0.0.0:8080/storagePlace", params={'x':'<name>'})
```


# Docker Python project Biba

## Conventions
$ is shell
port for elastic-search is 9200
port for flask as web server is 8000

I added an extra service named web to run the flask REST API from the docker-compose.

## How to run the application
Install docker and docker-compose. Build the docker image.
$ docker-compose up


## Populate database
On the host system, go to root folder of the project
$ chmod u+x setup.sh
$ bash setup.sh

## To view the data in database
$ curl -H 'Content-Type: application/json' -X GET http://localhost:9200/playgrounds?pretty

$ curl -H 'Content-Type: application/json' -X GET http://localhost:9200/playgrounds/_search?pretty


## API Design by Examples
No amount of description beats an example.
We can create RESTAPI to use the parameters ("name", "address", "city", "province", "location") or a combination of any of them.


### GET /playgrounds

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?name=Park

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?address=227

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?city=vancouver

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?province=bc

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?province=bc&city=vancouver

$ curl -i -H "Accept: application/json" http://localhost:8000/playgrounds?name=Park&address=227&province=bc&city=vancouver

$ curl -X GET http://localhost:8000/playgrounds -d '{"location":{"top_left": {"lat": 42, "lon": -72 }, "bottom_right": { "lat": 40, "lon": -74 }}}'

This query is possible, but my internet speed is too slow to test it
$ curl -X GET http://localhost:8000/playgrounds -d '{ "name": {"Park"}, "address" : {227}, "city" : {"vancouver"}, "province" : {"bc"}, "location":{"top_left": {"lat": 42, "lon": -72 }, "bottom_right": { "lat": 40, "lon": -74 }}}'


### PUT /playgrounds/<id>

$ curl -X PUT -H "Content-Type: application/json" -d '{"name": "Kenneth Odoh", "address": "120000 Main", "city":"Burnaby", "province":"OR", "location": [10.525777, -172.651551]}' http://localhost:8000/playgrounds/4


## To do
Sanitize the payload for each function
wildcard is hardcoded in logic. In future, we will create a settings.py file for configurations.
Unit testing



## Known Issues
If there is a virtual memory errors, then on the host running the image resolves the problem. 
$ sudo sysctl -w vm.max_map_count=262144


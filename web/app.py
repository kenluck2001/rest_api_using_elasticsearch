from flask import Flask, request, jsonify, json
from elasticsearch import Elasticsearch
import certifi

ELASTICSEARCH_PORT = 9200
es = Elasticsearch([{'host': 'elasticsearch', 'port': ELASTICSEARCH_PORT}] )
indexName = "playgrounds"
docType =  "location"


parameters = ["name", "address", "city", "province", "location"]

app = Flask(__name__)

NOT_ACCEPTABLE = 406 # Request is not Acceptable
SUCCESS = 200

WILDCARD_MATCHING = False
PORT = 8000

@app.route('/index')
def hello_world():
    return 'Flask Dockerized'



@app.route('/playgrounds')
def get_every_playground():
    res = []
    queryDict = request.args

    if request.method != 'GET':
        #HANDLE ERROR
        response = app.response_class(
            response=json.dumps(res),
            status=NOT_ACCEPTABLE,
            mimetype='application/json'
        )
        return response

    if not WILDCARD_MATCHING:
        #contains no wildcard
        for tag in parameters[:-1]:
            if tag in queryDict:
                tmp = es.search(index=indexName, doc_type=docType, body={'query': {'match': {  tag : queryDict[tag] }}})
                res.append ( tmp['hits']['hits'] )

    else:
        #contains wildcard
        for tag in parameters[:-1]:
            if tag in queryDict:
                tmp = es.search(index=indexName, doc_type=docType, body={'query': {'regexp': {  tag : "*."+queryDict[tag]+".*" }}})
                res.append ( tmp['hits']['hits'] )



    if parameters[-1] in queryDict:  #handle location
        tmp = es.search(index=indexName, doc_type=docType, body={ "query": { "bool" : { "must" : { "match_all" : {} }, "filter" : { "geo_bounding_box" : { "location" : queryDict[tag]  } } } } } )
        res.append ( tmp['hits']['hits'] )


    response = app.response_class(
        response=json.dumps(res),
        status=SUCCESS,
        mimetype='application/json'
    )

    return response



@app.route('/playgrounds/<int:id>', methods=('GET', 'PUT'))
def select_playground(id):
    data = {}

    if request.method != 'PUT':
        #HANDLE ERROR
        response = app.response_class(
            response=json.dumps(data),
            status=NOT_ACCEPTABLE,
            mimetype='application/json'
        )
        return response


    res = es.index(index=indexName, doc_type=docType, id=id, body=request.json)

    response = app.response_class(
        response=json.dumps(res['result']),
        status=SUCCESS,
        mimetype='application/json'
    )

    return response




if __name__ == '__main__':
    app.run('0.0.0.0', PORT, debug=True)



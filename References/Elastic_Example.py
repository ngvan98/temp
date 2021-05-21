from elasticsearch import Elasticsearch
ES_HOST = {"host" : "localhost", "port" : 1133}
INDEX_NAME = 'crawler_english'
#TYPE_NAME = 'news_documents'
ID_FIELD = 'id'

es = Elasticsearch([ES_HOST])

def delete_index(index_name):
    res = es.indices.delete(index = index_name)
    print(" response: '%s'" % (res))

def create_index(index_name):
    res = es.indices.create(index = index_name)
    print(" response: '%s'" % (res))

#create_index(INDEX_NAME)

def search_all():
    res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
    print(" response: '%s'" % (res))

def insert_doc(title_text, tags_text, author_text, date_time_parse, siteName, CATEGORY_FIX, url):
    bulk_data = [] 
    data_dict = {}

    #data_dict['id'] = title_text
    data_dict['reference'] = url
    data_dict['title'] = title_text
    data_dict['author'] = author_text
    if date_time_parse is not None:
        data_dict['datePublished'] = date_time_parse.strftime("%d/%m/%Y")
    else:
        data_dict['datePublished'] = 'None'

    data_dict['tag'] = tags_text
    data_dict['category'] = str(CATEGORY_FIX)
    data_dict['siteName'] = siteName


    op_dict = {
        "index": {
            "_index": INDEX_NAME, 
            # "_type": TYPE_NAME, 
            # "_id": data_dict[ID_FIELD]
        }
    }

    bulk_data.append(op_dict)
    bulk_data.append(data_dict)

    print("bulk indexing...")
    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
    print(res)


def delete_doc(id):
    res = es.delete(index=INDEX_NAME, id=id)
    print(res)

#search_all()
#delete_doc(1)
#insert_doc(title_text="HTK sas", tags_text="dfbi df", author_text="van", date_time_parse=None, siteName="chinhtri", CATEGORY_FIX="business", url="http:///")
#search_all()
#create_index(INDEX_NAME)



#es.index(index='test-index', doc_type='test', id=1, body={'test': 'test'})
#es.delete(index='crawler_english', id=1)
# es.index(index='crawler_english', id=1, body={
# 	"name": "Luke Skywalker",
# 	"height": "172",
# 	"mass": "77",
# 	"hair_color": "blond",
# 	"birth_year": "19BBY",
# 	"gender": "male",
# })

# es.index(index='sw', doc_type='people', id=2, body={
# 	"name": "Alibaba",
# 	"height": "125",
# 	"mass": "23",
# 	"hair_color": "straight",
# 	"birth_year": "12BBY",
# 	"gender": "female",
# })
#es.delete(index='sw', doc_type='people', id=2)
#r = requests.get('http://localhost:1133/sw/people/_search?q=*')
#headers = {'Content-Type': 'application/json'}
#r = requests.put('http://localhost:1133/sw/people/1?pretty', headers=headers,data ={'height':'100'})
#print(r.content)



#import json
#r = requests.get('http://localhost:1133') 
#i = 1
#while r.status_code == 200:
#    r = requests.get('http://swapi.co/api/people/'+ str(i))
#    print(r.content)
#    #es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
#    i=i+1
    
#print(i)
#https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/
#https://kb.objectrocket.com/mongo-db/how-to-use-python-to-update-api-elasticsearch-documents-259
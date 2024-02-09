# from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
# from django.template import loader
from django.urls import reverse
import pickle
# import osmnx as ox
import time
# import folium
# from geopy.extra.rate_limiter import RateLimiter
# from geopy.geocoders import Nominatim
# import networkx as nx

from transformers import AutoTokenizer, AutoModel
import torch
from django.http import HttpResponse
import json

import logging, sys
logging.disable(sys.maxsize)
import faiss    

# import lucene
import os
# from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
# from java.nio.file import Paths
# from org.apache.lucene.analysis.standard import StandardAnalyzer
# from org.apache.lucene.analysis.en import EnglishAnalyzer
# from org.apache.lucene.document import Document, Field, FieldType
# from org.apache.lucene.queryparser.classic import QueryParser
# from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
# from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
# from org.apache.lucene.search.similarities import BM25Similarity


## Backend code starts here ##

## Backend code ends here ##

from django.shortcuts import render




# show function takes the input from the index page of the app and
# shows some other output given the input

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1') # you can change the model here
model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

sentences = [
"Three years later, the coffin was still full of Jello.",
"The fish dreamed of escaping the fishbowl and into the toilet where he saw his friend go.",
"The person box was packed with jelly many dozens of months later.",
"He found a leprechaun in his walnut shell."]

def convert_to_embedding(query):
    tokens = {'input_ids': [], 'attention_mask': []}
    new_tokens = tokenizer.encode_plus(query, max_length=512,
                                       truncation=True, padding='max_length',
                                       return_tensors='pt')
    tokens['input_ids'].append(new_tokens['input_ids'][0])
    tokens['attention_mask'].append(new_tokens['attention_mask'][0])
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])

    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state
    attention_mask = tokens['attention_mask']
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)

    mean_pooled = summed / summed_mask
    # print('query emb',mean_pooled)
    return mean_pooled # assuming query is a single sentence

def getSentences():
    print("getSentences")
    import json
    mySentences = []
    myUrl = []
    titles = []
    print ("dev")
    with open("maps/data2_formatted.json", "r") as read_file:
        sample_doc = json.load(read_file)
    print ("dev1")
    for sample in sample_doc:
       
        mySentences.append(sample['text'])
        myUrl.append(sample['url'])
        titles.append(sample['title'])

    # print (mySentences)
    return mySentences,myUrl,titles

def faiss_script(mean_pooled,query_embedding):
    # index = faiss.IndexFlatIP(768)   # build the index
    # print(index.is_trained)
    # index.add(mean_pooled)                  # add vectors to the index
    # print(index.ntotal)
    print(query_embedding.shape)
    print(mean_pooled[0].shape)
    print ("created new")
    # D, I = index.search(query_embedding[None, :], 4) # None dimension is added because we only have one query against 4 documents
    D, I = index.search(query_embedding, 4)
    print ("created new")
    faiss.write_index(index,"SportsDataBert.index")
    print ("created new2")
    index_loaded = faiss.read_index("SportsDataBert.index")
    # D, I = index_loaded.search(query_embedding[None, :], 4)
    D, I = index_loaded.search(query_embedding, 4)

def faissIndexCreation(mean_pooled):
    index = faiss.IndexFlatIP(768)   # build the index
    print(index.is_trained)
    index.add(mean_pooled)                  # add vectors to the index
    print(index.ntotal)
    faiss.write_index(index,"SportsDataBert.index")
    print("bert index created")

def my_embeddings():


    # initialize dictionary to store tokenized sentences
    print ("xxx3")
    mean_pooled_final = torch.empty((0,768),dtype=torch.float32)
    print ("xxx2")
    tokens = {'input_ids': [], 'attention_mask': []}
    mySentences,myUrl,titles = getSentences()
    
    mySentences = mySentences
    print(len(mySentences))
    i_prev = 0
    print ("xxx")
    # for i in range(int(len(mySentences)/10000), len(mySentences), int(len(mySentences)/10000)):
    for i in range(int(len(mySentences)/500), len(mySentences), int(len(mySentences)/500)):
        tokens = {'input_ids': [], 'attention_mask': []}
        sentences_batch = mySentences[i_prev:i]
        print('mysentences', str(i_prev), ' to ', i)
        i_prev = i

        for sentence in sentences_batch:
            # encode each sentence and append to dictionary

            new_tokens = tokenizer.encode_plus(sentence, max_length=512,
                                            truncation=True, padding='max_length',
                                            return_tensors='pt')
            tokens['input_ids'].append(new_tokens['input_ids'][0])
            tokens['attention_mask'].append(new_tokens['attention_mask'][0])
        # print('1')
        tokens['input_ids'] = torch.stack(tokens['input_ids'])
        tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
       
        with torch.no_grad():
            outputs = model(**tokens)
        # print(tokens['input_ids'].shape)
        embeddings = outputs.last_hidden_state
        attention_mask = tokens['attention_mask']
        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        masked_embeddings = embeddings * mask
        # print('3')
        summed = torch.sum(masked_embeddings, 1)
        summed_mask = torch.clamp(mask.sum(1), min=1e-9)
        # print('here')
        mean_pooled = summed / summed_mask
        # print('meanpooledsize'+str(mean_pooled.type))
        # print (mean_pooled.shape)
        # mean_pooled_final.append(mean_pooled.tolist())
        mean_pooled_final = torch.cat((mean_pooled_final,mean_pooled),dim=0)
    print('done pooling')
    print(mean_pooled_final.shape)
    import json
    import numpy
    with open("Dataset.json", "w") as f:
        json.dump(mean_pooled_final.tolist(), f)
    return mean_pooled_final

    
def sortList(s):
    import numpy
    sort_index = numpy.flip(numpy.argsort(s.tolist()))
    
    return sort_index

from sklearn.metrics.pairwise import cosine_similarity
def query(query):
    # query = "Nemo is a fish"
    query_embedding = convert_to_embedding(query)
    with open("Dataset.json", "r") as read_file:
        mean_pooled = json.load(read_file)
    index = faiss.IndexFlatIP(768)
    mean_pooled = torch.tensor(mean_pooled)
    index.add(mean_pooled)  
    print(index.ntotal)
    print ("converted")
    # mean_pooled = my_embeddings()  
    # faissIndexCreation(mean_pooled) 
    faiss.write_index(index,"SportsDataBert.index")
    print ("converted2")
    cos = torch.nn.CosineSimilarity()
    print (query_embedding.shape)
    index_loaded = faiss.read_index("SportsDataBert.index")
    print("index loaded")
    # D, I = index_loaded.search(query_embedding[None, :], 4)
    # D, I = index_loaded.search(query_embedding, 4)
    # D, I = index.search(query_embedding, 4)
    # print(len(D))
    # print(len(I))
    # with open("Dataset.json", "r") as read_file:
        # mean_pooled_list = json.load(read_file)
    # mean_pooled = torch.Tensor(mean_pooled_list)
    sim = cos(query_embedding, mean_pooled)
    # print (sim)

    sortedList = sortList(sim)
    print ("dx")
    # print (sortedList)
    # faiss_script(mean_pooled,query_embedding)
    return sortedList
    # print (sim_demo_list)

def show(request):
    
    print ("sada")
    # list = [request.POST.get("handle", None),request.POST.get("handle2", None)]
    # input1 = list[0]
    myQuery = request.POST.get("handle", None)
    sortedList = query(myQuery)
    # return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'maps/show.html', {'source':sentences, 'flag': 1})
    index = 0
    index2 = 0
    myArray = {}
    myArray2 = {}
    mySentences,myUrl,titles = getSentences()
    # print (myUrl)
    for item in mySentences:
        myArray[index] = item
        index += 1

    for item in myUrl:
        myArray2[index2] = item
        index2 += 1
    print("i am called")
    sentence1 = myArray[sortedList[0]][:400]
    sentence2 = myArray[sortedList[1]][:300]
    sentence3 = myArray[sortedList[2]][:350]
    
    url1 = myArray2[sortedList[0]]
    url2 = myArray2[sortedList[1]]
    url3 = myArray2[sortedList[2]]
    return render(request, 'maps/index.html', {'sentence1':sentence1,'url1':url1, 'sentence2':sentence2,'url2':url2, 'sentence3':sentence3 ,'url3':url3,'flag': 1,'myQuery':myQuery})
 

def route(request):
    print("submitted")
    
    return render(request, 'maps/route.html')

def create_index(dir):
    start_time = time.time()
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = EnglishAnalyzer()
    # for stop_word in analyzer.getDefaultStopSet():
        # print(str(stop_word))
    config = IndexWriterConfig (analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    

    titleType = FieldType()
    titleType.setStored(True)
    titleType.setTokenized(True)
    titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    contextType = FieldType()
    contextType.setStored(False)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    urlType = FieldType()
    urlType.setStored(True)
    urlType.setTokenized(False)
    urlType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    i=0
    time_taken=[]
    # print(len(sample_doc))
    for sample in sample_doc:
        i+=1
        title = sample['title']
        context = sample['text']
        url = sample['url']
        if i%20000 == 0:
            end_time = time.time()
            time_so_far = (end_time - start_time)
            time_taken.append(time_so_far)
            print('time taken to index ' + str(i) + ' Documents: ' + str(round(time_so_far, 2)) + ' Seconds')
        doc = Document()
        doc.add(Field('Title', str(title), titleType))
        doc.add(Field('Context', str(context), contextType))
        doc.add(Field('Url', str(url), urlType))
        writer.addDocument(doc)
    writer.close()
    end_time = time.time()
    total_time = end_time - start_time
    # x = []
    # for i in range(1,len(time_taken)+1):
    #     x.append(i*5000)
    # plt.plot(x,time_taken)
    # plt.ylabel('Time in seconds')
    # plt.xlabel('No of Records indexed')
    # plt.title('Lucene Indexing Time Plot')
    # plt.show()
    # plt.plot(time_taken)
    # print(time_taken)
    print('Total indexing time:' + str(round(time_so_far, 2)) + 'seconds')

# index returns the default page for the maps app
def index(request):
    print(" called")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # create_index('SportsDataIndex/')
    return render(request, 'maps/index.html', {})

def lucene_demo():
    import json
    import time
    with open("test/SportsDataFinal.jsonl", "r") as read_file:
        sample_doc = json.load(read_file)
        pass
    create_index('SportsDataIndex/')
    start_time = time.time()
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = EnglishAnalyzer()
    # for stop_word in analyzer.getDefaultStopSet():
        # print(str(stop_word))
    config = IndexWriterConfig (analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    

    titleType = FieldType()
    titleType.setStored(True)
    titleType.setTokenized(True)
    titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    contextType = FieldType()
    contextType.setStored(False)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    urlType = FieldType()
    urlType.setStored(True)
    urlType.setTokenized(False)
    urlType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    i=0
    time_taken=[]
    # print(len(sample_doc))
    for sample in sample_doc:
        i+=1
        title = sample['title']
        context = sample['text']
        url = sample['url']
        if i%20000 == 0:
            end_time = time.time()
            time_so_far = (end_time - start_time)
            time_taken.append(time_so_far)
            print('time taken to index ' + str(i) + ' Documents: ' + str(round(time_so_far, 2)) + ' Seconds')
        doc = Document()
        doc.add(Field('Title', str(title), titleType))
        doc.add(Field('Context', str(context), contextType))
        doc.add(Field('Url', str(url), urlType))
        writer.addDocument(doc)
    writer.close()
    end_time = time.time()
    total_time = end_time - start_time
    # x = []
    # for i in range(1,len(time_taken)+1):
    #     x.append(i*5000)
    # plt.plot(x,time_taken)
    # plt.ylabel('Time in seconds')
    # plt.xlabel('No of Records indexed')
    # plt.title('Lucene Indexing Time Plot')
    # plt.show()
    # plt.plot(time_taken)
    # print(time_taken)
    print('Total indexing time:' + str(round(time_so_far, 2)) + 'seconds')

def luceneRetrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Context', EnglishAnalyzer())
    # parser.addMultiField('Title',EnglishAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "Score": hit.score,
            "Title":doc.get("Title"),
            # "Context": doc.get("Context"),
            "Url": doc.get("Url")
        })
    
    return topkdocs



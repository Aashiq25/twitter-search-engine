import sys
import urllib.request

import requests
from django.conf import settings

from indexer import Indexer
from sentiment_analysis import analyze_sentiment
from twitter import Twitter


import json

def download_data(core, aws_url, total_docs):
    count = 1000
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        print(i)
        start = i * count
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q=*&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        # print(json_response)
        docs = json_response['response']['docs']
        processed_docs = []
        for doc in docs:
            del doc['_version_']
            processed_docs.append(doc)
        index_data(processed_docs)
        # with open('data/' + str(i) + '.json', 'w') as outfile:
        #     json.dump(docs, outfile)


def populate_metrics_data(core, aws_url, total_docs):
    count = 1000
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        print(i)
        start = i * count
        query="-replies_count:[* TO *]"
        q = urllib.parse.quote(query, encoding="UTF-8")
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q='+q+'&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        # print(json_response)
        docs = json_response['response']['docs']
        processed_docs = []
        for doc in docs:
            del doc['_version_']
            print("test")
        
            if 'reply_count' in doc:
                doc['replies_count']=doc['reply_count']
                doc['retweets_count']=doc['retweet_count']
                doc['quotes_count']=doc['quote_count']
                doc['likes_count']=doc['like_count']
                processed_docs.append(doc)
        if len(processed_docs) > 0:
            index_data(processed_docs)


def clear_deleted_fields(doc):
    if 'reply_count' in doc:
        del doc['reply_count']
    if 'like_count' in doc:
        del doc['like_count']
    if 'retweet_count' in doc:
        del doc['retweet_count']
    if 'quote_count' in doc:
        del doc['quote_count']
    if '_version_' in doc:
        del doc['_version_']


def do_sentiment_analysis(core, aws_url, total_docs):
    count = 1000
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        # print(i)
        start = i * count
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q=*&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        # print(json_response)
        docs = json_response['response']['docs']
        processed_docs = []
        for doc in docs:
            if 'sentiment' not in doc and doc['tweet_lang'] != 'hi':
                # sentiment, score, magnitude = analyze_sentiment(doc['tweet_text'], doc['tweet_lang'])
                sentiment, score, magnitude = analyze_sentiment(doc['tweet_text'])
                print(sentiment)
                clear_deleted_fields(doc)
                doc['sentiment'] = sentiment
                doc['doc_score'] = score
                doc['doc_magnitude'] = magnitude
                processed_docs.append(doc)
        if len(processed_docs) > 0:
            index_data(processed_docs)


def get_tweet_insights(core, aws_url, total_docs):
    count = 100
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        #print(i)
        start = i * count
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q=*&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        docs = json_response['response']['docs']
        processed_docs = []
        tweet_ids=[]
        for doc in docs:
            if 'replies_count' in doc and 'likes_count' not in doc:
                print(i)
                clear_deleted_fields(doc)
                tweet_ids.append(doc['id'])
        if len(tweet_ids)>0:
            ids = ','.join(tweet_ids)
            processed_docs=update_doc_with_metrics(ids,docs)

        if len(processed_docs) > 0:
            index_data(processed_docs)


def update_doc_with_metrics(ids,docs):
    tweet_metrics = t.get_metrics(ids)
    if len(tweet_metrics)>0:
        for doc in docs:
            if doc['id'] in tweet_metrics:
                tweet_id=doc["id"]
                # doc['reply_count'] = tweet_metrics[tweet_id]['reply_count']
                # doc['retweet_count'] = tweet_metrics[tweet_id]['retweet_count']
                doc['likes_count'] = tweet_metrics[tweet_id]['like_count']
                # doc['quote_count'] = tweet_metrics[tweet_id]['quote_count']
                # doc['username'] = tweet_metrics[tweet_id]["username"]
                # doc['profile_name'] = tweet_metrics[tweet_id]["profile_name"]
                # doc['profile_url'] = tweet_metrics[tweet_id]["profile_url"]
                # doc['verified'] = tweet_metrics[tweet_id]["verified"]
        return docs
    else:
        return []
def get_top_influencers(aws_url,core):
    poi_dict={"DrEricDing":21361,"PMOIndia":1046,"narendramodi":1096,"CDCDirector":855,"mansukhmandviya":1067,"KamalaHarris":1531,"CDCgov":16127,"SSalud_mx":349,"JoeBiden":23407,"POTUS":8888,"MoHFW_INDIA":636,"EricTopol":572,"HLGatell":1103,"COVIDNewsByMIB":388} 
    
    poi_influencers={}
    
    for k,v in poi_dict.items():
        #processed_docs=[]
        q="poi_name:"+k
        q= urllib.parse.quote(q, encoding="UTF-8")

        query='http://' + aws_url + ':8983/solr/' + core + '/query?q='+q+'&start=0&rows=3200'
        response = requests.get(query)
        json_response = response.json()
        print(json_response['response']["numFound"])
        docs = json_response['response']['docs']
        count=0
        
        for doc in docs:
            q = "replied_to_tweet_id:"+doc['id']+" AND sentiment:positive"
            q = urllib.parse.quote(q, encoding="UTF-8")

            reply_query = 'http://' + aws_url + ':8983/solr/' + core + '/query?q=' + \
            q+'&start=0&rows=22000'
            response = requests.get(reply_query)
            json_response = response.json()
            reply_docs=json_response['response']['docs']
            #clear_deleted_fields(doc)
            # if len(reply_docs) > 0:
            #     doc['i_replies'] = len(reply_docs)
                #processed_docs.append(doc)
            count+=len(reply_docs)
        if count>0:
            poi_influencers[k]=str(v)+","+str(count)+","+str(round((count/v)*100))
        else:
            poi_influencers[k]=str(v)+","+str(count)+","+"0"
        
        # if len(processed_docs) > 0:
        #         index_data(processed_docs)
        print(poi_influencers)
    print(poi_influencers)

    return poi_influencers




def index_data(docs):
    i.create_documents(docs)


def change_country_case(core, aws_url, total_docs):
    count = 1000
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        print(i)
        start = i * count
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q=*&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        docs = json_response['response']['docs']
        processed_docs = []
        for doc in docs:
            clear_deleted_fields(doc)
            processed_docs.append(doc)
        index_data(processed_docs)


def update_actual_reply_count(core, aws_url, total_docs):
    count = 1000
    pages = int(total_docs / count)
    rows = count
    for i in range(pages):
        print(i)
        start = i * count
        response = requests.get('http://' + aws_url + ':8983/solr/' + core + '/query?q=poi_name:*&start='
                                + str(start) + '&rows=' + str(rows))
        json_response = response.json()
        docs = json_response['response']['docs']
        processed_docs = []
        for doc in docs:
            clear_deleted_fields(doc)
            count = get_actual_reply_count(doc)
            if count > 0:
                doc['i_replies'] = count
                processed_docs.append(doc)
        if len(processed_docs) > 0:
            index_data(processed_docs)
    pass


def get_actual_reply_count(doc):
    q = "replied_to_tweet_id:" + doc['id']
    q = urllib.parse.quote(q, encoding="UTF-8")

    reply_query = 'http://' + '18.190.13.51' + ':8983/solr/' + 'IRF21P1_demo' + '/query?q=' + \
                  q + '&facet=true&facet.field=sentiment'
    response = requests.get(reply_query)
    json_response = response.json()
    print(json_response)
    return len(json_response['response']['docs'])


if __name__ == '__main__':
    i = Indexer()
    t = Twitter()
    # i.do_initial_setup()
    # i.delete_fields()
    # i.add_fields()

    ################ Indexing from other solr instances #################
    # download_data(core='IRF21P1_demo', aws_url='18.191.161.74', total_docs=179000)  # Kavi
    # download_data(core='IRF21P1', aws_url='18.217.75.107', total_docs=179000)  # Pak
    # download_data(core='IRF21P1', aws_url='18.223.120.151', total_docs=73000)  # Aashiq
    # download_data(core='IRF21P1', aws_url='3.136.97.247', total_docs=75000)  # Daya

    ############### Sentiment analysis code from google API ############
    arguments = sys.argv
    arg_type = arguments[1]
    if arg_type == "1":
        print("coming in 1")
        do_sentiment_analysis(core='IRF21P1_demo', aws_url='18.190.13.51', total_docs=400000)  # Kavi
    elif arg_type == "2":
        change_country_case(core='IRF21P1_demo', aws_url='18.190.13.51', total_docs=400000)
    elif arg_type == "3":
        update_actual_reply_count(core='IRF21P1_demo', aws_url='18.190.13.51', total_docs=80000)
    else:
        print("coming in")
        #get_tweet_insights(core='IRF21P1_demo', aws_url='18.190.13.51', total_docs=380000)  
        get_top_influencers(core='IRF21P1_demo', aws_url='18.190.13.51')
    # else:
    #     print("updating the metrics fileds")
    #     populate_metrics_data(core='IRF21P1_demo', aws_url='18.190.13.51', total_docs=380000) #entire corpus to populate replies_count,retweets_count,quotes_count

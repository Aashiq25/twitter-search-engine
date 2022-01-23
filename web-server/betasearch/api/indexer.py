import os
import pysolr
import requests

# https://tecadmin.net/install-apache-solr-on-ubuntu/


CORE_NAME = "IRF21P1_demo"
# AWS_IP = "ec2-18-218-166-215.us-east-2.compute.amazonaws.com"
AWS_IP = "18.190.13.51"


# AWS_IP = "localhost"


def delete_core(core=CORE_NAME):
    # print(os.system('sudo su - solr -c "/home/ubuntu/solr-8.11.0/bin/solr delete -c {core}"'.format(core=core)))
    print(os.system(
        '/Volumes/MacintoshHD/Users/kaviarasu/SoftwareTools/solr-8.9.0/bin/solr delete -c {core}'.format(core=core)))


def create_core(core=CORE_NAME):
    # print(os.system('sudo su - solr -c "/home/ubuntu/solr-8.11.0/bin/solr create -c {core} -n data_driven_schema_configs"'.format(core=core)))
    print(os.system(
        '/Volumes/MacintoshHD/Users/kaviarasu/SoftwareTools/solr-8.9.0/bin/solr create -c {core} -n data_driven_schema_configs'.format(
            core=core)))


class Indexer:
    def __init__(self):
        self.solr_url = 'http://' + AWS_IP + ':8983/solr/'
        self.core_url = self.solr_url + CORE_NAME
        self.connection = pysolr.Solr(
            self.core_url, always_commit=True, timeout=50000)

    def do_initial_setup(self):
        delete_core()
        create_core()
        pass

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def delete_fields(self):
        request_data = {
            "delete-field": [
                {
                    "name": "lang",
                },
                {
                    "name": "hashtags",
                },
                {
                    "name": "mentions",
                },
                {
                    "name": "tweet_urls",
                },
                {
                    "name": "tweet_emoticons",
                },
                {
                    "name": "tweet_date",
                },
                {
                    "name": "geolocation",
                },
                {
                    "name": "replied_to_tweet_id",
                },
                {
                    "name": "replied_to_user_id",
                },
                {
                    "name": "reply_text",
                },
                {
                    "name": "text_en",
                },
                {
                    "name": "text_de",
                },
                {
                    "name": "text_hi",
                }
            ]
        }

        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def add_fields(self):
        request_data = {
            "add-field": [
                {
                    "name": "poi_name",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "poi_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "verified",
                    "type": "boolean",
                    "multiValued": False
                },
                {
                    "name": "country",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "tweet_text",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "tweet_lang",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "hashtags",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "mentions",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_urls",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_emoticons",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_date",
                    "type": "pdate",
                    "multiValued": False
                },
                {
                    "name": "geolocation",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "replied_to_tweet_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "replied_to_user_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "reply_text",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "text_en",
                    "type": "text_en",
                    "multiValued": False
                },
                {
                    "name": "text_es",
                    "type": "text_es",
                    "multiValued": False
                },
                {
                    "name": "text_hi",
                    "type": "text_hi",
                    "multiValued": False
                },
                {
                    "name": "sentiment",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "doc_score",
                    "type": "pdouble",
                    "multiValued": False
                },
                {
                    "name": "doc_magnitude",
                    "type": "pdouble",
                    "multiValued": False
                },
                {
                    "name": "i_replies",
                    "type": "pint",
                    "multiValued": False
                }
            ]
        }
        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def add_sentiment_fields(self):
        request_data = {
            "add-field": [
                {
                    "name": "sentiment",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "doc_score",
                    "type": "pdouble",
                    "multiValued": False
                },
                {
                    "name": "doc_magnitude",
                    "type": "pdouble",
                    "multiValued": False
                },
                {
                    "name": "i_replies",
                    "type": "pint",
                    "multiValued": False
                }
            ]
        }
        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def add_indexed_reply_count_field(self):
        request_data = {
            "add-field": [
                {
                    "name": "i_replies",
                    "type": "pint",
                    "multiValued": False
                }
            ]
        }
        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def add_metrics_fields(self):
        request_data = {
            "add-field": [
                {
                    "name": "replies_count",
                    "type": "pint",
                    "multiValued": False
                },
                {
                    "name": "likes_count",
                    "type": "pint",
                    "multiValued": False
                },
                {
                    "name": "retweets_count",
                    "type": "pint",
                    "multiValued": False
                },
                {"name": "quotes_count",
                 "type": "pint",
                 "multiValued": False

                 }
            ]
        }
        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def delete_metric_fields(self):
        request_data = {
            "delete-field": [
                {
                    "name": "reply_count",
                },
                {
                    "name": "like_count",
                },
                {
                    "name": "retweet_count",
                },
                {
                    "name": "quote_count"
                }
            ]
        }

        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def delete_sentiment_fields(self):
        request_data = {
            "delete-field": [
                {
                    "name": "doc_score",
                },
                {
                    "name": "doc_magnitude",
                },
                {
                    "name": "sentiment",
                }
            ]
        }

        print(requests.post(self.core_url + "/schema", json=request_data).json())

    def replace_BM25(self, b=None, k1=None):
        data = {
            "replace-field-type": [
                {
                    'name': 'text_en',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'indexAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                    'queryAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.SynonymGraphFilterFactory',
                            'expand': 'true',
                            'ignoreCase': 'true',
                            'synonyms': 'synonyms.txt'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    }
                }, {
                    'name': 'text_ru',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_ru.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.SnowballPorterFilterFactory',
                            'language': 'Russian'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }, {
                    'name': 'text_de',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_de.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.GermanNormalizationFilterFactory'
                        }, {
                            'class': 'solr.GermanLightStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


if __name__ == "__main__":
    #     i.do_initial_setup()
    #     i.delete_fields()
    i = Indexer()
    # i.delete_sentiment_fields()
    # i.add_sentiment_fields()
    # i.add_metrics_fields()
    # i.delete_metric_fields()
    i.add_indexed_reply_count_field()

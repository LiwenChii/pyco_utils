# -*- coding:utf-8 -*-

__author__ = 'nico'
import pymongo
from bson import ObjectId
from src.settings import current_settings

mongo_client = pymongo.MongoClient(current_settings.MONGO_URI)
mongo_db = mongo_client[current_settings.MONGO_DB]
mongo_collection = mongo_db.get_collection(current_settings.MONGO_COLLECTION)


class CoMongo(object):
    client = mongo_client
    db = mongo_db
    collection = mongo_collection

    def __init__(self, collection=None):
        if bool(collection):
            self.collection = self.db[collection]
        else:
            self.collection = CoMongo.collection

    @staticmethod
    def ensure_collection(collection=current_settings.MONGO_COLLECTION):
        collections = CoMongo.db.collection_names()
        if collection not in collections:
            CoMongo.db.create_collection(collection)

    def insert_item(self, item, _id=None):
        if _id is not None:
            item['_id'] = ObjectId(str(_id))
        item = self.collection.insert(item)
        oid = item.__str__()
        return oid

    def get(self, oid):
        oid = ObjectId(oid=oid)
        item = self.find_one(filter={'_id': oid})
        return item

    def find_one(self, filter):
        return self.collection.find_one(filter)

    def find(self, limit=20, filter={}):
        for item in self.collection.find(filter).sort('_id', pymongo.DESCENDING).limit(limit):
            yield item

    def count(self):
        return self.collection.count()

    def remove(self, filter):
        self.collection.remove(filter)

    def fetch(self, sample):
        sample_info = sample.get('sample_info', None)
        if not sample_info:
            sample_info = sample.get('demo_info', '')

        raw = dict(
            oid=sample['_id'].__str__(),
            created_time=sample['created_time'].strftime('%Y-%m-%d %H:%M'),
            sample_info=sample_info,
        )
        return raw

    def fetch_sample_list(self, limit, filter={}):
        raw_list = [self.fetch(sample) for sample in self.find(limit, filter)]
        return raw_list


co_mongo = CoMongo()

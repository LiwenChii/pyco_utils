import os
import pymongo
from bson import ObjectId


class CoMongo(object):
    client = None
    db = None
    collection = None

    def __init__(self, db_name, collection_name, uri=None):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection_name = self.db[collection_name]

    @classmethod
    def is_siblings(cls, collection_name):
        collections = cls.db.collection_names()
        if collection_name not in collections:
            cls.db.create_collection(collection_name)

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


co_mongo = CoMongo('project', 'model')

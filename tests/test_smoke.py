import pymongo
from pytest import skip
import subprocess

from instant_mongo import InstantMongoDB


def skip_if_no_mongod():
    try:
        subprocess.check_call(['mongod', '--version'])
    except FileNotFoundError:
        skip('mongod not found')


def test_example(tmpdir):
    skip_if_no_mongod()
    with InstantMongoDB(tmpdir) as im:
        im.db.testcoll.insert({'foo': 'bar'})
        doc, = im.db.testcoll.find()
        assert doc['foo'] == 'bar'
        assert 'testcoll' in im.db.collection_names()

        doc, = im.client.test.testcoll.find()
        assert doc['foo'] == 'bar'

        client = pymongo.MongoClient(im.mongo_uri)
        doc, = client.test.testcoll.find()
        assert doc['foo'] == 'bar'


def test_get_new_test_db(tmpdir):
    skip_if_no_mongod()
    with InstantMongoDB(tmpdir) as im:
        db1 = im.get_new_test_db()
        db2 = im.get_new_test_db()
        assert db1.name != db2.name


def test_drop_everything(tmpdir):
    skip_if_no_mongod()
    with InstantMongoDB(tmpdir) as im:
        im.db['testcoll'].insert({'foo': 'bar'})
        assert 'testcoll' in im.db.collection_names()
        assert im.db['testcoll'].count() == 1
        im.drop_everything()
        assert 'testcoll' not in im.db.collection_names()
        assert im.db['testcoll'].count() == 0

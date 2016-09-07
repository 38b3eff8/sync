#!/home/zhouyifan/.virtualenvs/work/bin/python
import unittest
import sync
import os
import json
from qiniu import etag


class DBObjectTest(unittest.TestCase):

    def setUp(self):
        self.db_path = '.'
        self.db_object = sync.DBObject(self.db_path)

    def test_db_init(self):
        self.assertTrue(os.path.exists(self.db_path + '/.md5.sqlite'))

    def test_db_save(self):
        self.db_object.save('test1', 'md5')
        row = self.db_object.get('test1')
        self.assertEqual('test1', row['full_path'])
        self.assertEqual('md5', row['md5'])

    def test_db_update(self):
        self.db_object.save('test1', 'md6')
        row = self.db_object.get('test1')
        self.assertEqual('test1', row['full_path'])
        self.assertNotEqual('md5', row['md5'])


class QiniuObjectTest(unittest.TestCase):

    def setUp(self):
        with open('config.json') as f:
            config = json.load(f)
            self.q = sync.QiniuObject(**config['qiniu'])

    def test_upload_file(self):
        info = self.q.upload_file('test.py')
        ret = json.loads(info.text_body)
        self.assertIn('hash', ret)
        self.assertEqual(ret['hash'], etag('test.py'))

    def test_download_file(self):
        r = self.q.download_file('test.py')
        self.assertIsNotNone(r)
        self.assertEqual(r.status_code, 200)

    def test_download_file_none(self):
        r = self.q.download_file('test_none.py')
        self.assertIsNone(r)

    def test_get_file_info(self):
        info = self.q.get_file_info('test.py')
        ret = json.loads(info.text_body)
        print(ret['putTime'])
        self.assertIsNotNone(info)
        self.assertIn('hash', ret)
        self.assertEqual(ret['hash'], etag('test.py'))

    def test_get_file_info_none(self):
        info = self.q.get_file_info('test_none.py')
        self.assertIsNone(info)

if __name__ == '__main__':
    if os.path.exists('./.md5.sqlite'):
        os.remove('./.md5.sqlite')
    unittest.main()

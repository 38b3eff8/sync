#!/usr/bin/python3
import unittest
import sync
import os


class UnitTest(unittest.TestCase):
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


if __name__ == '__main__':
    if os.path.exists('./.md5.sqlite'):
        os.remove('./.md5.sqlite')
    unittest.main()

#!/Users/zhouyifan/.virtualenvs/work/bin/python
import hashlib
import os
import sys
import getopt
import json
import sqlite3


def init(path):
    if not os.path.exists(path):
        return

    def travel_path(path):
        print(path)
        if not os.path.exists(path):
            return

        for subpath in os.listdir(path):
            subpath = path + '/' + subpath
            if os.path.isdir(subpath):
                travel_path(subpath)
            elif os.path.isfile(subpath):
                print('{path}: {md5}'.format(
                    path=subpath, md5=md5sum(subpath))
                )
    travel_path(path)


def md5sum(file_name):
    """
    根据给定文件名计算文件MD5值
    :param file_name: 文件的路径
    :return: 返回文件MD5校验值
    """

    def read_chunks(fp):
        fp.seek(0)
        chunk = fp.read(8 * 1024)
        while chunk:
            yield chunk
            chunk = fp.read(8 * 1024)
        else:
            fp.seek(0)

    m = hashlib.md5()

    if not os.path.exists(file_name):
        return None

    with open(file_name, 'rb') as fp:
        for chunk in read_chunks(fp):
            m.update(chunk)

    return m.hexdigest()


def save_to_db():
    conn = get_connet()


def get_connet():
    if os.path.exists('.md5.sqlite'):
        return init_db()
    else:
        return sqlite3.connect('.md5.sqlite3')


def init_db():
    conn = sqlite3.connect('.md5.sqlite')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE file_md5 (
            name       TEXT,
            md5        TEXT,
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        );''')

    return conn


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    config = None
    for o, a in opts:
        if o == '-c' and os.path.exists(a):
            with open(a, 'r') as f:
                config = json.load(f)

    if 'path' in config:
        init(config['path'])
    else:
        return

if __name__ == '__main__':
    main()

import hashlib
import os


def init(path):
    if not os.path.exists(path):
        return

    for subpath in os.listdir(path):
        print(subpath)


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

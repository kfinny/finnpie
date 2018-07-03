from hashlib import sha256
import os
import os.path


class FileCache(object):

    def __init__(self, root):
        self.root = os.path.abspath(root)

    @staticmethod
    def craft_path(key):
        name = key.lower()
        return "{2}{1}{3}{1}{0}".format(name, os.path.sep, name[0], name[1])

    def _resolve(self, key):
        p = os.path.join(self.root, FileCache.craft_path(key))
        parent = os.path.split(p)[0]
        if not os.path.exists(parent):
            os.makedirs(parent)
        return p

    def put(self, data):
        digest = sha256()
        digest.update(data)
        key = digest.hexdigest()
        with open(self._resolve(key), 'wb') as fd:
            fd.write(data)
        return key

    def invalidate(self, key):
        path = self._resolve(key)
        if os.path.exists(path):
            os.remove(path)

    def get(self, key, as_path=False):
        path = self._resolve(key)
        if not os.path.exists(path):
            raise KeyError(key)
        if as_path:
            return path
        with open(path, 'rb') as fd:
            return fd.read()

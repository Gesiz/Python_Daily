from django.core.files.storage import Storage


class QiniuStorage(Storage):
    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
        pass

    def url(self, name):
        # name name 其实就是

        return 'http://qmllvum7m.hn-bkt.clouddn.com/'+name

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class CloudinaryMediaStorage(Storage):

    def _open(self, name, mode='rb'):
        import urllib.request
        return urllib.request.urlopen(self.url(name))

    def _save(self, name, content):
        public_id = os.path.splitext(name)[0]
        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
            resource_type='auto',
        )
        ext = os.path.splitext(name)[1]
        return result['public_id'] + ext

    def delete(self, name):
        cloudinary.uploader.destroy(os.path.splitext(name)[0], resource_type='image')

    def exists(self, name):
        try:
            cloudinary.api.resource(os.path.splitext(name)[0])
            return True
        except Exception:
            return False

    def url(self, name):
        public_id = os.path.splitext(name)[0]
        ext = os.path.splitext(name)[1].lstrip('.')
        return cloudinary.CloudinaryImage(public_id).build_url(format=ext or 'jpg')

    def size(self, name):
        info = cloudinary.api.resource(os.path.splitext(name)[0])
        return info.get('bytes', 0)
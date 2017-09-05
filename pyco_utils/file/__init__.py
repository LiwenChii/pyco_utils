import os
from utils import (
    date_string,
    short_uuid,
)
from . import MongoMixin
import config


class ImageFile(MongoMixin):
    __fields__ = MongoMixin.__fields__ + [
        ('user_id', int, -1),
        ('path', str, ''),
        ('name', str, ''),
        ('url_prefix', str, ''),
        ('file_type', str, ''),
    ]

    allowed_types = ['png', 'jpg', 'jpeg', 'gif']

    @classmethod
    def new_image(cls, file, user_id=-1, url_prefix='/uploads/images/', path=config.upload_images_path):
        filename = file.filename
        ps = filename.split('.')
        t = ps[-1].lower()
        if t in cls.allowed_types:
            name = cls.upload(file, path, t)
            m = cls.new(user_id=user_id, name=name, path=path, file_type=t, url_prefix=url_prefix)
            return m

    def filename(self):
        m = os.path.join(self.path, self.name)
        return m

    def url(self):
        m = '{}{}'.format(self.url_prefix, self.name)
        return m

    def gen_avatar(self, url_prefix='/uploads/avatar/', path=config.upload_avatar_path):
        ff = self.filename()
        ft = os.path.join(path, self.name)
        cmd = 'magick {} -resize 64x64 {}'.format(ff, ft)
        status = os.system(cmd)
        code = os.WEXITSTATUS(status)
        if code == 0:
            m = self.new(
                user_id=self.user_id,
                name=self.name,
                file_type=self.file_type,
                path=path,
                url_prefix=url_prefix,
            )
            return m

    @classmethod
    def upload(cls, file, path, type='jpg'):
        name = '{}_{}.{}'.format(date_string(), short_uuid(6), type)
        f = os.path.join(path, name)
        file.save(f)
        return name

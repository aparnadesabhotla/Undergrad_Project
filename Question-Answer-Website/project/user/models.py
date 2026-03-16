from django.db import models as db_models
from django.contrib.auth import models as auth_models

from PIL import Image


def image_file_name(instance, file_name):
    file_extension = file_name.split('.')[1]
    file_name = f'{instance.user.username}.{file_extension}'
    return '/'.join(['profile_pictures', file_name])


class Profile(db_models.Model):
    user = db_models.OneToOneField(auth_models.User, on_delete=db_models.CASCADE)

    biography = db_models.TextField()
    image = db_models.ImageField(default='default-profile-picture.jpg', upload_to=image_file_name)

    def __str__(self):
        return f'{self.user.username} Profile'

    def resize_image(self):
        profile_image = Image.open(self.image.path)
        if profile_image.height > 256 or profile_image.width > 256:
            size = (256, 256)
            profile_image.thumbnail(size)
            profile_image.save(self.image.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        

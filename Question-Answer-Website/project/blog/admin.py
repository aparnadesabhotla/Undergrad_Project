from django.contrib import admin
from blog import models as blog_models

admin.site.register(blog_models.Question)
admin.site.register(blog_models.Answer)

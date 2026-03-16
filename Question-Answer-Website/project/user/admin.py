from django.contrib import admin
from user import models as user_models


admin.site.register(user_models.Profile)

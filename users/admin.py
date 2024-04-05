from django.contrib import admin

from users.models import User, OneTimeCode

admin.site.register(User)
admin.site.register(OneTimeCode)

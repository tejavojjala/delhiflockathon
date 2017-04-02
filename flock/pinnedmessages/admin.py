from django.contrib import admin
from pinnedmessages.models import Messages,Reactions,Users,Comments

# Register your models here.

admin.site.register(Messages)
admin.site.register(Reactions)
admin.site.register(Users)
admin.site.register(Comments)
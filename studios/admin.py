from django.contrib import admin

# Register your models here.
from models import *

admin.site.register(Studio)
admin.site.register(StudioServices)
admin.site.register(StudioProfile)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(StudioGroup)
admin.site.register(StudioType)
#admin.site.register(ThatModel)
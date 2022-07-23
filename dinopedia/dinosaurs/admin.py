from django.contrib import admin

from dinosaurs.models import DinoOwner, DinoSize, Period

admin.site.register(DinoOwner)
admin.site.register(Period)
admin.site.register(DinoSize)

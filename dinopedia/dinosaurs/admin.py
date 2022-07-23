from django.contrib import admin

from dinosaurs.models import DinoOwner, DinoSize, EatingType, Period

admin.site.register(DinoOwner)
admin.site.register(Period)
admin.site.register(DinoSize)
admin.site.register(EatingType)

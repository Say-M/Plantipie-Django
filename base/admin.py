from django.contrib import admin
from .models import Plant, Profile

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
admin.site.register(Plant,PlantAdmin)
admin.site.register(Profile)
from django.contrib import admin
from .models import CustomUser, Province, LocalLevel, Ward, TreeSpecies

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Province)
admin.site.register(LocalLevel)
admin.site.register(Ward)
admin.site.register(TreeSpecies)

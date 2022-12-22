from django.contrib import admin
from example.models import File


@admin.register(File)
class ProfileAdmin(admin.ModelAdmin):
    model = File



# Admin
from django.contrib import admin


# Models
from .models import *




@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [ 'fileOrigin','title' ]
    search_fields = [ 'title','id','fileOrigin' ]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_filter = [ 'program' ]


@admin.register(Signature)
class SemesterAdmin(admin.ModelAdmin):
    list_filter = [ 'semester' ]
    search_fields = [ 'name','id' ]





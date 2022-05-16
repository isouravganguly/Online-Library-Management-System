from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Transfers)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Teacher)
admin.site.register(Circulation)
admin.site.register(EachBook)
admin.site.register(Department)
# admin.site.register(Recommends)


from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Member, userProfile
from .models import Project
from .models import Blog
# Register your models here.
admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Blog)
admin.site.register(userProfile)
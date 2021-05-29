
from django.urls import path,include
from .views import *

urlpatterns = [
    path('signup/',signup),
    path('createproject/',createproject),
    path('login/',login),
    path('myprofile/',myprofile),
    path('deleteproject/',deleteproject),
    path('createblog/',createblog),
    path('deleteblog/',deleteblog),
    path('logout/',logout),
    path('recd/',recommend),
    path('handlelikes/<str:type>/<int:id>',handleLikes),
    path('explore/<str:cat>/',allitems),
    path('chart/',chart),
    path('updateproject/<int:id>/',updateproject),
    path('updateblog/<int:id>/',updateblog)
]

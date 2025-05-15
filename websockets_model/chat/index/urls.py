
from django.urls import path 
from . import views
urlpatterns=[

   path ("",views.logging_in,name="logging_in"),
   path("registe",views.register,name="register"),
   path("chat",views.chat,name="chat"),

   path("existed_notif",views.existed_notif,name="existed_notif")
   
   ]
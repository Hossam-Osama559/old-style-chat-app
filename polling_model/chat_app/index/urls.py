from django.urls import path,include
from . import views
urlpatterns = [
   path ("",views.logging_in,name="logging_in"),
   path("registe",views.register,name="register"),

   path("chat",views.chat,name="chat"),

   path("check_for_msg",views.is_there_new_msg_for_me,name="check"),

   path("add_friend",views.add_new_friend,name="make_friend"),

   path("add_req",views.add_req,name="add_req"),

   path("handle",views.handle_noti_submition,name="handle_noti_submition")

]

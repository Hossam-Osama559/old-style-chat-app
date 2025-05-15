from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import loggin_in,message,make_friend
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import msg,friends,notifications

import json

def logging_in(req):


    if req.method=="POST":

        name=req.POST["username"]
        password=req.POST['password']

        user=authenticate(req,username=name,password=password)

        if user is None:

            return HttpResponse("0")
        
        else:
            # req.session.set_expiry(5)
            login(req,user)
            return HttpResponse("1")

        


    else:
        loggin_in_obj=loggin_in()
        return render(req,"log_in.html",{"form":loggin_in_obj})

def register(req):


    if req.method=="POST":

        name=req.POST["username"]
        password=req.POST["password"]

        form=loggin_in(req.POST)

        if form.is_valid():

            print("clean")

            x=form.save(commit=False)

            x.set_password(password)

            x.save()

            return HttpResponse("1")
        

        else:

            return HttpResponse("0")
            
    

    else:

        loggin_in_obj=loggin_in()
        return render(req,"register.html",{"form":loggin_in_obj})
    



@login_required
def chat(req):


        if req.method=="POST":

            content=req.POST['content']
            rec_name=req.POST['reciever_name']

            rev_user=User.objects.filter(username=rec_name)

            if len(rev_user):

                friendship=friends.objects.filter(user=req.user,friend=rev_user[0]).exists() or friends.objects.filter(user=rev_user[0],friend=req.user).exists()

                if friendship:


                    msg_obj=message(req.POST)
                    x=msg_obj.save(commit=False)
                    x.seneder=req.user
                    x.reciever=rev_user[0]
                    x.save()

                    return HttpResponse("the message is sended")
                
                else:
                    return HttpResponse("you are not friends add him then try again")
            
            else:

                return HttpResponse("the user is not exist ")

        else:
            message_obj=message()
            add_friend_obj=make_friend()

            my_msgs=msg.objects.filter(reciever=req.user.id)


            res= render(req,"chat.html",{"form":message_obj,"msgs":my_msgs,"add_friend":add_friend_obj})

            if len(my_msgs):

                print("im here")

                # res.set_cookie("last_msg_index",my_msgs[len(my_msgs)-1].id)
            

            else:
                print("im there")

                # res.set_cookie("last_msg_index","0")
            

            return res
        
def existed_notif(req):


    

    all_objs=[]


    notif=notifications.objects.filter(to_user=req.user)


    # print(notif[0].from_user)


    for noti in notif:

        obj={}

        obj["type"]=f"{noti.noti_type}"
        obj["from"]=noti.from_user.username

        obj["id"]=noti.from_user.id 
        

        
        if noti.res_type==0:

            obj["msg"]=f"{noti.from_user} don't neet to be your friend"
        elif noti.res_type==1:

            obj["msg"]=f"{noti.from_user} become your friend .."
        
        all_objs.append(obj)


    json_obj=json.dumps(all_objs)

    return HttpResponse(json_obj)
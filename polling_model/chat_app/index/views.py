from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import loggin_in,message,make_friend
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import msg,friends,notifications
# Create  your  views  here.


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

                res.set_cookie("last_msg_index",my_msgs[len(my_msgs)-1].id)
            

            else:
                print("im there")

                res.set_cookie("last_msg_index","0")
            

            return res 



@login_required
def is_there_new_msg_for_me(req):

    
    last_msg_index=int(req.COOKIES["last_msg_index"])


    last_msg_index+=1

    is_there_new_msg=msg.objects.filter(reciever=req.user.id,id__gte=last_msg_index)

    msgs=""

    for x in is_there_new_msg:

        msgs+=f"{x.seneder}: {x.content}\n"

    if len(is_there_new_msg):

        print(f"here {req.user.username}",last_msg_index)

        res= HttpResponse(msgs)
        res.set_cookie("last_msg_index",is_there_new_msg[len(is_there_new_msg)-1].id)
        return res


    else:
        print(f"there {req.user.username}",last_msg_index)
        return HttpResponse("")


@require_POST
def add_new_friend(req):

    
    if req.method=="POST":
        

        friend_name=req.POST["friend_name"]
        friend_id=User.objects.filter(username=friend_name)

        if (len(friend_id)==0):

            return HttpResponse("the user not exist")
        
        elif len(friend_id):

            is_the_friendship_already_exist=friends.objects.filter(user=req.user,friend=friend_id[0]).exists()

            if is_the_friendship_already_exist:

                return HttpResponse("already friends")
            
            else:

                # new_friend=friends(user=req.user,friend=friend_id[0])

                # new_friend.save()
                return HttpResponse(f"1{friend_name} {req.user.username}")
            

            

                
@login_required
def add_req(req):

    if req.method=="POST":

        print("adding")

        body=req.body.decode("utf-8").split(" ")

        rec_name=body[0]
        sender_name=body[1]

        users0=User.objects.filter(username=rec_name)

        users1=User.objects.filter(username=sender_name)


        if len(users0) and len(users1):
            print("yo")
            new_notif=notifications(to_user=users0[0],from_user=users1[0])
            new_notif.save()

        return HttpResponse("done")
    

    elif req.method=="GET":

        my_notif=notifications.objects.filter(to_user=req.user)

        s=""


        for x in my_notif:

            s+=f"{int(x.id)}{int(x.noti_type)}{int(x.res_type)}{x.from_user.username}\n"
        
        # print(f"this is {my_notif}  and the user is {req.user.id} ")
        
        return HttpResponse(s)




@login_required
def handle_noti_submition(req):

    if req.method=="POST":

        noti_id=req.POST["dummy"]

        print(f"the noti_id id {noti_id}")

        
        noti=notifications.objects.filter(id=noti_id)[0]


        noti.noti_type=1

        noti.to_user,noti.from_user=noti.from_user,noti.to_user 

        noti_status=req.POST["but"]

 
        noti.res_type=int(noti_status)


        if noti_status=="1":

            print("become fr")

            friends(user=req.user,friend=noti.to_user).save()

        noti.save()
        print("ddddddddd")

        return HttpResponse("done")



import json
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth.models import User 

from asgiref.sync import sync_to_async
from .models import friends , notifications ,msg

class handle_add_friend(AsyncWebsocketConsumer):

    async def connect(self):

        # self.channel=(self.scope["user"]).username
        self.user_id=self.scope["user"].id
        self.group=f"{self.user_id}"

        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(

            self.group,
            self.channel_name
        )
    

    async def receive(self,text_data):

        loaded_data=json.loads(text_data)
        user=self.scope["user"]

        if loaded_data["type_msg"]=="0":

            """adding friend"""

            username=json.loads(text_data)["friend_name"]

            is_exist=await sync_to_async(list) (User.objects.filter(username=username))

            if len(is_exist):

                """the user exist"""
                

                friend=is_exist[0]
                

                is_they_friends_already=await sync_to_async(friends.objects.filter(user=user,friend=friend).exists)()  or await sync_to_async(friends.objects.filter(user=friend,friend=user).exists)() 
                

                if is_they_friends_already:
                    """already friends"""

                    await self.send(
                    text_data=json.dumps({"is":"1"})
                )

                    


                else: 
                    """they not friends"""

                    await self.channel_layer.group_send(

                        f"{friend.id}",

                        {
                            "type":"add_req",
                            "from":user,
                            "id":user.id
                        }

                    )


                    

                    await self.send(
                    text_data=json.dumps({"is":"2"})
                )
                

            
            else:

                """the user not exist"""
                
                await self.send(
                    text_data=json.dumps({"is":"0"})
    
    
                )


        elif loaded_data["type_msg"]=="1":

            """the user accepted or rejected friendship request"""


            notif_reciever=loaded_data["id"]

            ok_or_not=loaded_data["ok_or_no"]

            msg = f"{user.username}: Sorry, I don't need to be your friend." if ok_or_not == "0" else f"{user.username}: OK, we are now friends."


            await self.channel_layer.group_send(

                f"{notif_reciever}",

                {

                    "type":"respone_to_add_req",

                    "msg":msg,

                    "ok_or_not":ok_or_not,

                    "from":user
                }
            )



    async def add_req(self,event):

        """handle when someone send add req to you """


        to_user=self.scope["user"]

        from_user=event["from"]


        await sync_to_async(notifications.objects.create)(from_user=from_user,to_user=to_user)




        await self.send(

            text_data=json.dumps({
                
                "is":"3",
                
                "from":event["from"].username,
                "id":event["id"]
            })
        )
    

    async def respone_to_add_req(self,event):

        """when someone  respond to add req you sent it to him with ok or no"""


        to_user=self.scope["user"]

        from_user=event["from"]


        await sync_to_async(notifications.objects.create)(from_user=from_user,to_user=to_user,res_type=int(event["ok_or_not"]),noti_type=1)

        ret=await sync_to_async(notifications.objects.get)(from_user=to_user,to_user=from_user)
        await sync_to_async(ret.delete)()


        if event["ok_or_not"]=="1":
                    
                    """he responded with ok and yet another friendship in the databse table """

                    await sync_to_async(friends.objects.create)(user=from_user,friend=to_user)
        
        

        await self.send(

            text_data=json.dumps({

                "is":"4",
                "msg":event["msg"]
            })
        )





class msg_handling_consumer(AsyncWebsocketConsumer):
     


    async def connect(self):
          
          
        self.user=self.scope["user"]

        await self.channel_layer.group_add(
               f"{self.user.id}msg",
               self.channel_name
          )

         
        await self.accept()
    

    async def disconnect(self):
         
         await self.channel_layer.group_discard(
              
              f"{self.user.id}msg",

              self.channel_name
         )
    


    async def  receive(self,text_data):
         
         

        loaded_data=json.loads(text_data)

        msg_conntent=loaded_data["content"]

        reciever_user=await sync_to_async(list)(User.objects.filter(username=loaded_data["reciever_name"])) 

        print(reciever_user[0])
        

        if len(reciever_user):

            are_you_friends=await sync_to_async(friends.objects.filter(user=self.user,friend=reciever_user[0]).exists)()  or await sync_to_async(friends.objects.filter(user=reciever_user[0],friend=self.user).exists)() 

            if (are_you_friends):
                
                """the friendship exist"""


                await sync_to_async(msg.objects.create)(content=msg_conntent,reciever=reciever_user[0],seneder=self.user,reciever_name=reciever_user[0].username)


                await self.channel_layer.group_send(
                    f"{reciever_user[0].id}msg",

                    {
                            
                            "type":"handle_new_msg",

                            "from":self.user.username,

                            "content":msg_conntent
                    }
                )


                await self.send(
                    
                    text_data=json.dumps(
                            
                            {
                                "state":"1",
                            }
                    )
                )
            

            else :
             
             """you are not firiends"""

             await self.send(
                  
                  text_data=json.dumps(
                       
                       {
                            "state":"0",
                            
                       }
                  )
             )

    

            
        else :
             
             """you are not firiends"""

             await self.send(
                  
                  text_data=json.dumps(
                       
                       {
                            "state":"0",
                            
                       }
                  )
             )

    


    async def handle_new_msg(self,event):
         

         await self.send(
              
              text_data=json.dumps(
                   
                   {
                        
                        "state":"2",

                        "msg":f"{event['from']}:{event['content']}"
                   }
              )
         )
        




         

     

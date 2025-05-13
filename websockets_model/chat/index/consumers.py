import json
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth.models import User

from asgiref.sync import sync_to_async
# from .forms import m
from .models import friends

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
        print(text_data)

        print("here we are")
        print(json.loads(text_data)["friend_name"])

        username=json.loads(text_data)["friend_name"]

        is_exist=await sync_to_async(list) (User.objects.filter(username=username))

        if len(is_exist):
            print(f"there we are",{is_exist[0]})

            friend=is_exist[0]
            user=self.scope["user"]

            is_they_friends_already=await sync_to_async(friends.objects.filter(user=user,friend=friend).exists)()

            if is_they_friends_already:
                await self.send(
                text_data=json.dumps({"is":"1"})
            )

                print("they are already friends")


            else: 
                print("they not")

                await self.channel_layer.group_send(

                    f"{friend.id}",

                    {
                        "type":"add_req",
                        "from":user.username,
                        "id":user.id
                    }

                )

                # await sync_to_async(friends.objects.create)(user=user,friend=friend)

                

                await self.send(
                text_data=json.dumps({"is":"2"})
            )
              

        
        else:

            print("not exist")
            
            await self.send(
                text_data=json.dumps({"is":"0"})
            )



    async def add_req(self,event):


        await self.send(

            text_data=json.dumps({
                
                "is":"3",
                
                "from":event["from"],
                "id":event["id"]
            })
        )
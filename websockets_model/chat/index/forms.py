from django.contrib.auth.models import User
from .models import msg , friends
from django import forms
from django.core.exceptions import ValidationError

class loggin_in(forms.ModelForm):

    class Meta:

        model=User

        fields=['username','password']

    
    def clean(self):
        clean_data= super().clean()

        is_the_name_exiast=User.objects.filter(username=clean_data['username']).exists()

        if is_the_name_exiast:
            raise ValidationError("exist")
        
        else:
            return clean_data



class message(forms.ModelForm):


  
    class Meta:

        model=msg

        fields=['content','reciever_name']
    



class make_friend(forms.Form):

    friend_name=forms.CharField(max_length=10)

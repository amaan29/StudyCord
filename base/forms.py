from django.forms import ModelForm    #importing modelForm  (inbuilt function to handle forms)
from django.contrib.auth.forms import UserCreationForm     
from .models import Room, User            #importing room from models/database to access the details of em
# from django.contrib.auth.models import User



#creating new form fro user registration
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):        #created a class for form
    class Meta:
        model = Room             
        fields = '__all__'      # it will take all the titles of room in model and make a form out of it
        exclude = ['host', 'participants']  #it will exclude host and participnants from form



class UserFrom(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
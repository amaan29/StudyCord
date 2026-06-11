from django.db import models
# from django.contrib.auth.models import User  #removing default user model cause its no longer needed
from django.contrib.auth.models import AbstractUser   #importing abstact user

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg") #image firld rely on a third party package called pillow to be processed. django cant process image on its own
    #in order for this field to work install pillow in terminal
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):    #inhareting from models 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # Foreighkey defines one to many relationship. means topic can have many rooms by one room can only have single topic. on delete command means if topic is deleted the room will set to 0)
    name = models.CharField(max_length=200)   #Room name that can be max lenght of 200
    description = models.TextField(null=True, blank=True)    #textfield is used for large amount of text. null set to blank so that discroption can be (blank)set to empty, blank=True while submitting form discription can be set to empty
    participants = models.ManyToManyField(User, related_name='participants', blank=True)   #gave many to many relationship because participants will interfare with many things at once. 
    updated = models.DateTimeField(auto_now=True) #whenever save method is called its gonna take timestamp of it.
    created = models.DateTimeField(auto_now_add=True) #take a snapshot of when it was first created/updated

    class Meta:
        ordering = ['-updated', '-created']   #to get recently updated or created items on top. by default its opposite so we use - (dash) to reverse 

    def __str__(self):    #without this function room will be shown in int e.g (1). to show it in str we eill have to convert in one which is what this function do. it is for admin panel
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  #its the child of room class #if room deleted the message will be deleted as well
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #whenever save method is called its gonna take timestamp of it.
    created = models.DateTimeField(auto_now_add=True) #take a snapshot of when it was first created/updated

    class Meta:
        ordering = ['-updated', '-created']    #makes sure that mwssage is always and everywhere in decending order (means recent to old)

    def __str__(self):    #without this function body will be shown in int e.g (1). to show it in str we eill have to convert in one which is what this function do. it is for admin panel
        return self.body[0:50]
    

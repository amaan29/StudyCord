from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#from django.contrib.auth.models import User    #since user model is a man mad model now so we willl import it from models
# from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserFrom, MyUserCreationForm



def loginPage(request):
    page = 'login'    # page variable is gieven to check if user is in the login page

    if request.user.is_authenticated:      #restrict users from acessing login page if theyre already logged in
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()    #get username of user and store it in database
        password = request.POST.get('password')    #get password

        try:
            user = User.objects.get(username=username)   #check if user already exist in database, if yes then next function
        except:
            messages.error(request, 'User does not exist')  #if no then error pops up

        user = authenticate(request, username=username, password=password) #checks if username and password matches with whats in the database

        if user is not None:     #is its not none that means user is available in database
            login(request, user)   #login the user
            return redirect('home')  #return user to home page
        else:
            messages.error(request, 'Username OR Password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()           #inbuilt django form for registration

    if request.method == 'POST':        #check if user passing data
        form = MyUserCreationForm(request.POST)        #send it to user creation form
        if form.is_valid():                         #check if form is valid, #if yes
            user = form.save(commit=False)          #save this form and freeze it in time to access the user information for further authentication
            user.username = user.username.lower()      #make sure username is in lowercase
            user.save()                                #save the user
            login(request, user)                       #login the user
            return redirect('home')                      # send them to home page
        else:                                          #if form not valid
            messages.error(request, 'An error occured during registration')     #error occure 

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    #it makes sure is q is empty then all the room loads else the given load
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )     #filter the room as per topic name, icontain command - when you write few letters it gives possible available room suggestions as per the letter
              # Q helps us wrap diff search mehtods together with OR gateway

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))        #gets only the messages filtered by the topics if not filtered then it will show all


    context = {'rooms' : rooms, 'topics': topics, 'room_count': room_count, 'room_messages' : room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) #this logic will help room id match with ulr primary key. it will make sure that we land on the correct on the same url 
    room_messages = room.message_set.all()   # give us the set of messages that are related to this room
    
    participants = room.participants.all()     #to access all the participants
 
    if request.method == 'POST':               #check and varify the request if its post
        message = Message.objects.create(      #create a message
            user=request.user,                 #the user requesting 
            room=room,                         #the room in which the message is created
            body=request.POST.get('body')      #the message to be created
        )
        room.participants.add(request.user)     #to add a user in particiants whenerver he comments
        return redirect('room', pk=room.id)    #redirect on the same page
    
    context = {'room' : room, 'room_messages': room_messages, 'participants': participants}

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)   #it wiil get user  
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics =  Topic.objects.all()
    context = {'user':user, 'rooms': rooms, 'room_messages':room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')    #restrict user from creating room if they are not logged in 
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':          #to get data from user
        topic_name = request.POST.get('topic')      #gets topic name
        topic, created = Topic.objects.get_or_create(name=topic_name)    #c\if topic exist if gets else creates

        Room.objects.create(              #creates new room
            host=request.user,
            topic= topic, 
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        
    
        return redirect('home')       #redirect user to the home page
    context = {'form' : form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):     #to update the room. passing primary kwy to know what room is getting updated
    room = Room.objects.get(id=pk)    #to get the exact room
    form = RoomForm(instance=room)    #the form will be filled with original room values
    topics = Topic.objects.all()

    if request.user != room.host:          #it makes sure that only host can edit their room
        return HttpResponse('You are not allowed!!')

    if request.method == 'POST':          #to process data from user
        topic_name = request.POST.get('topic')      #gets topic name
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic_name
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')       #redirect user to the home page
        
    context = {'form' : form,  'topics' : topics, 'room' : room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:          #it makes sure that only host can delete their room
        return HttpResponse('You are not allowed!!')
    
    if request.method == 'POST':          
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:          #it makes sure that only host can delete their room
        return HttpResponse('You are not allowed!!')
    
    if request.method == 'POST':          
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url=login)
def updateUser(request):
    user = request.user
    form = UserFrom(instance=user)

    if request.method == 'POST':
        form = UserFrom(request.POST, request.FILES, instance=user)  #files function will accept user files
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages' : room_messages})

#from django.http import JsonResponse  #json = javascript object notation is a format of data, format of how we can provide data
#commented athat cause we dont want data in Json we want it in what django rest framework gives us
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room    #to access rooms from models in base app
from .serializers import RoomSerializers    #importing serialized room to get on api screen

@api_view(['GET'])    #this view can only take GET request we can also specifly PUT and POST
def getRoutes(request):  #function to show all the routes in out api
    routes = [
        'GET /api' 
        'GET /api/rooms',       # gives all the room in our database
        'GET /api/rooms/:id'    #gives specific room

    ]
    #return JsonResponse(routes, safe=False)  no longer need it cause we are not getting json response #safe=False - we can use other than python dictionary. allow list to convert data into Json response
    return Response(routes)    #django response give much more options and Json response as well



#this was just to get interface now lets add more function

'''
function to get rooms
@api_view(['GET'])     #define the respose type in this case its GET
def getRooms(request):
    rooms = Room.objects.all()     #gets all the rooms
    return Response(rooms)          #return rooms
'''   
#it will show error cause python objects cannot be converted automatically in Json response
#for that we use serializers 


@api_view(['GET'])     #define the respose type in this case its GET
def getRooms(request):
    rooms = Room.objects.all()     #gets all the rooms
    serializer = RoomSerializers(rooms, many=True)   #  many=True - means we are getting many objcects. used when objects are many
    return Response(serializer.data)          #return serialized data
    



#now lets suppose we dont want users to js allow to see the room. we want to give them authority to open that room in their website or smt

#to get a single room by its ID
@api_view(['GET'])     #define the respose type in this case its GET
def getRoom(request, pk):
    room = Room.objects.get(id=pk)     #gets specified room
    serializer = RoomSerializers(room, many=False)   #  many=Fale - return back a single object 
    return Response(serializer.data)          #return serialized data
    

#now if you call this api fro unknown frontend it will give error cause default django doesnt allow unknown 
#frontend to call our API.
#we have option to either let any unknown source call our API or give out specific URLs to certain frontends

# to allow unknown sources to access our api data we can use third party package 
# to install - python -m pip install django-cors-headers
#now add  'corsheaders' to installed app in settings of root app

#now add  "corsheaders.middleware.CorsMiddleware" to middleware in settings of root app
'''
three types
CORS_ALLOWED_ORIGINS - allow specific urls 

Example:

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]


CORS_ALLOWED_ORIGIN_REGEXES  - allow certain types of domains
ex - 
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
]


CORS_ALLOW_ALL_ORIGINS - allow all 
'''

#to allow all add in setting and make it true
# ex - 
#  CORS_ALLOW_ALL_ORIGINS = True
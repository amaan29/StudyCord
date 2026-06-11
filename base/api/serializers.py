#classes that take a model and turn it into a Json data( turn python object into Json data)


from rest_framework.serializers import ModelSerializer  #importing serializer
from base.models import Room                            #importing room here to serialize it
 

class RoomSerializers(ModelSerializer):       #made a class to serialize room data
    class Meta:
        model = Room                           #accessing room model
        fields = '__all__'                     #serializing all the data in the room


#after serializing we import this serialized data in views and the process
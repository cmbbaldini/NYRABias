from .models import Race
from .serializers import RaceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .filters import RaceFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(["GET"])
def raceGet(request, format=None):
    raceFilter = RaceFilter(request.data, queryset=Race.objects.all())
    serializer = RaceSerializer(raceFilter.qs, many=True)
    return Response(serializer.data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def racePost(request, format=None):
    serializer = RaceSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("Race already exists", status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def raceUpdateDel(request, mydate, track, raceNumber, format=None):
    try:
        race = Race.objects.get(date=mydate, track=track, raceNumber=raceNumber)
    except Race.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = RaceSerializer(race, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        race.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
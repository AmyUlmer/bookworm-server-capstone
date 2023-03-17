from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bookwormapi.models import Event, Reader


class EventView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        event = Event.objects.get(pk=pk)
        # serialize to convert data to json
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        events = Event.objects.all()
        
        #if reader parameter is included in, the events are filtered by 'reader_id' to only include events that that reader joined. 
        if "reader" in request.query_params:
            query = request.GET.get('reader')
            query_int = int(query)
            events = Event.objects.all()
            events = events.filter(reader_id=query_int)
        else:
            events = Event.objects.all()

        reader = Reader.objects.get(user=request.auth.user)

        # for each event, function checks if the currently authenticated user is in the "attendees" list for event.
        # If they are, the 'joined' property on the event is set to 'true', otherwise 'false' 
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the reader is in the attendees list on the event
            event.joined = reader in event.attendees.all()

        # 'events' query is passed to the EventSerializer class to be serialized into JSON data
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for organizers
    """
    class Meta:
        model = Reader
        fields = ('full_name',)

class AttendeeSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Reader
        fields = ('full_name',)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    # game = EventGameSerializer(many=False)
    reader = OrganizerSerializer(many=False)
    attendees = AttendeeSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'event_name', 'book', 'organizing_reader', 'location',
                'date_of_event', 'start_time', 'end_time', 'max_capacity', 'image_url','attendees', 'joined')

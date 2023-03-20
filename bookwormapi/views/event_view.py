from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bookwormapi.models import Event, Reader, Book
from rest_framework.decorators import action


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
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        #get the book from the request query params
        book = request.query_params.get('book')

        if book:
            #filter the event queryset by the Book id
            events = Event.objects.filter(book_id=book)
        else:
            #get all events
            events = Event.objects.all()
        
        # for each event, function checks if the currently authenticated user is in the "attendees" list for event.
        reader = Reader.objects.get(user=request.auth.user)
        # If they are, the 'joined' property on the event is set to 'true', otherwise 'false' 
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the reader is in the attendees list on the event
            event.joined = reader in event.attendees.all()
    
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        #getting the user that is logged in 
        organizing_reader = Reader.objects.get(user=request.auth.user)
        #retrieve book from database. make sure the book the user is trying to add with new event actually exists in database  
        book = Book.objects.get(pk=request.data["book"])

        #whichever keys are used on the request.data must match what the client is passing to the server.
        event = Book.objects.create(
            event_name=request.data["event_name"],
            location=request.data["location"],
            date_of_event=request.data["date_of_event"],
            start_time=request.data["start_time"],
            end_time=request.data["start_time"],
            max_capacity=request.data["max_capacity"],
            image_url=request.data["image_url"],
            organizing_reader=organizing_reader,
            book=book
        )
        
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a event
        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.event_name=request.data["event_name"]
        event.location=request.data["location"],
        event.date_of_event=request.data["date_of_event"],
        event.start_time=request.data["start_time"],
        event.end_time=request.data["start_time"],
        event.max_capacity=request.data["max_capacity"],
        event.image_url=request.data["image_url"]

        book = Book.objects.get(pk=request.data["book"])
        event.book = book
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        reader = Reader.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(reader)
        return Response({'message': 'Reader added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Deletes request for a user to leave an event"""

        reader = Reader.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(reader)
        return Response({'message': 'Reader removed'}, status=status.HTTP_204_NO_CONTENT)

class EventBookSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Book
        fields = ('id', 'title',)

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
    book = EventBookSerializer(many=False)
    organizing_reader = OrganizerSerializer(many=False)
    attendees = AttendeeSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'event_name', 'book', 'location', 'organizing_reader',
                'date_of_event', 'start_time', 'end_time', 'max_capacity', 'image_url','attendees', 'joined')

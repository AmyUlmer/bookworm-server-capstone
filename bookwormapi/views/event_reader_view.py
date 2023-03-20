def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        #get the Reader from the request query params
        reader = request.query_params.get('reader')

        if reader:
            #filter the event queryset by the Reader id
            events = Event.objects.filter(reader_id=reader)
        else:
            #get all events
            events = Event.objects.all()

         # for each event, function checks if the currently authenticated user is in the "attendees" list for event.
        # If they are, the 'joined' property on the event is set to 'true', otherwise 'false' 
        # Set the `joined` property on every event
        # for event in events:
            # Check to see if the reader is in the attendees list on the event
            # event.joined = reader in event.attendees.all()

        # 'events' query is passed to the EventSerializer class to be serialized into JSON data
        # serializer = EventSerializer(events, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK

        reader = Reader.objects.get(user=request.auth.user)
"""View module for handling requests about book genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bookwormapi.models import BookGenre


class BookGenreView(ViewSet):
    """Level up book genres view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book genre

        Returns:
            Response -- JSON serialized book genre
        """
        book_genre = BookGenre.objects.get(pk=pk) #get a single object from database on the pk in the URL 
        #use ORM to get data
        serializer = BookGenreSerializer(book_genre) #serialize to convert data to json
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all book genres

        Returns:
            Response -- JSON serialized list of book genres
        """
        book_genres = BookGenre.objects.all()
        serializer = BookGenreSerializer(book_genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for book genres
    """
    class Meta:
        model = BookGenre
        fields = ('id', 'label')    
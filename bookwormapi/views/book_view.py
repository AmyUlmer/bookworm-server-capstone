"""View module for handling requests about books"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bookwormapi.models import Book, Reader, BookGenre


class BookView(ViewSet):
    """Bookworm book view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book

        Returns:
            Response -- JSON serialized book
        """
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)  # serialize to convert data to json
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all booka

        Returns:
            Response -- JSON serialized list of books
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized book instance
        """
        # getting the user that is logged in
        # use request.auth.user to get Reader obj based on user
        reader = Reader.objects.get(user=request.auth.user)
        # retrieve BookGenre from database. make sure the book genre the user is trying to add with new book actually exists in database
        book_genre = BookGenre.objects.get(pk=request.data["book_genre"])

        # whichever keys are used on the request.data must match what the client is passing to the server.
        book = Book.objects.create(
            author=request.data["author"],
            title=request.data["title"],
            released_date=request.data["released_date"],
            length=request.data["length"],
            reader=reader,
            book_genre=book_genre,
            image_url=request.data["image_url"]
        )
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a book

            Returns:
            Response -- Empty body with 204 status code
            """
        book = Book.objects.get(pk=pk)
        book.author = request.data["author"]
        book.title=request.data["title"]
        book.released_date=request.data["released_date"]
        book.length=request.data["length"]
        book.image_url=request.data["image_url"]

        book_genre = BookGenre.objects.get(pk=request.data["book_genre"])
        book.book_genre = book_genre
        book.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books"""

    class Meta:
        model = Book
        fields = ('id','author', 'title', 'released_date',
                'length', 'description', 'book_genre', 'reader', 'image_url')
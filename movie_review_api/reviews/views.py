from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken  # Import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing movie reviews."""
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user (authenticated or not)

    def perform_create(self, serializer):
        """Save the review with the current user as the author if authenticated, else None."""
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    def destroy(self, request, *args, **kwargs):
        """Delete a review instance."""
        try:
            review = self.get_object()  # Get the review instance by primary key (pk)
            review.delete()  # Delete the review
            return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 No Content on success
        except Http404:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        """Update a review instance."""
        try:
            review = self.get_object()  # Get the review instance by primary key (pk)
            serializer = self.get_serializer(review, data=request.data)  # Pass the existing review and new data

            if serializer.is_valid():  # Validate the data
                serializer.save()  # Save the updated review
                return Response(serializer.data)  # Return updated data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

        except Http404:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

def home(request):
    """Home view that returns a welcome message."""
    return HttpResponse("Welcome to the Movie Review API!")

class CustomAuthToken(ObtainAuthToken):
    """Custom Auth Token view."""
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)

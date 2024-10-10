from rest_framework import serializers
from .models import Review
from .models import CustomUser  # Import CustomUser model

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),  # Provide a queryset for the user field
        required=False,
        allow_null=True  # Make user optional
    )

    class Meta:
        model = Review
        fields = '__all__'  # Alternatively, you can specify fields explicitly if needed.

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """Create a new review instance."""
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing review instance."""
        instance.movie_title = validated_data.get('movie_title', instance.movie_title)
        instance.content = validated_data.get('content', instance.content)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

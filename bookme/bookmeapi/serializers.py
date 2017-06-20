from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Book, Issue

class IssueSerializer(serializers.ModelSerializer):
    
    book = serializers.HyperlinkedRelatedField(view_name='book-detail', queryset=Book.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = Issue
        fields = ('book', 'user', 'approved')

class BookSerializer(serializers.HyperlinkedModelSerializer):
    
    bookissue = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'category', 'bookissue')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from .models import Book, Issue
from .serializers import IssueSerializer, BookSerializer, UserSerializer

class HomeView(TemplateView):
    template_name = 'book.html'

class BookListCreateView(ListCreateAPIView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @permission_classes((IsAdminUser,))
    def create(self, request, *args, **kwargs):
        return super(BookListCreateView, self).create(request, *args, **kwargs)

    @permission_classes((IsAuthenticated,))
    def list(self, request, *args, **kwargs):
        return super(BookListCreateView, self).list(request, *args, **kwargs)


class BookDetail(GenericAPIView):
    model = Book
    serializer_class = BookSerializer()
    queryset = Book.objects.all()

    def get(self, request, pk):
        book = self.get_object()
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)


class UserDetail(GenericAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, pk):
        id_user = self.get_object()
        serializer = UserSerializer(id_user, context={'request': request})
        return Response(serializer.data)


class IssueListCreateView(ListCreateAPIView):
    model = Issue
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)


class IssueUpdateView(UpdateAPIView):
    model = Issue
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IsAdminUser,)


class UserListCreateView(ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

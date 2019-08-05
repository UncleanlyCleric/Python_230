from django.shortcuts import render
from blogging.models import Post, Category
from django.contrib.auth.models import User, Group

from .serializers import PostSerializer, CategorySerializer, UserSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to view blog posts.
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to view blog posts.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

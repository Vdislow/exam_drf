from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer
from account.models import Author
from .permissions import IsAuthorPermission, IsStaffPermission,StatusAddPermission


class NewsListCreateView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthorPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    # def get_queryset(self):
    #     return self.queryset.filter(author=self.kwargs['author_id'])


class NewsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthorPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author, news=News.objects.get(id=self.kwargs["news_id"]))

    def get_queryset(self):
        return self.queryset.filter(news=self.kwargs['news_id'])


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author, news=News.objects.get(id=self.kwargs["news_id"]))

    def get_queryset(self):
        return self.queryset.filter(news=self.kwargs['news_id'])


class StatusesListCreate(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsStaffPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class StatusesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsStaffPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class NewsStatusGET(APIView):
    permission_classes = (StatusAddPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, status_slug):
        news = get_object_or_404(News, id=news_id)
        news_status = get_object_or_404(Status, slug=status_slug)
        try:
            stat_add = NewsStatus.objects.create(news=news, author=request.user.author, status=news_status)
        except IntegrityError:
            stat_add = NewsStatus.objects.get(news=news, author=request.user.author,)
            data = {'message': f'You already added status'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'Status added'}
            return Response(data, status=status.HTTP_201_CREATED)


class CommentStatusGET(APIView):
    permission_classes = (StatusAddPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, comment_id, status_slug):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_status = get_object_or_404(Status, slug=status_slug)
        try:
            stat_add = CommentStatus.objects.create(comment=comment, author=request.user.author, status=comment_status)
        except IntegrityError:
            stat_add = CommentStatus.objects.get(comment=comment, author=request.user.author,)
            data = {'message': f'You already added status'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'Status added'}
            return Response(data, status=status.HTTP_201_CREATED)
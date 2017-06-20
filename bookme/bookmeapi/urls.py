from django.conf.urls import url, include
from bookmeapi import views

urlpatterns = [
    url(r'books/$', views.BookListCreateView.as_view(), name='apibooks'),
    url(r'issues/$', views.IssueListCreateView.as_view(), name='api_issues'),
    url(r'users/$', views.UserListCreateView.as_view(), name='api_users'),
    url(r'issue-update/(?P<pk>[0-9]+)/$', views.IssueUpdateView.as_view(),
        name='issue-update'),
    url(r'bookdetail/(?P<pk>[0-9]+)/$', views.BookDetail.as_view(),
        name='book-detail'),
    url(r'userdetail/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name='user-detail'),
]
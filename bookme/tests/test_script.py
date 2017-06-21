# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from bookmeapi.models import Book, Issue


class setUpModelInstanceTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            email='admin_user@test.com', first_name='User',
            last_name='Admin', password='pythonistainaction',
            username='user_admin', is_superuser=True)

        self.authUser = User.objects.create(
            email='auth_user@test.com', first_name='User',
            last_name='Auth', password='pythonistainaction', 
            username='user_auth', is_staff=False)

        self.book_1 = Book.objects.create(
            title='King Author',
            isbn='1234hjy',
            category='History'
        )

        self.book_2 = Book.objects.create(
            title='Desert Knights',
            isbn='1we232d',
            category='Action'
        )

        self.issue_1 = Issue.objects.create(
            book = self.book_1,
            user = self.authUser,
            approved = False
        )

        self.issue_2 = Issue.objects.create(
            book = self.book_2,
            user = self.admin,
            approved = False
        )

        super(setUpModelInstanceTestCase, self).setUp()


    def test_user_can_be_retrieved(self):
        url = reverse('api_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIsInstance(data, list)


class BookTestCase(setUpModelInstanceTestCase):
        pass


class IssueTestCase(setUpModelInstanceTestCase):
        pass


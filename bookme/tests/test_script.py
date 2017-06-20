# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from bookmeapi.models import Book, Issue


class UserTestCase(APITestCase):
    def setUp(self):
        User.objects.create(
            email='test.admin@test.com', first_name='Test', 
            last_name='Admin', password='random', 
            username='test.admin', is_staff=True)


        # User.objects.create(
        #     email='test.admin@test.com', first_name='Test', 
        #     last_name='Admin', password='random', 
        #     username='test.admin', is_staff=True)

        super(UserTestCase, self).setUp()

    
    def test_user_can_be_retrieved(self):
        url = reverse('api_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        data = response.data
        self.assertIsInstance(data, list)



class BookTestCase(APITestCase):
    def setUp(self):
        pass



class IssueTestCase(APITestCase):
    def setUp(self):
        pass


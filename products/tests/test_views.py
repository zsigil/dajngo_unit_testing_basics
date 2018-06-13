from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from products.views import productdetail

from django.test import RequestFactory
from mixer.backend.django import mixer
import pytest



@pytest.mark.django_db
class TestViews:

    def test_product_detail_authenticated(self):
        mixer.blend('products.Product')   #so pk will be 1
        path = reverse('detail', kwargs={'pk':1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)   #user is authenticated!

        response = productdetail(request, pk=1)
        assert response.status_code == 200

    def test_product_detail_unauthenticated(self):
        mixer.blend('products.Product')   #so pk will be 1
        path = reverse('detail', kwargs={'pk':1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()  #not authenticated

        response = productdetail(request, pk=1)
        #assert response.status_code != 200
        assert 'accounts/login' in response.url

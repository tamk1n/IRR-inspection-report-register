from django.test import TestCase, Client
from base_user.models import MyUser
from django.urls import reverse
# Create your tests here.

class LoginViewTestCase(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(username='example', password='exmpsw')
        self.login_url = reverse('irr_app:user-login')
        return super().setUp()
        
    def test_correct_data(self):
        data = {
            'username': self.user.username,
            'password': self.user.password
        }
        c = Client()
        response = c.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)


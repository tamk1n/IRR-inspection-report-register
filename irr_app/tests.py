from django.test import TestCase, Client
from base_user.models import MyUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus
# Create your tests here.


class LoginViewTestCase(TestCase):
    """
    It is used to test login and authentication problem
    Run this command:
    python manage.py test irr_app.tests.LoginViewTestCase
    """
    def setUp(self):
        User = get_user_model()
        self.password = 'exmpsw'
        self.url = reverse('irr_app:user-login')
        self.user = User.objects.create_user(username='example', password=self.password)
    
    def test_wrong_credentials(self):
        """
        It is used to check how login function behaves successfull login.
        Run this command:
        python manage.py test irr_app.tests.LoginViewTestCase.test_wrong_credentials
        """
        data = {
            'username': self.user.username,
            'password': 'wrong'
        }
        response = self.client.post(self.url, data)

        # gives 200 status code because error message appears
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_correct_data(self):
        """
        It is used to check how login function behaves successfull login.
        Run this command:
        python manage.py test irr_app.tests.LoginViewTestCase.test_correct_data
        """
        data = {
            'username': self.user.username,
            'password': self.password
        }
        response = self.client.post(self.url, data)

        # gives 302 status code because redirect to home page
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


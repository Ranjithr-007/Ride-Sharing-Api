from rest_framework.test import APITestCase,force_authenticate
from django.urls import reverse
from rest_framework import status
from .models import Users,Rides
from django.contrib.auth.hashers import make_password

class UserSignupViewSetTests(APITestCase):
    def test_user_signup_success(self):
        url = reverse('usersignup')  # Assuming you have defined a proper URL name for this viewset
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '9645610883',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_signup_validation_error(self):
        url = reverse('usersignup')  # Assuming 'usersignup' is the name you've given to the URL
        # Missing 'confirm_password' field intentionally to trigger validation error
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '9234567890',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DriverSignupViewSetTests(APITestCase):
    def test_driver_signup_success(self):
        url = reverse('ridersignup')  # Assuming you have defined a proper URL name for this viewset
        data = {
            "username": "abhijith",
            "email": "abhijith@gmail.com",
            "phone_number": "7845121289",
            "password": "abhijith@123",
            "confirm_password": "abhijith@123",
            "vehicle_number":"kl02be8203"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_driver_signup_validation_error(self):
        url = reverse('ridersignup')  # Assuming 'usersignup' is the name you've given to the URL
        # Missing 'confirm_password' field intentionally to trigger validation error
        data = {
            "username": "abhijith",
            "email": "abhijith@gmail.com",
            "phone_number": "7845121289",
            "password": "abhijith@123",
            "vehicle_number":"kl02be8203"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginViewSetTests(APITestCase):
    def test_user_login_success(self):
        hashed_password = make_password('testpassword')
        Users.objects.create(email='test@example.com', password=hashed_password, is_user=True)
        url = reverse('userlogin')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['message'], 'User logged in successfully')
    def test_user_login_error(self):
        hashed_password = make_password('testpassword')
        Users.objects.create(email='test@example.com', password=hashed_password, is_user=True)
        url = reverse('userlogin')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword1'
        }
        response = self.client.post(url, data, format='json')
        # if response.status_code != status.HTTP_200_OK:
        #     print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DriverLoginViewSetTests(APITestCase):
    def test_driver_login_success(self):
        hashed_password = make_password('testpassword')
        Users.objects.create(email='test@example.com', password=hashed_password, is_staff=True)
        url = reverse('riderlogin')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['message'], 'Driver logged in successfully')
    def test_driver_login_error(self):
        hashed_password = make_password('testpassword')
        Users.objects.create(email='test@example.com', password=hashed_password, is_staff=True)
        url = reverse('riderlogin')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword1'
        }
        response = self.client.post(url, data, format='json')
        # if response.status_code != status.HTTP_200_OK:
        #     print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DriverListTests(APITestCase):
    def setUp(self):
        self.driver1 = Users.objects.create(email='driver1@example.com', is_staff=True)
        self.driver2 = Users.objects.create(email='driver2@example.com', is_staff=True)
        self.user = Users.objects.create(email='user@example.com', is_user=True)
    
    def test_list_drivers(self):
        url = reverse('driverlist')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        # if response.status_code != status.HTTP_200_OK:
        #     print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookingViewSetTests(APITestCase):
    def setUp(self):
        self.user = Users.objects.create(username='testuser', email='user@example.com', password='userpassword',is_user=True)
        self.driver = Users.objects.create(username='testdriver', email='driver@example.com', password='driverpassword',is_staff=True)
        
    def test_create_ride_success(self):
        url = reverse('booking')
        data = {
            'driver': 2,
            'pickup_location': 'TestPickup',
            'dropoff_location': 'TestDropoff'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class NewRidesViewSetTests(APITestCase):
    def setUp(self):
        self.driver = Users.objects.create(username='testdriver', email='driver@example.com', password='testpassword',is_staff=True)
        
    def test_list_new_rides_success(self):
        url = reverse('newrides') 
        self.client.force_authenticate(user=self.driver)
        response = self.client.get(url)
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NewRidesViewSetTests(APITestCase):
    def setUp(self):
        self.user = Users.objects.create(username='testuser', email='user@example.com', password='userpassword',is_user=True)
        self.driver = Users.objects.create(username='testdriver', email='driver@example.com', password='driverpassword',is_staff=True)
        self.test_ride = Rides.objects.create(rider=self.user,driver=self.driver)

    def test_status_update_accept_success_accept(self):
        url = reverse('newrides')
        self.client.force_authenticate(user=self.driver)
        data = {'ride': self.test_ride.pk, 'status': 'accept'}
        response = self.client.patch(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_update_accept_success_reject(self):
        url = reverse('newrides')
        self.client.force_authenticate(user=self.driver)
        data = {'ride': self.test_ride.pk, 'status': 'reject'}
        response = self.client.patch(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RidesHistoryViewSetTests(APITestCase):
    def setUp(self):
        self.test_user = Users.objects.create_user(username='testuser', email='user@example.com', password='testpassword',is_user=True)
        self.test_driver = Users.objects.create_user(username='testdriver', email='driver@example.com', password='driverpassword',is_staff=True)
    def test_list_rides_history_success(self):
        url = reverse('ridehistory')
        self.client.force_authenticate(user=self.test_user)
        Rides.objects.create(rider=self.test_user,driver=self.test_driver, status='ongoing'),
        Rides.objects.create(rider=self.test_user,driver=self.test_driver, status='completed')
        response = self.client.get(url)
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CancelOrCompleteRidesViewSetTests(APITestCase):
    def setUp(self):
        self.test_user = Users.objects.create(username='testuser', email='user@example.com', password='testpassword',is_user=True)
        self.test_driver = Users.objects.create(username='testdriver', email='driver@example.com', password='testpassword',is_staff=True)
        self.test_ride = Rides.objects.create(rider=self.test_user,driver=self.test_driver, status='ongoing')

    def test_cancel_ride_cancel(self):
        url = reverse('cancelorcomplete')
        self.client.force_authenticate(user=self.test_driver)
        data = {'ride': self.test_ride.id, 'action': 'cancelled'}
        response = self.client.patch(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Ride cancelled successfully')

    def test_cancel_ride_complete(self):
        url = reverse('cancelorcomplete')
        self.client.force_authenticate(user=self.test_driver)
        data = {'ride': self.test_ride.id, 'action': 'completed'}
        response = self.client.patch(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Ride completed successfully')
    
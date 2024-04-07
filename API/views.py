from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import viewsets
from . import serializers
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .import models
from .import permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

class sample(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        return Response({"message": "it is a POST method"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response({"message": "it is a GET method"}, status=status.HTTP_200_OK)
    
class UserSignupViewSet(viewsets.ViewSet):
    @swagger_auto_schema(operation_summary='User can register by giving the details (username,email,phone_number,password,confirm_password)')
    def create(self, request):
        serializer = serializers.UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DriverSignupViewSet(viewsets.ViewSet):
    @swagger_auto_schema(operation_summary='Driver can register by providing the details (username,email,phone_number,password,confirm_password,vehicle_number)')
    def create(self, request):
        serializer = serializers.DriverSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Driver registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginViewSet(viewsets.ViewSet):
    serializer_class = serializers.UserLoginSerializer
    @swagger_auto_schema(operation_summary='User can login by providing the details (email,password)')
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        response = {
            'message': 'User logged in successfully',
            'access': str(tokens.access_token),
            'refresh': str(tokens)
        }
        return Response(data=response, status=status.HTTP_200_OK)
    
class DriverLoginViewSet(viewsets.ViewSet):
    serializer_class = serializers.DriverLoginSerializer
    @swagger_auto_schema(operation_summary='Driver can login by providing the details (email,password)')
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        response = {
            'message': 'Driver logged in successfully',
            'access': str(tokens.access_token),
            'refresh': str(tokens)
        }
        return Response(data=response, status=status.HTTP_200_OK)

class DriverList(viewsets.ViewSet):
    permission_classes = [permissions.IsUser]
    @swagger_auto_schema(operation_summary='The users can view the list of Drivers registered here.')
    def list(self,request):
        drivers = models.Users.objects.filter(is_staff=True).all()
        serializer = serializers.DriverListSerializer(instance=drivers,many=True)
        return Response(serializer.data)
    
class Booking(viewsets.ViewSet):
    permission_classes = [permissions.IsUser]
    @swagger_auto_schema(operation_summary='User can book the Riders by providing the details (driver,pickup_location,dropoff_location)') 
    def create(self,request):
        serializer=serializers.RideSerializer(data=request.data)
        if serializer.is_valid():
            driver_id = serializer.validated_data.get('driver')
            rider_id = request.user.id
            if not models.Users.objects.filter(id=driver_id.id, is_staff=True).exists():
                return Response({'error': 'The driver ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            elif models.Rides.objects.filter(driver=driver_id,status='ongoing').exists():
                return Response({'error':'The driver is on a ride, please book another driver'})
            elif models.Rides.objects.filter(Q(rider=rider_id) & (Q(status='ongoing') | Q(status='waiting'))).exists():
                return Response({'error':'You already have a booking, first complete it'})
            serializer.save(rider=request.user)  # Set the rider to the authenticated user
            driver = models.Users.objects.get(id=serializer.data['driver'])
            response = {
                'driver':driver.username,
                'vehicle_number':driver.vehicle_number,
                'pickup_location':serializer.data['pickup_location'],
                'dropoff_location':serializer.data['dropoff_location']
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NewRides(viewsets.ViewSet):
    permission_classes = [permissions.IsDriver]
    @swagger_auto_schema(operation_summary='List of all the new rides which were having status waiting') 
    def list(self,request):
        current_user = request.user
        rides = models.Rides.objects.filter(driver=current_user,status='waiting').all()
        serializer = serializers.NewRideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_summary='Driver can either accept it or reject it by providing the details (status)')
    def status_update(self,request):
        # Retrieve the ride instance to update
        try:
            ride = models.Rides.objects.get(pk=request.data['ride'], driver=request.user, status='waiting')
        except models.Rides.DoesNotExist:
            return Response({'error': 'Ride not found or not available for update'}, status=status.HTTP_404_NOT_FOUND)
        # Update the status of the ride based on the request data
        if 'status' in request.data:
            status_data = request.data['status']
            if status_data == 'accept':
                ride.status = 'ongoing'
                ride.save()
                return Response({'message': 'Ride accepted successfully'}, status=status.HTTP_200_OK)
            elif status_data == 'reject':
                ride.status = 'rejected'
                ride.save()
                return Response({'message': 'Ride rejected successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Status field is required'}, status=status.HTTP_400_BAD_REQUEST)

class RidesHistory(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_summary='History of the rides except the waiting one.') 
    def list(self,request):
        current_user = request.user
        rides = models.Rides.objects.exclude(driver=current_user, status='waiting').all()
        serializer = serializers.RideHistorySerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CancelOrCompleteRides(viewsets.ViewSet):
    permission_classes = [permissions.IsDriver]
    @swagger_auto_schema(operation_summary='Driver can either cancel or complete the ride by provide the details (rideid,status)') 
    def update(self,request):
        current_user = request.user
        ride_id = request.data.get('ride')
        # Fetch the ride object
        current_ride = models.Rides.objects.filter(id=ride_id, driver=current_user, status='ongoing').first()
        if current_ride:
            # Update the status based on request data
            action = request.data.get('action')
            if action == 'cancelled':
                current_ride.status = 'cancelled'
            elif action == 'completed':
                current_ride.status = 'completed'
            current_ride.save()
            # Return success response
            return Response({'message': f'Ride {action} successfully'}, status=status.HTTP_200_OK)
        else:
            # Ride not found or not in 'ongoing' status
            return Response({'error': 'Ride not found or not in ongoing status'}, status=status.HTTP_404_NOT_FOUND)

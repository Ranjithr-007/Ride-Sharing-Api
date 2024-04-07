from .import views
from django.urls import path
from rest_framework.routers import DefaultRouter

#it is one of the another method for handling the routers
# router = DefaultRouter()
# router.register(r'sample', views.sample, basename='sample1')
# urlpatterns = router.urls

urlpatterns = [
    #create and list methods implemented in your viewset and only mentioned it, your viewset will only handle POST and GET requests
    # path('', views.sample.as_view({'post': 'create', 'get': 'list'}), name='sample'),
    path('user/signup',views.UserSignupViewSet.as_view({'post':'create'}),name='usersignup'),
    path('user/login',views.UserLoginViewSet.as_view({'post':'login'}),name='userlogin'),
    path('rider/signup',views.DriverSignupViewSet.as_view({'post':'create'}),name='ridersignup'),
    path('rider/login',views.DriverLoginViewSet.as_view({'post':'login'}),name='riderlogin'),
    path('user/driverlist',views.DriverList.as_view({'get':'list'}),name='driverlist'),
    path('user/booking',views.Booking.as_view({'post':'create'}),name='booking'),
    path('rider/newrides',views.NewRides.as_view({'get':'list','patch':'status_update'}),name='newrides'),
    path('ridehistory',views.RidesHistory.as_view({'get':'list'}),name='ridehistory'),
    path('rider/cancelorcomplete',views.CancelOrCompleteRides.as_view({'patch':'update'}),name='cancelorcomplete')
]

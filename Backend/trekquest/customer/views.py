from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
# Create your views here.


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *   
from .models import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import logout

#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]  #specifying rendereres class to serialize data in user defined way
    
    def post (self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)  
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token = get_tokens_for_user(user)
            print("done")
            return Response({'token':token,'msg':'Registration successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
from django.contrib.auth import login

class UserLoginView(APIView):
    renderer_classes=[UserRenderer] #specifying rendereres class to serialize data in user defined way

    def post (self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email , password=password)
            print(user)
            if user is not None :  
                login(request, user)   
                user.save()             
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'login successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_error':['Email or Password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication



def UserLogoutView(request):
    logout(request)
    return redirect('/home/customer-login/')
    
class TourAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication] 
    def get(self, request):
        tours = Tour.objects.all()
        serializer = TourSerializer(tours, many=True)
        return render(request,'h1.html',{'tours':tours})
    
class AllTourAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication] 
    def get(self, request):
        tours = Tour.objects.all()
        serializer = TourSerializer(tours, many=True)
        return render(request,'alltour.html',{'tours':tours})

class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication] 
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, card_id):
        tour = get_object_or_404(Tour, pk=card_id)

        # cpollecting data from the form
        review_text = request.POST.get('reviewText')
        rating = request.POST.get('rating')

        # Getting logged-in user
        user = request.user

        # Create a new review
        review = Review.objects.create(
            tour=tour,
            useremail=user,
            reviewText=review_text,
            rating=rating
        )

        return HttpResponseRedirect('/customer/tours/{0}/'.format(card_id))

class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication] 
    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     request_data = request.data.copy()
    #     request_data.pop('price', None)

    #     serializer = BookingSerializer(data=request_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request, tour_id):
        tour = get_object_or_404(Tour, pk=tour_id)

        # cpollecting data from the form
        

        # Getting logged-in user
        user = request.user

        # Create a new review
        booking = Booking.objects.create(
            tour=tour,
            guest_name = request.POST.get('guest_name'),
            guest_email = user,
            guest_phone= request.POST.get('guest_phone'),
            guest_size = request.POST.get('guest_size'),
            booking_date = request.POST.get('booking_date'),
        )
        
        # return HttpResponseRedirect('/customer/tours/{0}/'.format(tour_id))
        return render(request,'thankyou.html',{'booking':booking})
        

    
class TourDetailView(APIView):
    def get(self, request, card_id):
        try:
            tour = get_object_or_404(Tour,pk=card_id)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found"}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = Review.objects.filter(tour=tour)
        return render(request,'detail.html',{'tour':tour,'reviews': reviews}) 

def booking_form(request,card_id):
    
    tour = get_object_or_404(Tour,pk=card_id)
    return render(request,'booking.html',{'tour':tour})

def about(request):
    return render(request,'about.html')


class SearchDetailView(APIView):
    def post(self, request):
        try:
            # tour = get_object_or_404(Tour)
            searchTerm = request.POST.get('location')
            if searchTerm:
                tour = Tour.objects.filter(title__icontains=searchTerm)
                if tour:
                    return render(request, 'tours.html',{'searchTerm':searchTerm,'tours': tour})
                else:
                    searchTerm='No such tour is currently avaliable,Check out our other tours'
                    tour = Tour.objects.all()
                    return render(request, 'tours.html',{'searchTerm':searchTerm,'tours': tour})
        
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found"}, status=status.HTTP_404_NOT_FOUND)
        
    

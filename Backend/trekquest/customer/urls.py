from customer import views
from django.urls import path
urlpatterns = [
    
    path('register/', views.UserRegistrationView.as_view(),name='register'),
    path('login/', views.UserLoginView.as_view(),name='login'),
    # path('profile/', views.UserProfileView.as_view(),name='profile'),
    path('logout/', views.UserLogoutView, name='logout'),
    path('tours/',views.TourAPIView.as_view(),name='tour-api'),
    path('alltour/',views.AllTourAPIView.as_view(),name='all-tour'),
    path('reviews/',views.ReviewAPIView.as_view(), name='review-list-create'),
    path('booking/<int:tour_id>/submit_booking/',views.BookingAPIView.as_view(),name='booking'),
    path('tours/<int:card_id>/',views.TourDetailView.as_view(), name='tour-detail'),
    path('tours/<int:card_id>/submit_review/', views.ReviewAPIView.as_view(), name='submit-review'),
    path('booking_tour/<int:card_id>/',views.booking_form,name='book-tour'),
    path('about/',views.about,name='about'),
    path('search/tour/',views.SearchDetailView.as_view(),name='search-tour'),
    
]
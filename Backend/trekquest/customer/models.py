from django.db import models
from decimal import Decimal
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,name,tc ,password=None,password2=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,tc,password=None):
        user = self.create_user(
            email,
            name=name,
            tc=tc,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc=models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


class Tour(models.Model):
    title = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    distance = models.FloatField()
    photo = models.ImageField(upload_to='tour/images/')
    desc = models.TextField()
    price = models.IntegerField()
    max_group_size = models.IntegerField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    useremail = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewText = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.tour.title} by {self.useremail}"

@receiver(post_save, sender=Review)
def update_tour_average_rating(sender, instance, **kwargs):
    tour = instance.tour  # Use the 'tour' ForeignKey relationship
    reviews = Review.objects.filter(tour=tour)  # Filter by the 'tour' ForeignKey
    total_rating = sum(reviews.values_list('rating', flat=True))
    average_rating = total_rating / reviews.count() if reviews.count() > 0 else 0
    tour.average_rating = average_rating
    tour.save()
    

class Booking(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_email = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_phone=models.CharField(max_length=10)
    guest_size=models.IntegerField()
    booking_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.tour.title} by {self.guest_name}"

    def save(self, *args, **kwargs):
        # Calculate the price based on the associated tour's price and guest size
        self.price = Decimal(self.tour.price) * Decimal(self.guest_size)
        super().save(*args, **kwargs)


from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'
    
    # def ready(self):
    #     import customer.signals  # Replace 'your_app_name' with your actual app name

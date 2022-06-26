from django.urls import path
from . import views

urlpatterns = [
    path('imports', views.add_data),
    path('delete/<uuid>', views.delete_data),
    path('nodes/<uuid>', views.get_data),
]
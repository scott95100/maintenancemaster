from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('machines/', views.machines_index, name='machines'),
    path('machines/<int:machine_id>/', views.machines_show, name='machines_show'),
    path('machines/create/', views.machines_new, name='machines_create'),
    path('machines/<int:pk>/update/', views.machines_update, name='machines_update'),
    path('machines/<int:pk>/delete/', views.MachineDelete.as_view(), name='machines_delete'),
    path('machines/<int:pk>/add_maintenance/', views.add_maintenance, name='add_maintenance'),
    path('accounts/signup', views.sign_up, name='sign_up'),

]
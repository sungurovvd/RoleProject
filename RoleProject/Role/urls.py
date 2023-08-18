from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('user/', UserList.as_view(), name = 'user'),
    path('user/<int:pk>', AddRoleToUser.as_view(), name = 'add_role_to_user'),
    path('role/', RoleList.as_view(), name = 'roles'),
    path('role/<int:pk>', ChangeStatus.as_view(), name = 'change_status'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_role/', CreateRole.as_view(), name = 'create_role'),

]
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
    path('role/create', CreateRole.as_view(), name = 'create_role'),
    path('user/create', views.create_user, name='create_user'),
    path('server/', ServerList.as_view(), name='all_servers'),
    path('server/create/', CreateServer.as_view(), name='create_server'),
    path('server/<int:pk>', RolesOnServer.as_view(), name='roles_on_server')

]
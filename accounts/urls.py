from django.urls import path, include
from django.conf import settings
from accounts import views
from .views import site_login,site_logout,site_signup , complete_profile

app_name = 'accounts'
urlpatterns = [
    #login
    path('login/', site_login, name = 'login'),
    #logout
    path('logout/', site_logout, name = 'logout'),
    #signup
    path('signup/', site_signup, name = 'signup'),
    path('complete-profile/', complete_profile , name='complete_profile'),
]


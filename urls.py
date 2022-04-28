"""DatabaseProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Scheduler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view()),
    path('login/', views.Login.as_view()),
    path('createuser/', views.CreateUser.as_view()),
    path('createcourse/', views.CreateCourse.as_view()),
    path('assignTAToCourse/<str:coursename>', views.AssignTAToCourse.as_view(), name='assign-TA-course'),
    path('assignTAToCourse/', views.AssignTAToCourse.as_view()),
    path('createlab/<str:coursename>', views.CreateLab.as_view(), name='create-lab'),
    path('createlab/', views.CreateLab.as_view()),
    path('profile/<str:userEmail>', views.UserProfile.as_view()),
    path('editprofile/', views.EditProfile.as_view()),
    path('editprofile/<str:userEmail>', views.EditProfile.as_view(), name='edit-profile'),
    path('logout/', views.SignOut.as_view()),
    path('userdirectory/', views.UserDirectory.as_view()),
    path('editcourse/', views.EditCourse.as_view()),
    path('editcourse/<str:coursename>', views.EditCourse.as_view(), name='edit-course'),
    path('permissiondenied/', views.PermissionDenied.as_view())
]

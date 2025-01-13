"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
path("",views.index,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("course",views.course,name="course"),
    path("register",views.register,name="register"),
    path("6",views.home,name="fayyas"),
    path("employeregister",views.employregidter,name="employeregister"),
    path("test",views.test,name="test"),
    path("userhome/<usname>",views.userhome,name="userhome"),
    path('logout',views.logout,name="logout"),
    path("profile/<usname>",views.profile,name="profile"),
    path("editprofile/<usname>",views.editpro,name="editprofile"),
    path("employeehome/<usname>",views.employeehome,name="employeehome"),
    path("adminhome/<usname>",views.adminhome,name="adminhome"),
    path('slotbooking/<usname>/<stname>/<emplnme>',views.slotbooking,name="slotbooking"),
    path('employeeappoint/<usname>/<stname>',views.employeeapooint,name="employeeappoint"),
    path('appointment/<usname>/<stdata>/<employee>',views.appointment,name="appointment"),
    path("changepass/<usname>", views.changepass, name="changepass"),
    path("createslot/<usname>", views.createslot, name="createslot"),
    path("joinslot/<usname>", views.joinslot, name="joinslot"),
    path("myslot/<usname>", views.myslot, name="myslot"),
    path("stdelete/<usname>/<stname>/<emponame>", views.stdelete, name="stdelete"),
    path("stemdelete/<usname>/<stname>/<emponame>", views.stemdelete, name="stemdelete"),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('search/<usname>', views.search, name='search'),
    path('employee_search/<usname>/<stname>', views.employee_search, name='employee_search'),
    path("empodelete/<usname>/<employe>",views.empodelte,name="empodelete"),
    path('refund_form/<id>', views.refund_form, name='refund_form'),
    path('refund_request/<id>/', views.refund_request, name='refund_request'),
    path('payment_page/<id>/', views.payment_page, name='payment_page'),
    path('payment_callback/<id>/', views.payment_callback, name='payment_callback'),
    path('success_page/<id>/', views.success_page, name='success_page'),
    # path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

from django.contrib import admin
from django.urls import path
from goobusinessesapp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("searching", views.searching, name='searching'),
    path("freetrail", views.freetrail, name='freetrail'),
    path("servicepage/<str:slag>/<int:slID>", views.servicepage, name='servicepage'),
    path("ordercontinue", views.ordercontinue, name='ordercontinue'),
    path("ordersuccessfull", views.ordersuccessfull, name='ordersuccessfull'),
    path("about", views.about, name='about'),
    path("ordertraking/<str:email>/<str:phone>/<int:otp>/<int:slID>", views.ordertraking, name='ordertraking'),
    path("freetrialcheck", views.freetrialcheck, name='freetrialcheck'),
    path("successfulysendunderhumanreview", views.successfulysendunderhumanreview, name='successfulysendunderhumanreview'),
    path("contact", views.contact, name='contact'),
    path("whyus", views.whyus, name='whyus'),
    path("emailseen/<str:email>/<str:msgtitle>", views.emailseen, name='emailseen'),
    path("openvia/<str:email>/<str:opentype>/<str:openmessage>", views.openvia, name='openvia'),
    path("unsubscribe/<str:email>", views.unsubscribe, name='unsubscribe'),
    path("subscribe/<str:email>", views.subscribe, name='subscribe'),
    path("timeck", views.timeck, name='timeck'),
    path("hire", views.registationform, name='registationform'),
    path("registationcontinue", views.registationcontinue, name='registationcontinue'),
    path("registationsuccessfull", views.registationsuccessfull, name='registationsuccessfull'),
    path("login", views.Login, name='login'),
    path("loginsuccess", views.loginsuccess, name='loginsuccess'),
    path("dashboard", views.dashboard, name='dashboard'),
    path("newadminmanagingdashboard", views.newadminmanagingdashboard, name='newadminmanagingdashboard'),
    path("userbatchandemailrequest", views.userbatchandemailrequest, name='userbatchandemailrequest'),
    path("notlogin/<int:startnum>", views.notlogin, name='notlogin'),
    path("contactdata", views.contactdata, name='contactdata'),
    path("resentuserbatchandemailrequest", views.resentuserbatchandemailrequest, name='resentuserbatchandemailrequest'),
    path("offerletter/<str:email>/<str:batchname>/<str:empid>", views.offerletter, name='offerletter'),
############## 5th Feb 2024 ################
    path("termsandconditions", views.termsandconditions, name='termsandconditions'),
    path("CancellationRefundPolicy", views.CancellationRefundPolicy, name='CancellationRefundPolicy'),
    path("courses", views.courses, name='courses'),
    path("privacypolicy", views.privacypolicy, name='privacypolicy'),
    path("paymentVaryfyForInt", views.paymentVaryfyForInt, name='paymentVaryfyForInt'),
    path("paymentRejectForEmp", views.paymentRejectForEmp, name='paymentRejectForEmp'),
    path("intrnpaymentrequest", views.intrnpaymentrequest, name='intrnpaymentrequest'),


    
]

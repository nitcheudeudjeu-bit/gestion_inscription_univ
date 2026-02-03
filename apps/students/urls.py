from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('register/', views.student_register, name='student_register'),
    path('register/success/', views.registration_success, name='registration_success'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),

    # Dashboard & profil
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('edit/', views.edit_student_profile, name='edit_student_profile'),

    # PDF confirmation
    path('confirmation/pdf/', views.student_confirmation_pdf, name='student_confirmation_pdf'),

    # Paiement
    path('payment/', views.student_payment, name='student_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]


from django.urls import path,include
from .views import register,user_login,user_logout,profile_view,edit_profile
# to use auth_views.PasswordResetView we are importing auth_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    # path('',include('django.contrib.auth.urls')),
    path("register/",register,name='register'),
    path("login/",user_login,name='login'),
    path("logout/",user_logout,name='logout'),
    path("profile/<str:username>/", profile_view, name="profile"),
    path('edit-profile/', edit_profile, name='edit_profile'),

    # password reset related links
    # PasswordResetView is a class, not a function.it contains all the logic to: Display the forgot password form, Accept the email, Generate reset tokens, Send reset emails.
    # Django URLs expect a function.but here PasswordResetView is a class, so we cannot use it directly,because Django expects a callable view.
    # here as_view() converts a class into a view function.which django can use.
    # as_view() is used with Class-Based Views (CBVs). It converts a class into a callable view function that Django can use in URL patterns.

    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ),
    name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]

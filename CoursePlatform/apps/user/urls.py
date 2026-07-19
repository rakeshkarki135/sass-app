from django.urls import path
from apps.user.views import register
from django.contrib.auth import views as auth_view


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", auth_view.LoginView.as_view(next_page="course_list"), name="login"),
    path("logout/", auth_view.LogoutView.as_view(next_page="login"), name="logout"),
    path("password-reset/", auth_view.PasswordResetView.as_view(),
         name="password_reset"),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_view.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/", auth_view.PasswordResetCompleteView.as_view(),
         name="reset_done"),
    path("password-change/", auth_view.PasswordChangeView.as_view(),
         name="password_change"),
    path("password-change/done/", auth_view.PasswordChangeDoneView.as_view(),
         name="password_change_done"),

]

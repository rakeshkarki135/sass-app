from django.urls import path
from apps.payment.views import (
    initiate_khalti,
    verify_khalti_payment,
    initialize_esewa,
)


urlpatterns = [
    # khalti url
    path("", initiate_khalti, name="initiate_khalti"),
    # path("khalti", khalti_payment, name="khalti_payment"),
    path("verify/<int:course_id>", verify_khalti_payment, name="verify"),
    path("esewa", initialize_esewa, name="esewa_initialize"),
]

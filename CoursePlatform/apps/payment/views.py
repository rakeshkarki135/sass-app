from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.course.models import Course
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

import os
import uuid
import json
import hmac
import base64
import hashlib
import requests
load_dotenv()


@login_required
def khalti_payment(request):
    id = uuid.uuid4()

    context = {
        "uuid": id
    }
    return render(request, "payment_create_form.html", context)


@login_required
def initiate_khalti(request):
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    if request.method == "POST":
        return_url = request.POST.get("return_url")
        amount = request.POST.get("amount")

    purchase_order_id = str(uuid.uuid4())
    user = request.user

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": user.username,
            "email": user.email,
            "phone": "9800000001"
        }
    })
    headers = {
        'Authorization': f"Key {os.getenv("KHALTI_LIVE_SECRET_KEY")}",
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = json.loads(response.text)
    return redirect(json_response["payment_url"])


@login_required
def verify_khalti_payment(request, course_id):

    url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get("pidx")

    headers = {
        'Authorization': f"Key {os.getenv("KHALTI_LIVE_SECRET_KEY")}",
        'Content-Type': 'application/json',
    }

    payload = json.dumps({
        "pidx": pidx
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = json.loads(response.text)

    if json_response["status"] == "Completed":
        course = get_object_or_404(Course, pk=course_id)
        # for many to many field use set(), add() and clear(), remove()
        course.subscribers.add(request.user.id)
        course.save()
        messages.info(request, "Payment Successful")
    else:
        print(json_response)
        messages.error(request, "Payment Failed, Try again later")

    return redirect("course_list")


def initialize_esewa(request):
    hmac_sha256 = hmac.new(settings.DJANGO_SECRET_KEY, message, hashlib.sha256)

    digest = hmac_sha256.digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return render(request, "esewa.html")

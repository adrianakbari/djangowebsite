from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import EmailSignupForm
from .models import Signup

import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=MAILCHIMP_EMAIL_LIST_ID
)


def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()


def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed")
            else:
                subscribe(form.instance.email)
                form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'about.html')


def resume(request):
    filters = {
        "skip": 0, "limit": 30, "individual": "Enterprise System Design Associate 10.5", "country": [
            "CHE", "SWE", "ESP", "SVN", "SVK", "ROU", "PRT", "NOR", "NLD", "MLT", "LUX", "LTU", "LVA", "ITA", "ISL", "HUN", "GRC", "DEU", "FRA", "FIN", "EST", "DNK", "CZE", "HRV", "BEL"], "certification": [], "version": [], "sort": {"FullName": 1}
    }
    params = {
        'filter': json.dumps(filters)
    }
    eu = requests.get(
        'https://www.esri.com/training/TechnicalCertification/Directory/Search/', params=params)
    euJson = json.loads(eu.text)
    # print('eu count is: {0}'.format(euJson['count']))
    filters = {
        "skip": 0, "limit": 30, "individual": "Enterprise System Design Associate 10.5", "country": [
            "USA"], "certification": [], "version": [], "sort": {"FullName": 1}
    }
    params = {
        'filter': json.dumps(filters)
    }
    us = requests.get(
        'https://www.esri.com/training/TechnicalCertification/Directory/Search/', params=params)
    usJson = json.loads(us.text)
    # print('us is: {0}'.format(usJson['count']))
    context = {
        'euCount': euJson['count'],
        'usCount': usJson['count']
    }
    return render(request, 'resume.html', context)

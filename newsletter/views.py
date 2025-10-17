from django.shortcuts import render, redirect
from .models import Subscriber


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Subscriber.objects.get_or_create(email=email)
            return redirect('newsletter:subscribe')
    return render(request, 'newsletter/subscribe.html')

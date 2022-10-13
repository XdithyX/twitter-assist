from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from .models import User
from .twitter_bot import download_file
#index page
def index(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).count()!=0:
            if User.objects.filter(email=email, password=password).count() ==1:
                request.session['email'] = email
                return redirect('dashboard')
            return render(request, 'index.html', {'error': 'wpwd'})
        return render(request, 'index.html', {'error': 'wemail'})
    return render(request, 'index.html')
#signup page
def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('fullname')
        twitterid = request.POST.get('twitterid')
        password = request.POST.get('password')
        user = User(email=email, name=name, twitterid=twitterid, password=password)
        user.save()
        return redirect('index')
    return render(request, 'signup.html')
#dashboard page
def dashboard(request):
    user = User.objects.get(email=request.session['email'])
    return render(request, 'dashboard.html', {'user' : user})
#download page
def download(request):
    user = User.objects.get(email=request.session['email'])
    filename = user.twitterid + '.txt'
    file_path = os.path.join(settings.TWEETS_ROOT, filename)
    download_file(twitterid=user.twitterid, filepath=file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = "attachment; filename=%s" % 'tweets.txt'
            return response
    raise Http404
#layout page
def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('index')

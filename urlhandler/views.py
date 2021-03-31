from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shortenurl
import random,string
# Create your views here.

@login_required(login_url = '/login/')
def dashboard(request):
    usr = request.user
    urls = shortenurl.objects.filter(user = usr)
    return render(request, 'dashboard.html', { 'urls' : urls })

def randomgen():
    return ''.join(random.choices(string.ascii_lowercase + string.digit) for _ in range(6))

@login_required(login_url = '/login/')
def generate(request):
    if request.method == "POST":
        # generate 
        pass
        if request.POST['original'] and request.POST['short']:
            # generate based on user input
            usr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shortenurl.objects.filter(short_query = short)
            if not check:
                newurl = shortenurl(
                    user = usr,
                    original_url = original,
                    short_query = short,
                )
                newurl.save()
                return redirect(dashboard)
            else:
                messages.error(request, "409 : Shortcode already in use" )
                return redirect(dashboard)
        elif request.POST['original']:
            # generate randomly
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shortenurl.objects.filter(short_query = short)
                if not check:
                    newurl = shortenurl(
                        user = usr,
                        original_url = original,
                        short_query = short,
                    )
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue
        else:
            messages.error(request, "400 : URL not present")
            return redirect(dashboard)
        if request.POST['original'] and request.POST['short']:
            # generate based on user input
            usr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shortenurl.objects.filter(short_query = short)
            if not check:
                newurl = shortenurl(
                    user = usr,
                    original_url = original,
                    short_query = short,
                )
                newurl.save()
                return redirect(dashboard)
            else:
                messages.error(request, "412 : The provided shortcode is Invalid" )
                return redirect(dashboard)
        
    else:
        return redirect('/dashboard')

def home(request, query= None):
    if not query or query is None:
        return render(request, 'home.html')
    else:
        try:
            check = shortenurl.objects.get(short_query = query)
            check.visits = check.visits + 1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except shortenurl.UrlNotPresent:
            return render(request, 'home.html', { 'error' : "error" })
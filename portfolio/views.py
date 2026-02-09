from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import ContactForm
from django.contrib import messages


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("OK")
        else:
            return HttpResponse("Form validation failed", status=400)
    else:
        form = ContactForm()
    project = Project.objects.first()
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    service = Service.objects.all()
    portfolio= PortfolioItem.objects.all()
    return render(request, 'home.html', {'project': project, 'profile': profile, 'skills': skills, 'service': service, 'form': form,'portfolio':portfolio})
def portfolio_details(request, pk):
    profile = Profile.objects.first()
    item = get_object_or_404(PortfolioItem, pk=pk)
    images= item.images.all() #images related name from PortfolioImage model
    return render(request, 'portfolio_details.html', {'profile':profile,'item': item, 'images': images})




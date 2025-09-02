from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form=form.save()
            # بعد الحفظ ابعتي نسخة على الإيميل
            send_mail(
                subject=f"رسالة جديدة من {form.name}: {form.subject}",
                message=f"الاسم: {form.name}\nالبريد: {form.email}\n\n{form.message}",
                from_email="eali56167@gmail.com",  # أو سيبيها نفس الإيميل بتاعك
                recipient_list=["eali56167@gmail.com"],  # إيميلك
                fail_silently=False,
            )

            messages.success(
                request, "✅ Your message has been sent successfully!")
            # Redirect to a success page or the same page
            # return redirect('home')
            return HttpResponse("OK") # Temporary response for AJAX
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




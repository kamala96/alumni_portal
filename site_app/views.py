from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # sliders = Slider.objects.order_by('-created_at')[:7]
    # sliders = Slider.objects.filter(is_active=True).order_by('-created_at')
    # accounting_officer = AccountingOfficer.load()

    context = {
    }
    return render(request, 'index.html', context)

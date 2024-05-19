from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import *
# Create your views here.

def Home(request):
    return redirect('/receipe/')

def handleReceipe(request):
    if request.method == 'GET':
        queryset = Receipe.objects.all()
        context = {'receipes': queryset}
        return render(request, 'receipe.html', context)
    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')
        Receipe.objects.create(receipe_name=receipe_name, receipe_description=receipe_description, receipe_image=receipe_image)
        queryset = Receipe.objects.all()
        return render(request, 'receipe.html', context={'receipes': queryset})
    else:
        pass


def deleteReceipe(request, id):
    try:
        receipe = get_object_or_404(Receipe, id=id)
        receipe.delete()
        return redirect('/receipe/')
    except Http404:
        return render(request, 'error.html', {'messages': 'Record not found'})

def editReceipe(request, id):
    if request.method == 'GET':
        try:
            receipe = get_object_or_404(Receipe, id=id)
            return render(request, 'editreceipe.html', context={'receipe': receipe})
        except Http404:
            return render(request, 'error.html', {'messages': 'Receipe not found'})
    if request.method == 'POST':
        try:
            queryset = get_object_or_404(Receipe, id=id)
            data = request.POST
            receipe_name = data.get('receipe_name')
            receipe_description = data.get('receipe_description')
            receipe_image = request.FILES.get('receipe_image')
            
            queryset.receipe_name = receipe_name
            queryset.receipe_description = receipe_description

            if receipe_image:
                queryset.receipe_image = receipe_image
            queryset.save()
            return redirect('/receipe/')
        except Http404:
             return render(request, 'error.html', {'messages': 'Unable to update. Please try again!!'})
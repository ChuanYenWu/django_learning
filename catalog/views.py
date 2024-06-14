from django.shortcuts import render

# Create your views here.
import datetime
from .models import LunchboxModel, BuyingModel
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import BuyingModelForm, CheckOrderForm
from django.core.paginator import Paginator

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    #num_books = Book.objects.all().count()
    num_lunchbox = LunchboxModel.objects.all().count()
    num_buying = BuyingModel.objects.all().count()

    #jpbooks = Book.objects.filter(language__name__contains='japanese').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_lunchbox': num_lunchbox,
        'num_buying': num_buying,

        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class LunchboxListView(generic.ListView):
    model = LunchboxModel
    paginate_by = 10

class LunchboxDetailView(generic.DetailView):
    model = LunchboxModel

#https://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
@method_decorator(staff_member_required(login_url='login'), name='dispatch') #dispatch & Decorate
class BuyingListView(generic.ListView):
    model = BuyingModel
    paginate_by = 10

def neworder(request):
    #book_instance = get_object_or_404(BookInstance, pk=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = BuyingModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            order = BuyingModel(
                customer_name= form.cleaned_data['customer_name'],
                customer_phone= form.cleaned_data['customer_phone'],
                meat_num= form.cleaned_data['meat_num'],
                vege_num= form.cleaned_data['vege_num'],
                total_cost= form.cleaned_data['vege_num']* LunchboxModel.objects.get(lunchbox_name='素食便當').lunchbox_cost
                            +form.cleaned_data['meat_num']* LunchboxModel.objects.get(lunchbox_name='葷食便當').lunchbox_cost,
                buytime=datetime.date.today()
            )
            order.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        #proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BuyingModelForm(initial={'meat_num': 0, 'vege_num': 0})

    context = {
        'form': form,
    }

    return render(request, 'catalog/neworder.html', context)

def checkorder(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CheckOrderForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            
            request.session['phone_number'] = form.cleaned_data['phone']

            return HttpResponseRedirect(reverse('order_result'))
            
            # redirect to a new URL:

    # If this is a GET (or any other method) create the default form.
    else:
        
        form = CheckOrderForm()    

    context = {
        'form': form,
    }

    return render(request, 'catalog/checkorder.html', context)

def order_result(request):
    phone_number = request.session['phone_number']
    orderlist=BuyingModel.objects.filter(customer_phone=phone_number).order_by('-buytime')

    paginator = Paginator(orderlist, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #orderlist=page_obj

    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        #'orderlist': orderlist,
    }

    return render(request, 'catalog/order_result.html', context)
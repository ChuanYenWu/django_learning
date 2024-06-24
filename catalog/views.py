from django.shortcuts import render

# Create your views here.
import datetime
from .models import LunchboxModel, BuyingModel
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import BuyingModelForm, CheckOrderForm, UpdateForm_staff, UpdateForm_customer
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import BooleanField, Case, When, Value, F

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
            #return HttpResponseRedirect(reverse('index'))
            # 從 POST 資料中取得 'next' 參數的值，如果沒有(會取得空字串)則預設為 'index'
            next_url = request.POST.get('next') or 'index'  
            #return HttpResponseRedirect(reverse(next_url))
            #使用redirect可以接受相對路徑和urls.py的名稱, 不需要reverse
            return redirect(next_url)

    # If this is a GET (or any other method) create the default form.
    else:
        #proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BuyingModelForm(initial={'meat_num': 0, 'vege_num': 0})

    #在context中傳輸'next': request.GET.get('next')) 或直接在template中索取request.GET.next
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
    orderlist=BuyingModel.objects.filter(customer_phone=phone_number).order_by('-id')
    #latest_uuid = orderlist.latest('id').uuid
    if orderlist:
        three_days_ago = datetime.date.today() - datetime.timedelta(days=3)

        orderlist = orderlist.annotate(
            intime=Case(
                When(buytime__gte=three_days_ago, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

    paginator = Paginator(orderlist, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #orderlist=page_obj

    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        #'orderlist': orderlist,
        #'latest_uuid': latest_uuid,
    }

    return render(request, 'catalog/order_result.html', context)


#若使用UpdateView, 可由form_valid（super）方法和form.instance來修改價格（不可人為修改的部份）
@staff_member_required(login_url='login')
def update_orderview_staff(request, uuid):
    order = get_object_or_404(BuyingModel, uuid=uuid)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UpdateForm_staff(request.POST, instance=order)

        # Check if the form is valid:
        if form.is_valid():

            #if order.buytime != datetime.date.today():
            #    raise ValidationError(_('已過期，不可修改'))
            #else:
                order.customer_name = form.cleaned_data['customer_name']
                order.customer_phone = form.cleaned_data['customer_phone']
                order.meat_num = form.cleaned_data['meat_num']
                order.vege_num = form.cleaned_data['vege_num']
                order.total_cost = form.cleaned_data['vege_num']* LunchboxModel.objects.get(lunchbox_name='素食便當').lunchbox_cost \
                                +form.cleaned_data['meat_num']* LunchboxModel.objects.get(lunchbox_name='葷食便當').lunchbox_cost
                order.save()

                #return HttpResponseRedirect(reverse('orderlist'))
                next_url = request.POST.get('next') or 'orderlist'
                return redirect(next_url)
        
    else:
        form = UpdateForm_staff(
            initial={
                'customer_name': order.customer_name, 
                'customer_phone': order.customer_phone, 
                'meat_num': order.meat_num, 
                'vege_num': order.vege_num
            }
        )
    context = {
        'form': form,
        'order': order,
    }

    return render(request, 'catalog/update_order_staff.html', context)

@staff_member_required(login_url='login')
def delete_orderview_staff(request, uuid):
    order = get_object_or_404(BuyingModel, uuid=uuid)

    if request.method == 'POST':
        order.delete()
        return redirect('orderlist')
    return render(request, 'catalog/order_confirm_delete.html', {'order': order})

def update_orderview_customer(request, uuid):
    order = get_object_or_404(BuyingModel, uuid=uuid)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        #form = UpdateForm_customer(request.POST, instance=order)
        form = UpdateForm_customer(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            
            if order.buytime < datetime.date.today() - datetime.timedelta(days=3):
                form.add_error(None, ValidationError(_('已過期，不可修改')))
            #if order.buytime != datetime.date.today():
            #    raise ValidationError(_('已過期，不可修改'))
            else:
                order.customer_name = form.cleaned_data['customer_name']
                order.customer_phone = form.cleaned_data['customer_phone']
                order.meat_num = form.cleaned_data['meat_num']
                order.vege_num = form.cleaned_data['vege_num']
                order.total_cost = form.cleaned_data['vege_num']* LunchboxModel.objects.get(lunchbox_name='素食便當').lunchbox_cost \
                                +form.cleaned_data['meat_num']* LunchboxModel.objects.get(lunchbox_name='葷食便當').lunchbox_cost
                order.save()
            # request.session['phone_number'] should still exist
                return HttpResponseRedirect(reverse('order_result'))
        
    else:
        form = UpdateForm_customer(
            initial={
                'customer_name': order.customer_name, 
                'customer_phone': order.customer_phone, 
                'meat_num': order.meat_num, 
                'vege_num': order.vege_num
            }
        )
    context = {
        'form': form,
        'order': order,
    }
    
    # seems OK to use same template with staff version
    return render(request, 'catalog/update_order_staff.html', context)
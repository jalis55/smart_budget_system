from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Budgets,Costs
from django.contrib import messages
from main_app.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
#import re
import datetime
from time import gmtime, strftime
import csv
import json
from django.core import serializers
import pytesseract
from PIL import Image
#from datefinder import find_dates


def home(request):
	return render(request,'index.html')
# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('user_dashboard')
        else:
        	messages.success(request, "Invalid username or password")
        	return redirect('login')
            #return HttpResponse("Username or password incorrect")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def user_dashboard(request):
	id=request.user.id

	if request.method=="POST":
		#return HttpResponse(request.user.id)
		budget=Budgets(
			user_id=id,
			budget_name=request.POST["budget_name"],
			total_budget=request.POST["total_budget"],
			)
		budget.save()
	budget=Budgets.objects.filter(user_id=id).order_by("-budget_id")
	context={
        
        'budgets':budget,
    }

	return render(request,'admin pages/admin_home.html',context)
@login_required
def manage_budget(request,id):
    budget=Budgets.objects.get(budget_id=id)
    costs=Costs.objects.filter(budget_id=id)
    total_cost=0
    for c in costs:
        total_cost=total_cost+c.cost
    total_budget=budget.total_budget
    rem_budget=total_budget-total_cost
    half_budget=int((50/100)*total_budget)
    third_quater_budget=int((75/100)*total_budget)



    date=datetime.datetime.now()

    if request.method=="POST" and 'form1' in request.POST:
        cost=Costs(
            date=date,
            purpose=request.POST["purpose"],
            cost=request.POST["cost"],
            budget_id=id,
        )
        cost.save()
        messages.success(request, "Successfully added")
        return redirect('manage_budget',id=id)
    if request.method=="POST" and 'form2' in request.POST:
        purpose=request.POST["purpose"]
        memo=request.FILES['image']
        img = Image.open(memo)
        result = pytesseract.image_to_string(img)
        #matches = list(datefinder.find_dates(result))

        # if len(matches) > 0:
        #
        #     date = matches[0]
        #     print(date)
        # else:
        #     print('No dates found')

        ix = result.find('TOTAL')

        # ix = ix + 6
        # price = result[ix] + result[ix + 1] + result[ix + 2] + result[ix + 3]

        return HttpResponse(result[ix])




        #return HttpResponse(purpose)
    context={
        "total_budget":total_budget,
        "rem_budget":rem_budget,
        "h_budget":half_budget,
        "tq_budget":third_quater_budget,
    }
    return render(request,'admin pages/manage_budget.html',context)
@login_required
def view_budget_details(request,id):

    costs=Costs.objects.filter(budget_id=id)
    budget = Budgets.objects.get(budget_id=id)

    file_name='static/csvFiles/details_budget_id='+str(id)+'.csv'

    csv_file = open(file_name, 'w')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['cost', 'purpose', 'date'])

    total=0

    for c in costs:

        csv_writer.writerow([c.cost,c.purpose,c.date])
        total=total+c.cost
    costs=list(costs)
    context={
        "costs":costs,
        "total":total,
        "file_name":file_name,
        "budget_name":budget.budget_name,
        "total_budget":budget.total_budget,

    }


    return render(request, 'admin pages/view_budget_details.html',context)

def delete_budget(request,id):
    budget=Budgets.objects.get(budget_id=id)
    budget.delete()
    return redirect('user_dashboard')


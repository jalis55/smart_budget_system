from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Budgets,Costs
from django.contrib import messages
from main_app.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
import re
import datetime
from time import gmtime, strftime





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

    if request.method=="POST":
        cost=Costs(
            date=date,
            purpose=request.POST["purpose"],
            cost=request.POST["cost"],
            budget_id=id,
        )
        cost.save()
        messages.success(request, "Successfully added")
        return redirect('manage_budget',id=id)
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
    total=0
    for c in costs:
        total=total+c.cost
    context={
        "costs":costs,
        "total":total,
    }
    return render(request, 'admin pages/view_budget_details.html',context)

def delete_budget(request,id):
    budget=Budgets.objects.get(budget_id=id)
    budget.delete()
    return redirect('user_dashboard')


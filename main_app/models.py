from django.db import models
import datetime

# Create your models here.
class Budgets(models.Model):
    budget_id = models.AutoField(null=False,primary_key=True)
    user_id = models.IntegerField(null=False)
    budget_name=models.CharField(null=False,max_length=200)
    total_budget=models.IntegerField(null=False)

    def __str__(self):
        return self.budget_name
        
class Costs(models.Model):
    cost_id=models.AutoField(null=False,primary_key=True)
    purpose=models.CharField(null=False,max_length=200)
    cost=models.IntegerField(null=False)
    date = models.DateField(default=datetime.date.today)
    budget_id = models.IntegerField(null=False)

    def __str__(self):
        return self.purpose
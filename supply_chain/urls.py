from django.urls import path
from .import budget

app_name = 'supplychain'

urlpatterns = [
    path('annual/budget/list/',budget.annualbudget,name='annualbudget-list'),
    path('annual/budget/list/new/',budget.add_annualbudget,name='add-annualbudget'),
    path('annual/budget/list/<str:budget_id>',budget.edit_annualbudget,name='update-annualbudget'),

]
from .models import *
from random import randint, randrange

def check_active_accounting_year():
    try:
        ff = Fiscal_year.objects.all().order_by('id').last()
        if ff is None :
            res = "NO ACCOUNT"
            return res
        elif ff.status == "In Active" or ff.status == "Open":
            res = "CLOSE"
            return res
        else:
            res = "OPEN"
            return res

    except Fiscal_year.DoesNotExist:
        res = "NO ACCOUNT"
        return res
        

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end) 
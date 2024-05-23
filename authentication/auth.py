# from msilib.schema import Error
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .forms import UserGroupForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .upload_thread import *
import pandas as pd
from tablib import Dataset
from django.core.files.storage import FileSystemStorage
from appsystem.models import *
from company.models import Sub_Devision
import os
# from django.views.decorators.cache import cache_page

def error_404_view(request, exception):
    form = UserLoginForm()
    if request.method == 'POST':
        # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
           email = form.cleaned_data.get('email')
            # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
           password = form.cleaned_data.get('password')
            # re-authenticate the username and password and store it into variable called user
           user = authenticate(username=email, password=password)
           print(user)
           if user is not None:
               login(request, user)
               if user.is_authenticated and user.is_active and not user.is_new:
                    messages.success(request, 'Login Successful')
                    return redirect('dashboard')
               elif user.is_authenticated and user.is_active and user.is_new:
                    return redirect("authentication:change-password")
               elif user.is_authenticated and not user.is_active:
                    messages.info(request, 'User Account Deactivated')
                # redirect the user to the managers
                    return redirect("authentication:login")
            #    elif user.is_authenticated and not user.devision.tenant_id.status:
            #         messages.info(request, 'User Institutuin Deactivated')
            #         return redirect("authentication:login")
           else:
                            
                messages.info(request, 'Username or Password is incorrect')
                # redirect the user to the managers
                return redirect("authentication:login")


    context = {
        'form': form,  # context is the form itself
    }
    template = '404.html'
    # data = {"name": "ThePythonDjango.com"}
    return render(request, template, context)

def login_view(request):
   
    form = UserLoginForm()
    if request.method == 'POST':
        # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
           email = form.cleaned_data.get('email')
            # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
           password = form.cleaned_data.get('password')
            # re-authenticate the username and password and store it into variable called user
           user = authenticate(username=email, password=password)
           print(user)
           if user is not None:
               login(request, user)
               if user.is_authenticated and user.is_active and not user.is_new:
                    messages.success(request, 'Login Successful')
                    return redirect('dashboard')
               elif user.is_authenticated and user.is_active and user.is_new:
                    return redirect("authentication:change-password")
               elif user.is_authenticated and not user.is_active:
                    messages.info(request, 'User Account Deactivated')
                # redirect the user to the managers
                    return redirect("authentication:login")
            #    elif user.is_authenticated and not user.devision.tenant_id.status:
            #         messages.info(request, 'User Institutuin Deactivated')
            #         return redirect("authentication:login")
           else:
                            
                messages.info(request, 'Username or Password is incorrect')
                # redirect the user to the managers
                return redirect("authentication:login")


    context = {
        'form': form,  # context is the form itself
    }
    template = 'authentication/auth-login.html'
    return render(request, template, context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def usergroups(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group_list = Group.objects.all()
    template = 'authentication/groups.html'
    context = {
        'group_list': group_list,
        'heading': 'List of Groups',
        'pageview': 'Groups',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user',raise_exception = True)
def add_usergroups(request):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            permissions = form.cleaned_data['permissions']
            name = form.cleaned_data['name']
            group = Group(name=name.title())
            group.save()
            group.permissions.set(permissions)
            messages.info(request,'Group Saved')
            return redirect('authentication:detail-group', group.id )
    else:
        form = UserGroupForm()

    template = 'authentication/creategroup.html'
    context = {
        'form':form,
        'heading': 'Group List',
        'pageview': 'New Group',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_update_user',raise_exception = True)
def edit_usergroups(request,group_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group_list = Group.objects.all().order_by('-id')
    group=Group.objects.get(id=group_id)
    if request.method == 'POST':
        form = UserGroupEditForm(request.POST,instance=group)
        if form.is_valid():
            group=form.save()
            messages.info(request,'Group Updated')
            return redirect('authentication:detail-group', group.id )
    else:
        form = UserGroupEditForm(instance=group)

    template = 'authentication/creategroup.html'
    context = {
        'form':form,
        'heading': 'List of Groups',
        'pageview': 'Update',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def delete_usergroups(request,group_id):
    group=Group.objects.get(id=group_id)
    group.delete()
    messages.error(request,'Group Deleted')
    return redirect('authentication:group-list')
   
@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def detail_usergroups(request,group_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    group=Group.objects.get(id=group_id)
    group_permissions = group.permissions.all()
    template = 'authentication/group-detail-view.html'
    context = {
        'group':group,
        'group_permissions':group_permissions,
        'heading': 'List of Groups',
        'pageview': 'Details'
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def users(request):

    if request.user.is_superuser:
        user_list = User.objects.all()
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        user_list = User.objects.filter(devision__tenant_id=request.user.devision.tenant_id.id)
    total_user = user_list.count()
    active_users = user_list.filter(is_active = True).count()
    inactive_users = user_list.filter(is_active = False).count()
    template = 'authentication/users.html'
    context = {
        'user_list': user_list,
        'total_user':total_user,
        'active_users':active_users,
        'inactive_users':inactive_users,
        'heading': 'List of Users',
        'pageview': 'USers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user',raise_exception = True)
def add_user(request):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST,request=request)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_new = True
            user.save()
            group = form.cleaned_data['group']
            permission_data = form.cleaned_data['user_permissions']
            user.groups.add(group)
            if permission_data is not None:
                for permissions in permission_data:
                    user.user_permissions.add(permissions)
            messages.info(request,'User Created')
            return redirect('authentication:user-list')
    else:
        form = CreateUserForm(request=request)
        user= request.user
    template = 'authentication/create-user.html'
    context = {
        'form':form,
        'heading': 'List Of Users',
        'pageview': 'New User',
        'app_model':app_model,
        
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_update_user',raise_exception = True)
def edit_user(request,user_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    user=User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST,instance=user,request=request)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            user.groups.clear()
            user.groups.add(group)
            user.user_permissions.clear()
            permission_data = form.cleaned_data['user_permissions']
            if permission_data is not None:
                user.user_permissions.clear()
                for permissions in permission_data:
                    user.user_permissions.add(permissions)
          
            
            messages.info(request,'User Updated')
            return redirect('authentication:detail-user', user.id)
    else:
        form = UpdateUserForm(request=request,instance=user)
        user=request.user

    template = 'authentication/update-user.html'
    context = {
        'form':form,
        'heading': 'List of Users',
        'pageview': 'Update',
        'app_model':app_model,

    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_update_user',raise_exception = True)
def user_edit_user(request,user_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    user=User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserUpdateUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.info(request,'User Updated')
            return redirect('authentication:detail-user', user.id)
    else:
        form = UserUpdateUserForm(instance=user)

    template = 'authentication/self-update.html'
    context = {
        'form':form,
        'heading': 'List of Users',
        'pageview': 'Update',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def delete_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    messages.error(request,'User Deleted')
    return redirect('authentication:user-list')


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def change_userstatus(request,user_id):
    user=User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    messages.info(request,'User Status Changed')
    return redirect('authentication:detail-user', user.id)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_user',raise_exception = True)
def detail_user(request,user_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    user=User.objects.get(id=user_id)
    # print(user_permission)
    template = 'authentication/user-detail-view.html'
    context = {
        'user':user,
        'heading': 'List of Users',
        'pageview': 'Details',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
def uploads_users(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()

            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)
            # Get the complete path to the uploaded file
            file_path = os.path.join(fs.location, filename)
            if os.path.exists(file_path):  # Check if the file exists
                empexceldata = pd.read_excel(file_path)
                dbframe = empexceldata
                UserThread(dbframe).start()
                messages.success(request,'User Data Upload Started')
                
            else:
                messages.error(request, 'File not found.')

            return redirect('authentication:user-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

@login_required(login_url='authentication:login')
def load_district(request):
    region_id = request.GET.get('devision')
    district = Sub_Devision.objects.filter(devision=region_id).order_by('name')
    return render(request, 'authentication/district_dropdown_list.html', {'district': district})

@login_required(login_url='authentication:login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            user.is_new = False
            user.save()
            update_session_auth_hash(request,user)
            return redirect('authentication:login')  # Redirect to a success page after password change
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'authentication/change-password.html', {'form': form})

@login_required(login_url='authentication:login')
def logout_request(request):
    logout(request)
    return redirect('authentication:login')

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_delete_user',raise_exception = True)
def reset_password(request,user_id):
    user=User.objects.get(id=user_id)
    cc = "password"
    password = make_password(cc)
    user.password=password
    user.is_new = True
    user.save()
    messages.error(request,'Password Reset Successful')
    return redirect('authentication:detail-user', user.id)
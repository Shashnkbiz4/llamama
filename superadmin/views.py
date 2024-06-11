from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request, 'superadmin/index.html')



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import ClientAdminCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

# @login_required
# @user_passes_test(lambda u: u.is_superadmin)
def create_client_admin_view(request):
    if request.method == 'POST':
        form = ClientAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superadmin:index')  # Redirect to the superadmin dashboard
        else:
            print(form.errors)
    else:
        form = ClientAdminCreationForm()
    return render(request, 'superadmin/createclient.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(user)
                if user.is_superadmin:
                    return redirect('superadmin:index')
                elif user.is_clientadmin:
                    return redirect('dashboard:index')
                else:
                    return redirect('user_dashboard')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'superadmin/login.html', {'form': form})
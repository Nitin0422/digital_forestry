from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import RegistrationForm, EmailAuthenticationForm, AccountInformationForm, LandInformationForm, SeedTreeForestInformationForm, ElectronicTreeForestInformationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import AccountInformation, LandInformation, SeedTreeForestInformation, Ward, LocalLevel, ElectronicTreesModel

# Create your views here.
def login_request(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main:home')
        else:
            print(form.errors)
    else:
        form = EmailAuthenticationForm(request)

    return render(request, 'signups/login.html', {'form': form})

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend= 'django.contrib.auth.backends.ModelBackend')
            return redirect('main:home')
        else:
            print(form.errors)
       
    else:
        form = RegistrationForm()

    return render(request, 'signups/registration.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/")
def home(request):
    return render(request, 'signups/home.html', {})

@login_required(login_url="/")
def account_information_form_view(request):
    user_instance = request.user
    try:
        account_information_instance = get_object_or_404(AccountInformation, user_id = user_instance.id)
        return redirect("main:account_information")
    except Exception as e:
        if request.method == "POST":
            form = AccountInformationForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user_id = user_instance.id
                account.save()
                return redirect("main:home")
        form = AccountInformationForm()
        return render(request, "main/accountform.html", {"form": form, "user": user_instance})

@login_required(login_url="/")
def account_information_view(request):
    user_instance = request.user

    try:
        account_information = get_object_or_404(AccountInformation, user_id = user_instance.id)
        return render(request, "main/accountinfo.html", {"account_information": account_information})
    except Exception as e:
        account_information = None
        return render(request, "main/accountinfo.html", {"account_information": account_information})

@login_required(login_url="/")
def edit_account_information(request):
    try:
        account_instance = get_object_or_404(AccountInformation, user_id = request.user.id)
        if request.method == "POST":
            form = AccountInformationForm(request.POST, instance=account_instance)
            if form.is_valid():
                form.save()
                return redirect('main:account_information')
        form = AccountInformationForm(instance=account_instance)
        return render(request, 'main/accountform.html', {"form":form})
    except Exception as e:
        return redirect('main:home')


@login_required(login_url="/")
def land_information_view(request):
    try:
        land_information_datas = get_list_or_404(LandInformation, user_id = request.user.id)
        return render(request, "main/landinfo.html", {"land_information_datas":land_information_datas})
    except Exception as e:
        land_information_datas = None
        return render(request, "main/landinfo.html", {"land_information_datas":land_information_datas})
    
@login_required(login_url="/")
def land_information_add(request):
    if request.method == "POST":
        form = LandInformationForm(request.POST)
        if form.is_valid():
            land_information_instance = form.save(commit=False)
            land_information_instance.user_id = request.user.id
            land_information_instance.save()
            return redirect("main:land_information")
        else:
            print(form.errors)
    form = LandInformationForm()
    return render(request, "main/landinfoform.html", {"form":form})

@login_required(login_url="/")
def land_information_edit(request, land_information_id):
    try:
        land_information_instance = get_object_or_404(LandInformation, pk=land_information_id)
        if request.method == "POST":
            form = LandInformationForm(request.POST, instance=land_information_instance)
            if form.is_valid():
                form.save()
                return redirect("main:land_information")
        form = LandInformationForm(instance=land_information_instance)
        return render(request, 'main/landinfoform.html', {"form":form})   
    except Exception as e:
        print(e)
        return render(request, "main/landinfo.html", {})

@login_required(login_url="/")
def land_information_delete(request, land_information_id):
    try:
        land_information_instance = get_object_or_404(LandInformation, pk = land_information_id)
        if request.method == "POST":
            land_information_instance.delete()
            return redirect("main:land_information")
        return render(request, "main/confirm.html", {})
    except Exception as e:
        return redirect("main:land_information")

@login_required(login_url="/")
def strs_information_view(request):
    try:
        user_id = request.user.id
        strs_information_datas = []
        land_instances = get_list_or_404(LandInformation, user_id= user_id)
        for land_instance in land_instances:
            forest_instance = get_object_or_404(SeedTreeForestInformation, land_id = land_instance.id)
            strs_information_datas.append(forest_instance)
        # strs_information_datas = get_list_or_404(SeedTreeForestInformation, user_id = request.user.id)
        return render(request, "main/strsview.html", {"strs_information_datas":strs_information_datas})
    except Exception as e:
        print(e)
        strs_information_datas = None
        return render(request, "main/strsview.html", {"strs_information_datas":strs_information_datas})

@login_required(login_url="/")
def strs_information_form(request):
    user = request.user.id
    print("User id from views is ", user)
    if request.method == "POST":
        form = SeedTreeForestInformationForm(request.POST, user_id = user)  
        if form.is_valid():
            form.save()
            return redirect('main:strs_information')
    form = SeedTreeForestInformationForm(user_id = user)
    return render(request, "main/strsform.html", {"form": form})

@login_required(login_url="/")
def strs_information_update(request, strs_information_id):
    try:
        user = request.user.id
        print(strs_information_id)
        strs_information_instance = get_object_or_404(SeedTreeForestInformation, pk = strs_information_id)
        if request.method == "POST":
            form = SeedTreeForestInformationForm(request.POST, instance=strs_information_instance, user_id = user)
            if form.is_valid():
                form.save()
                return redirect('main:strs_information')
        
        form = SeedTreeForestInformationForm(instance=strs_information_instance, user_id = user)
        return render(request, "main/strsform.html", {"form":form})
    except Exception as e:
        print(e)
        return redirect('main:strs_information')
    
@login_required(login_url="/")
def strs_information_delete(request, strs_information_id):
    try:
        strs_information_instance = get_object_or_404(SeedTreeForestInformation, pk = strs_information_id)
        source = "STRS"
        if request.method == "POST":
            strs_information_instance.delete()
            return redirect("main:strs_information")
        return render(request, "main/confirm.html", {"source": source})
    except Exception as e:
        return redirect("main:strs_information")
    

def load_local_level(request):
    province_id = request.GET.get('province')
    local_levels = LocalLevel.objects.filter(province_id = province_id)
    return render(request, "main/local_level_dd.html", {"local_levels": local_levels})

def load_ward(request):
    local_level_id = request.GET.get('local_level')
    wards = Ward.objects.filter(local_level_id = local_level_id)
    return render(request, "main/ward_dd.html", {"wards": wards})

@login_required(login_url='/')
def etrs_add(request):
    if request.method == 'POST':
        form = ElectronicTreeForestInformationForm(request.POST, user_id = request.user.id)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    form = ElectronicTreeForestInformationForm(user_id = request.user.id)
    return render(request, 'main/etrsform.html', {"form": form})

@login_required(login_url="/")
def etrs_view(request):
    try:
        user_id = request.user.id
        forest_information_datas = []
        land_instances = get_list_or_404(LandInformation, user_id= user_id)
        for land_instance in land_instances:
            forest_instance = get_object_or_404(ElectronicTreesModel, land_id = land_instance.id)
            forest_information_datas.append(forest_instance)
        return render(request, "main/etrsview.html", {"forest_information_datas":forest_information_datas})
    except Exception as e:
        print(e)
        forest_information_datas = None
        return render(request, "main/etrsview.html", {"forest_information_datas":forest_information_datas})
    
@login_required(login_url='/')
def etrs_update(request, etrs_information_id):
    try:
        user = request.user.id
        print(etrs_information_id)
        etrs_information_instance = get_object_or_404(ElectronicTreesModel, pk = etrs_information_id)
        if request.method == "POST":
            form = ElectronicTreeForestInformationForm(request.POST, instance=etrs_information_instance, user_id = user)
            if form.is_valid():
                form.save()
                return redirect('main:etrs_view')
        
        form = ElectronicTreeForestInformationForm(instance=etrs_information_instance, user_id = user)
        return render(request, "main/etrsform.html", {"form":form})
    except Exception as e:
        print(e)
        return redirect('main:etrs_view')

@login_required(login_url="/")
def etrs_delete(request, etrs_information_id):
    try:
        etrs_information_instance = get_object_or_404(ElectronicTreeForestInformationForm, pk = etrs_information_id)
        source = "ETRS"
        if request.method == "POST":
            etrs_information_instance.delete()
            return redirect("main:etrs_view")
        return render(request, "main/confirm.html", {"source": source})
    except Exception as e:
        return redirect("main:etrs_information")
    

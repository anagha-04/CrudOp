from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, ItemForm
from .models import Item

# Create your views here.
class RegisterView(View):
    
    def get(self, request):

        form = RegistrationForm()

        return render(request, 'register.html', {'form': form})

    def post(self, request):

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])

            user.save()

            return redirect('login')
        
        return render(request, 'register.html', {'form': form})

class LoginView(View):

    def get(self, request):

        form = LoginForm()

        return render(request, 'login.html', {'form': form})

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:

                login(request, user)

                return redirect('item_list')
            
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('login')
    

class ItemListView(View):

    def get(self, request):

        if not request.user.is_authenticated:

            return redirect('login')
        
        items = Item.objects.filter(user=request.user)

        return render(request, 'item_list.html', {'items': items})

class ItemCreateView(View):

    def get(self, request):

        if not request.user.is_authenticated:

            return redirect('login')
        
        form = ItemForm()

        return render(request, 'item_form.html', {'form': form})

    def post(self, request):

        if not request.user.is_authenticated:

            return redirect('login')
        
        form = ItemForm(request.POST)

        if form.is_valid():

            item = form.save(commit=False)

            item.user = request.user

            item.save()

            return redirect('item_list')
        
        return render(request, 'item_form.html', {'form': form})
    
class ItemUpdateView(View):

    def get(self, request, **kwargs):

        id = kwargs.get("pk")

        item = Item.objects.get(id=id)

        if item.user != request.user:

            return redirect("item_list")

        return render(request, "update_form.html", {"item": item})

    def post(self, request, **kwargs):

        id = kwargs.get("pk")

        item = Item.objects.get(id=id)

        if item.user != request.user:

            return redirect("item_list")

        item.title = request.POST.get("title")

        item.description = request.POST.get("description")

        item.save()

        return redirect("item_list")

class ItemDeleteView(View):

    def get(self, request, **kwargs):

        id = kwargs.get("pk")

        item = Item.objects.get(id=id)

        if item.user != request.user:

            return redirect("item_list")

        return render(request, "delete.html", {"item": item})

    def post(self, request, **kwargs):

        id = kwargs.get("pk")

        item = Item.objects.get(id=id)

        if item.user != request.user:

            return redirect("item_list")

        item.delete()
        
        return redirect("item_list")

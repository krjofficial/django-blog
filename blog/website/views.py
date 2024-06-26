from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Blog 
from .forms import SignUpForm, AddBlog


# Create your views here.
def home(request):

  blogs = Blog.objects.all()

  # Check to see if logging in 
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    # Check to see if user is valid (Authentication)
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('home')
    else:
      messages.error(request, 'Invalid username or password')
      return redirect('home')
  else:
    return render(request, 'home.html', {'blogs': blogs})



def logout_user(request):
  logout(request)
  messages.success(request, 'You are now logged out')
  return redirect('home')

def register_user(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        # if the form is valid, then it gets saved
        # Authenticate and login
        username = form.cleaned_data['username'] # gets the username from the form which was saved
        password = form.cleaned_data['password1']# gets the password from the form which was saved
        user = authenticate(username=username, password=password) # we need this variable for login function
        login(request, user)
        messages.success(request, "You are Successfully Registered")
        return redirect('home')
      
  else: 
    form = SignUpForm()
    return render(request, 'register.html', {'form': form}) 
  
  return render(request, 'register.html', {'form': form}) 


def user_blog(request, pk):
  #check if the user is logged in 
  if request.user.is_authenticated:
    #look up record
    user_blog = Blog.objects.get(id=pk)
    return render(request, 'blog.html', {'user_blog': user_blog})
  else:
    messages.success(request, "Please login to View this blog")
    return redirect('home')
  

def delete_blog(request, pk):
  if request.user.is_authenticated:
    delete_it = Blog.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "Blog deleted")
    return redirect('home')
  else:
    messages.success(request, "Login to Delete Blog")
    return redirect('home')
  


def add_blog(request):
  form = AddBlog(request.POST or None)
  if request.user.is_authenticated:
    if request.method == "POST":
      if form.is_valid():
        form.save()
        messages.success(request, "Blog Added")
        return redirect('home')
    return render(request, 'add_blog.html', {'form': form})
  else:
    messages.success(request, "Login to Add Blogs")
    return redirect('home')


def update_blog(request, pk):
  if request.user.is_authenticated:
    current_record = Blog.objects.get(id=pk)
    form = AddBlog(request.POST or None, instance=current_record) #Instance will initialize the form with the contents of current_record
    if form.is_valid():
      form.save()
      messages.success(request, "Blog has been Updated!")
      return redirect('home')
    return render(request, 'update_Blog.html', {'form': form})
  else: 
     messages.success(request, "Login to Update Records")
     return redirect('home')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Author
from .forms import SignUpForm, AddBlog


# Create your views here.
def home(request):

    blogs = Blog.objects.all()

    # Check to see if logging in
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Check to see if user is valid (Authentication)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")
    else:
        return render(request, "home.html", {"blogs": blogs})


def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect("home")


def register_user(request):
    if request.user.is_authenticated:
        return redirect("home") # redirect to home page if user is logged in


    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # if the form is valid, then it gets saved
            # Authenticate and login
            username = form.cleaned_data[
                "username"
            ]  # gets the username from the form which was saved
            password = form.cleaned_data[
                "password1"
            ]  # gets the password from the form which was saved
            user = authenticate(
                username=username, password=password
            )  # we need this variable for login function
            login(request, user)
            messages.success(request, "You are Successfully Registered")
            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def user_blog(request, pk):
  # look up blog
  user_blog = Blog.objects.get(id=pk)
  return render(request, "blog.html", {"user_blog": user_blog})

@login_required
def delete_blog(request, pk):
    current_blog = get_object_or_404(Blog, pk=pk)

    if request.user == current_blog.author:
      if request.user.is_authenticated:
          delete_it = Blog.objects.get(id=pk)
          delete_it.delete()
          messages.success(request, "Blog deleted")
          return redirect("home")
      else:
          messages.success(request, "Login to Delete Blog")
          user_blog = Blog.objects.get(id=pk)
          return render(request, "blog.html", {"user_blog": user_blog})
    else: 
      messages.error(request, "You are not authorized to delete this blog.")
      user_blog = Blog.objects.get(id=pk)
      return render(request, "blog.html", {"user_blog": user_blog})

@login_required
def add_blog(request):
    form = AddBlog(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                new_blog = form.save(commit=False)
                #  form.save(commit=False), you instruct Django not to save the object to the database yet. Instead, Django creates a model instance populated with the form data, but it remains in memory and not persisted to the database.
                new_blog.author = request.user
                new_blog.save()
                messages.success(request, "Blog Added")
                return redirect("home")
        return render(request, "add_blog.html", {"form": form})
    else:
        messages.success(request, "Login to Add Blogs")
        return redirect("home")


# Update Blog only if author is logged in
# An Author can only update their own blogs 

@login_required
def update_blog(request, pk):
    current_blog = get_object_or_404(Blog, pk=pk)

    # Check if the logged-in user is the author of the blog
    if request.user == current_blog.author:
        if request.method == 'POST':
            form = AddBlog(request.POST, instance=current_blog)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                messages.success(request, "Blog has been updated successfully.")
                user_blog = Blog.objects.get(id=pk)
                return render(request, "blog.html", {"user_blog": user_blog})  
        else:
            form = AddBlog(instance=current_blog)
        return render(request, "update_blog.html", {"form": form})
    else:
        messages.error(request, "You are not authorized to update this blog.")
        return redirect("home")  # Redirect to home 



# An Author can view thier own profile with their Password
# Anyone can view anyone's profile but not their password

def view_profile(request, pk):
  author = get_object_or_404(Author, pk=pk)
  return render(request, "view_profile.html", {"author": author})



# An Author can edit their profile with their Password and can't edit others profile
# def edit_profile

@login_required
def edit_profile(request, pk):
    current_author = get_object_or_404(Author, pk=pk)

    # Check if the logged-in user is the author of the blog
    if request.user == current_author:
        if request.method == 'POST':
            form = SignUpForm(request.POST, instance=current_author)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Profile has been updated successfully.")
                author = get_object_or_404(Author, pk=pk)
                return render(request, "view_profile.html", {"author": author})
        else:
            form = SignUpForm(instance=current_author)
        return render(request, "edit_profile.html", {"form": form})
    else:
        messages.error(request, "You are not authorized to update this profile.")
        return redirect("home")  # Redirect to home 



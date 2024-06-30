from .models import Author
from django.contrib.auth.models import User

def current_author(request):
  if request.user.is_authenticated:
    try:
      author = Author.objects.get(username=request.user)
      return { "current_author": author }
    except Author.DoesNotExist:
      return {}
  return {}
from django.contrib.auth.models import AbstractUser
from django.db import models

# Database Representation

# Blog Table:
# id (Primary Key)
# created_at
# title
# content
# author_id (Foreign Key to Author)


# Author Table:
# id (Primary Key)
# created_at
# username (from AbstractUser)
# password (from AbstractUser)
# email
# bio

class Author(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add automatically set to the current date and time when the object is first created. It is not updated on subsequent saves.
    email = models.EmailField(unique=True)
    # unique ensures that the value of the field must be unique across the entire table. No two rows can have the same value for this field.
    bio = models.TextField(blank=True)
    # blank+true  the field is allowed to be empty in forms, making it optional

    def __str__(self):
        return self.username
    
    # __str__  method is a special method that is called when you use the str() function on an instance of the class, or when you print the instance. It is intended to return a string representation of the object that is readable and useful for display purposes.

class Blog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey('website.Author', on_delete=models.CASCADE)
    # on_delete=models.CASCADE - when the referenced object (the one that is being pointed to by the foreign key) is deleted, all objects that reference it will also be deleted.  
    # When an author is deleted, all objects (Blogs) that reference it will also be deleted
    SearchableFields = ['author', 'title']
    FilterFields = ['author']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

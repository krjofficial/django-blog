from django.db import models

# Create your models here.
class Blog(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=50)
  content = models.CharField(max_length=500)
  author = models.CharField(max_length=50)
  SearchableFields = ['author', 'title']
  FilterFields = ['author']
  
  def __str__(self):
      return (f"{self.title} {self.author}")


  
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
        
        
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250) #SQL varchar
    slug = models.SlugField(max_length=250, unique_for_date='publish') #unique_for_date - this field be unique for the value of the date field
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') #related_name - allows to trace from related object back here in reverse
    body = models.TextField() #SQL text
    publish = models.DateTimeField(default=timezone.now) #date and time in a timezone; sorta version of Python's datetime.now but with timezones
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() # default manager - first declared manager is always the default one
    published = PublishedManager() # new manager defined above

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug]) #TODO: research this
    

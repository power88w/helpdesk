from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPost(models.Model):
    waiting = 'waiting'
    in_progress ='in progress'
    completed = 'completed'
    user = models.ForeignKey(User,related_name='f_author', default = 1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120,unique=True)
    content = models.TextField(null=True,blank=True)
    images = models.ImageField(null=True,blank=True)
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    posted_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    value = models.IntegerField(default=0)
    status_CHOICES = [
        (waiting, 'waiting'),
        (in_progress, 'in progress'),
        (completed, 'completed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=status_CHOICES,
        default=waiting,
    )
    priority_CHOICES = [
                        ("critical","critical"),
                        ("important","important"),
                        ("medium","medium"),
                        ]
    priority =  models.CharField(
        max_length=20,
        choices=priority_CHOICES,
        default="medium",
    )
    def __str__(self):
        return self.title

class BlogComment(models.Model):

    Comment = models.TextField(null = True, blank = True)
    user    = models.ForeignKey(User,related_name='f_poster',default =1,
              on_delete=models.CASCADE)
    Blog    = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    posted_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return ("Comment_"+str(self.Blog)+"_"+str(self.user))

class BlogStats(models.Model):

    user = models.ForeignKey(User,related_name='f_rater',default =1,
              on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    rating = models.IntegerField(default =0)
    views = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)+str(self.blog)
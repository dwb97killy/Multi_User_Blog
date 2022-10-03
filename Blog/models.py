from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class BlogContext(models.Model):
    publisher = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # 外键连接superuser
    title = models.CharField(max_length=256)
    tag = models.CharField(max_length=256)
    content = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)  # 创建时间
    publish_time = models.DateTimeField(blank=True, null=True)  # 发布时间
    modify_time = models.DateTimeField(blank=True, null=True)  # 修改时间
    approve_comments = models.BooleanField(default=True)  # 是否允许评论

    def __str__(self):
        return self.title

    def publish(self):
        self.publish_time = timezone.now()
        self.save()

    def modify(self):
        self.modify_time = timezone.now()
        self.save()

    def get_absolute_url(self):  # 获得每个blog的域名
        return reverse('blog_content', kwargs={'pk': self.pk})

    def approve(self):
        self.approve_comments = True
        self.save()

    def notapprove(self):
        self.approve_comments = False
        self.save()

    def count_comments(self):
        if self.approve_comments == True:
            return self.comments.filter(create_time__isnull=False)
        else:
            return self.comments.filter(create_time__isnull=True)

    def get_comments(self):
        return self.filter(approve_comments=True)  # 挑选出comment的blog



class Comments(models.Model):
    relatedblog = models.ForeignKey('Blog.BlogContext', on_delete=models.CASCADE, related_name='comments')  # 外键连接相关Blog
    publisher = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.publisher

    def get_absolute_url(self):  # 获得每个blog的域名
        return reverse('blog_content', kwargs={'pk': self.relatedblog})


class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    # Add any additional attributes you want
    # portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='static/profile_img', blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories')

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True,blank=True,upload_to='images/profile')
    website_url = models.URLField(max_length=255,null=True,blank=True)
    fb_url = models.URLField(max_length=255,null=True,blank=True)
    twitter_url = models.URLField(max_length=255,null=True,blank=True)
    insta_url = models.URLField(max_length=255,null=True,blank=True)
    pinterest_url = models.URLField(max_length=255,null=True,blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('show-profile',args=[self.pk])

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True,blank=True,upload_to='images/')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank=True,null=True)
    #body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True,)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,
                                 #default=Category.objects.get(name="Uncategorized")
                                 )
    snippet = models.CharField(max_length=255,default='Click the above link to read the blog post')
    likes = models.ManyToManyField(User,related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('article-detail',args=[self.pk])

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('article-detail',args=[Comment.objects.get(id=self.pk).post.id])

    def __str__(self):
        return '%s - %s' % (self.post.title,self.name)

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reply')
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('article-detail',args=[Reply.objects.get(id=self.pk).comment.post.id])

    def __str__(self):
        return '%s - %s' % (self.comment.post.title,self.name)
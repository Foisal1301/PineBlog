from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Category,Comment,Reply
from .forms import PostEditForm,PostForm,AddCategoryForm,AddCommentForm,AddReplyForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        posts = Post.objects.filter(title__contains=searched)
        categories = Category.objects.filter(name__contains=searched)
        return render(request,'search.html',{
            'users':users,
            'searched':searched,
            'posts':posts,
            'categories':categories,
            'cat_menu': Category.objects.all(),
        })

def delete_comment(request,post,com):
    comment = get_object_or_404(Comment,pk=com)
    comment.delete()
    return HttpResponseRedirect(reverse('article-detail',args=[str(post)]))

def delete_reply(request,post,repl):
    reply = get_object_or_404(Reply,id=repl)
    reply.delete()
    return HttpResponseRedirect(reverse('article-detail',args=[str(post)]))

def like_post(request,pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():#if request.user in post.likes.all()
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('article-detail',args=[str(pk)]))

def categories(request):
    return render(request,'categories.html',{'cat_menu':Category.objects.all()})

def CategoryView(request,cats):
    category_posts = Post.objects.filter(category=cats)
    cat_name = Category.objects.get(pk=cats)

    return render(request,'category.html',{
        "cats": cats,
        "posts": category_posts,
        "cat_name": cat_name,
        'cat_menu': Category.objects.all(),
    })

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-id']
    #ordering = ['-post_date']
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        context['admin'] = 'admin'
        return context

class ArticleView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super(ArticleView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        context['liked'] = liked
        context['total_likes'] = total_likes
        return context

class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(CreatePostView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

class AddCommentView(CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'add_comment.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCommentView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name_id = self.request.user.id
        return super().form_valid(form)

class AddReplyView(CreateView):
    model = Reply
    form_class = AddReplyForm
    template_name = 'add_reply.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddReplyView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

    def form_valid(self, form):
        form.instance.comment_id = self.kwargs['com']
        form.instance.name_id = self.request.user.id
        return super().form_valid(form)

class AddCategoryView(CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'add_category.html'
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

class EditPost(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = PostEditForm
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(EditPost,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

#class DeletePost(DeleteView):
#    model = Post
#    template_name = 'delete_post.html'
#    success_url = reverse_lazy('home')
#    def get_context_data(self, *args, **kwargs):
#        cat_menu = Category.objects.all()
#        context = super(DeletePost,self).get_context_data(*args, **kwargs)
#        context['cat_menu'] = cat_menu
#        return context

def delete_post(request,pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    messages.success(request,'Post is Deleted successfully!')
    return redirect('home')
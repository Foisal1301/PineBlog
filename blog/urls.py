from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('article/<int:pk>/',views.ArticleView.as_view(),name='article-detail'),
    #path('article/<int:pk>/',views.article_view,name='article-detail'),
    path('article/<int:pk>/comment/',views.AddCommentView.as_view(),name='add-comment'),
    path('article/<int:post>/comment/<int:com>/',views.AddReplyView.as_view(),name='add-reply'),
    path('article/delete_comment/<post>/<com>/',views.delete_comment,name='delete-comment'),
    path('article/delete_reply/<post>/<repl>/',views.delete_reply,name='delete-reply'),
    #path('article/edit_comment/<int:comment_pk>',views.EditComment.as_view(),name='edit-comment'),
    path("create_post/",views.CreatePostView.as_view(),name='create-post'),
    path("article/edit_post/<int:pk>/",views.EditPost.as_view(),name='edit-post'),
    path("article/delete/<int:pk>/",views.delete_post,name='delete-post'),
    path('add_category/',views.AddCategoryView.as_view(),name='add-category'),
    path('category/<str:cats>/',views.CategoryView,name='category'),
    path('category/',views.categories,name='categories'),
    path('like/<int:pk>/',views.like_post,name='like-post'),
    path('search/',views.search,name='search'),
    #path("add_comment_2/<int:pk>/",views.add_comment_2,name="add-comment-2")
]

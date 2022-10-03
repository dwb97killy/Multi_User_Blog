from Blog import views
from django.urls import path

urlpatterns = [
    path("", views.Post.as_view(), name='home_page'),
    path("about/", views.About.as_view(), name='blog_about'),
    path('blog/<int:pk>', views.Details.as_view(), name='blog_content'),  # 'blog_content'必须和model中的get_absolute_url一致
    path('blog/new_blog', views.CreateBlog.as_view(), name='new_blog'),
    path('blog/<int:pk>/update', views.UpdateBlog.as_view(), name='update_blog'),
    path('blog/<int:pk>/delete_blog', views.DeleteBlog.as_view(), name='delete_blog'),
    path('blog/draft_blog', views.DraftBlog.as_view(), name='draft_blog'),
    path('blog/<int:pk>/comment', views.add_comment, name='add_comment'),
    path('blog/<int:pk>/approve_comment', views.approve_comment, name='approve_comment'),
    path('blog/<int:pk>/notapprove_comment', views.notapprove_comment, name='notapprove_comment'),
    path('blog/<int:pk>/delete_comment', views.delete_comment, name='delete_comment'),
    path('blog/<int:pk>/publish', views.publish_blog, name='publish_blog'),
    path('register/', views.register, name='register'),
    path('accounts/<int:pk>/', views.user_profile, name='user_profile'),
]

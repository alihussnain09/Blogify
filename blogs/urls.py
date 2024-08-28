from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_page, name='register_page'),
    path('login/',views.login_page, name='login_page'),
    path('logout/', views.logout_page, name ='logout_page'),
    path('create/',views.create_blog, name='create_blog'),
    path('blogs/',views.blog_list,name='blog_list'),
    path('blog/<int:pk>',views.blog_detail,name='blog_detail'),
    path('blog/<int:pk>/delete',views.blog_delete,name='blog_delete'),
    path('blog/<int:pk>edit/',views.blog_edit,name='blog_edit'),
    path('category/<int:category_id>',views.blog_category,name='blog_category'),
    path('like/<int:pk>',views.blog_like,name='blog_like'),
    path('comment/<int:pk>/delete',views.delete_comment,name='delete_comment'),
    path('ajax/load-tags/', views.load_tags, name='ajax_load_tags'),
    path('dashboard',views.user_dashboard,name='user_dashboard'),
]

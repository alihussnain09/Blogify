from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogPostForm, CommentForm
from .models import blog_post, Category, Tag, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.core.paginator  import Paginator
from django.db.models import Q


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('login_page')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('blog_list')  
        else:
            messages.error(request, "Invalid Password")
            return redirect('login_page')
    
    return render(request, 'blogs/login.html')

def logout_page(request):
    logout(request)
    return redirect ('login_page')

def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "This username is already taken")
            return redirect('register_page')
        
        if any(char.isupper() for char in username):
            messages.error(request,"All Username letters must be lowercase")
            return redirect('register_page')
        
        if len(username)<6:
            messages.error(request, "Username must be at least 6 characters long")
            return redirect('register_page')
        
        if len(password)<6:
            messages.error(request, "Password should be at least 6 characters long")
            return redirect('register_page')
        
        
        user=User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        
        
        user.set_password(password)
        user.save()
        
        messages.success(request, "Account Created Successfully")
        return redirect('register_page')
    return render(request,'blogs/register.html')


@login_required(login_url="login_page")
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            form.save()
            form.save_m2m()
            return redirect('blog_list')
        return render(request, 'blogs/create_blog.html', {'form': form})
    
    else:
        form = BlogPostForm()
        
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blogs/create_blog.html', {'form': form,'categories':categories,'tags':tags})
    
    

def blog_list(request):
    blog_posts = blog_post.objects.all().order_by('date_posted')
    categories = Category.objects.all()
    tags = Tag.objects.all()

    selected_tags = request.GET.getlist('tags',[])
    query = request.GET.get('q','')
    
    if query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        blog_posts = blog_post.objects.all()
    
    if selected_tags:
        blog_posts = blog_posts.filter(tags__id__in=selected_tags).distinct()

        
    paginator = Paginator(blog_posts,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blogs/blog_list.html', {
        'blog_posts': blog_posts,
        'categories':categories,
        'query':query,
        'page_obj':page_obj,
        'tags':tags,
        'selected_tags':selected_tags,
        })

# @login_required(login_url="login_page")
def blog_detail(request, pk):
    try:
        blog = get_object_or_404(blog_post, pk=pk)
        comments = blog.comments.all()
        tags = blog.tags.all()

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.Author = request.user
                comment.save()
                return redirect('blog_detail', pk=pk)
        else:
            comment_form = CommentForm()

        return render(request, 'blogs/blog_detail.html', {
            'blog': blog,
            'comments': comments,
            'comment_form': comment_form,
            'tags': tags,
        })

    except Http404:
        messages.error(request, "Blog post not found.")
        return redirect('blog_list')

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('blog_list')

    
@login_required(login_url="login_page")
def blog_delete(request, pk):
    try:
        if request.method == 'POST':
            blog = get_object_or_404(blog_post, pk=pk)

            if blog.author != request.user:
                return HttpResponseForbidden("You are not allowed to delete this!")

            blog.delete()
            return redirect('blog_list')

        else:
            return redirect('blog_detail', pk=pk)

    except Http404:
        messages.error(request, "Blog post not found.")
        return redirect('blog_list')

    except Exception as e:
        messages.error(request, f"An error occurred while trying to delete the blog: {e}")
        return redirect('blog_detail', pk=pk)

    
@login_required(login_url="login_page")
def blog_edit(request, pk):
    blog = get_object_or_404(blog_post, pk=pk)
    if blog.author!= request.user:
        return HttpResponse("You are not allowed to edit this blog!")
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogPostForm(instance=blog)
        
    return render(request, 'blogs/blog_edit.html', {'form': form, 'blog': blog})


# @login_required(login_url="login_page")
def blog_category(request, category_id):
    category = get_object_or_404(Category,id= category_id)
    blogs = blog_post.objects.filter(category=category)
    return render(request,'blogs/blog_category.html',{'category': category, 'blogs':blogs})

@login_required(login_url="login_page")
def blog_like(request, pk):
    blog = get_object_or_404(blog_post, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('blog_detail',pk=pk)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if not User.is_authenticated:
        return HttpResponse("You are not allowed to delete this comment!")
    else:
        comment.delete()
        return redirect('blog_detail',pk=comment.blog.pk)

def load_tags(request):
    category_id = request.GET.get('category')
    tags = Tag.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(tags), safe=False)

@login_required
def user_dashboard(request):
    
    user_blogs = blog_post.objects.filter(author=request.user).order_by('-date_posted')
    user_comments = Comment.objects.filter(Author=request.user)
    
    return render(request,'blogs/user_dashboard.html',{
        'user_blogs':user_blogs,
        'user_comments': user_comments
    })
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from .forms import PostForm
from .models import Post
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core.exceptions import PermissionDenied


# creating a function to list out all the posts by a user 

# Home/post list
def post_list(request):
    query = request.GET.get('q', '')

    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    # 🔥 PAGINATION ADDED
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {
        'posts': page_obj,
        'query': query
    })

# in order to check the post in detail we are creating a seperate function
def post_detail(request,post_id):

    # get_object_or_404() is a Django shortcut function used to retrieve an object from the database. If the object doesn't exist, Django automatically returns a 404 Page Not Found
    #  error instead of crashing.
    
    post=get_object_or_404(Post,id=post_id)

    return render(request,'post_detail.html',{'post':post})

# create post
@login_required
def create_post(request):
    if request.method=="POST":
        form =PostForm(request.POST,request.FILES)

        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user 
            post.save()
            return redirect('blog:post_list')
    else:
        form =PostForm()
    return render(
        request,
        'create_post.html',
        {'form':form}
    )

# Edit post
@login_required
def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    # Authorization check 
    if request.user!=post.author:
        raise PermissionDenied
    
    if request.method=="POST":
        form=PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            updated_post=form.save(commit=False)
            updated_post.author=request.user

            updated_post.save()

            return redirect('blog:post_list')
    else:
        form=PostForm(instance=post)
    
    return render(
        request,
        'edit_post.html',
        {'form':form}
    )


# Delete post
@login_required
def delete_post(request,post_id):

    post=get_object_or_404(
        Post,
        id=post_id
    )

    # Authorization check 
    if request.user!=post.author:
        raise PermissionDenied
    post.delete()
    return redirect('blog:post_list')


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'my_posts.html', {'posts': posts})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('blog:post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

    return redirect('blog:post_detail', post_id=post.id)

@login_required
def dashboard(request):

    user_posts = Post.objects.filter(
        author=request.user
    )

    total_posts = user_posts.count()

    total_likes = Post.objects.filter(author=request.user).aggregate(
        total=Count('likes')
    )['total']

    total_comments = Post.objects.filter(author=request.user).aggregate(
        total=Count('comments')
    )['total']

    recent_posts = user_posts.order_by(
        '-created_at'
    )[:5]

    return render(
        request,
        'dashboard.html',
        {
            'total_posts': total_posts,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'recent_posts': recent_posts,
        }
    )
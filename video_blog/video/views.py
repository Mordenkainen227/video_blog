from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Category, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.core.files.storage import FileSystemStorage
import translit
from random import randint


# Create your views here.
def index(request):
    posts = Post.objects.filter(published=True).order_by('-date')[:9]
    featureds = Post.objects.filter(featured=True).order_by('-date')[:9]
    categories = Category.objects.all()
    context = {'posts': posts, 'featureds': featureds, 'categories': categories}
    return render(request, 'index.html', context)

def posts(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(published=True).order_by('-date')
    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    context = {'posts': posts, 'categories': categories}
    return render(request, 'posts.html', context)

def post_detail(request, slug):
    post = Post.objects.get(slug__exact=slug)
    return render(request, 'post_detail.html', {'post': post})

def category_detail(request, slug):
    category = Category.objects.get(slug__exact=slug)
    return render(request, 'category_detail.html', {'category': category})

def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Username or password is incorrect'
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')

def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile()
                profile.user = user
                profile.save()
                login(request, user)
                return redirect('index')
        else:
            form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    return redirect('index')
    
def create_post(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        new_slug = translit(request.POST.get('title'))
        if Post.objects.filter(slug__exact=new_slug).exists():
            post.slug = new_slug + '__' + str(timezone.now().format('Y-m-d_H-i-s')) + '__' + str(randint(1, 100))
        else:
            post.slug = new_slug
        if request.FILES.get('image', False) != False:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            post.preview = filename
            myfile = request.FILES['video']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            post.video = filename
        post.description = request.POST.get('description')
        category_ids = request.POST.getlist('categories[]')
        for id in category_ids:
                post.category.add(id)
        post.save()
        return redirect('index')
    return render(request, 'create_post.html', {'categories': categories})

def delete_post(request, slug):
    post = Post.objects.get(slug__exact=slug)
    post.delete()
    return redirect('index')

def profile(request, user_id):
    profile = Profile.objects.get(user_id__exact=request.user.id)
    return render(request, 'profile.html', {'profile': profile})
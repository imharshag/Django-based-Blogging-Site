from django.shortcuts import render, redirect
from .form import *
from .models import BlogModel
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('/')



def home(request):
    context = {'blogs': BlogModel.objects.order_by('-created_at')}
    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'see_blog.html', context)


def add_blog(request):
    context = {}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                image = form.cleaned_data['image'] 

                user = request.user
                blog_obj = BlogModel.objects.create(
                    user=user, title=title,
                    content=content, image=image
                )
                print(blog_obj)
                return redirect('/')  
        else:
            form = BlogForm()  

        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)


def blog_update(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(slug=slug)
        if blog_obj.user != request.user:
            return redirect('/')

        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=blog_obj) 
            if form.is_valid():
                form.save()
                # Set success message
                context['success_message'] = "Blog updated successfully!"
                # Redirect to home page or any other appropriate page after successful update
                return redirect('/')  
        else:
            form = BlogForm(instance=blog_obj)

        context['blog_obj'] = blog_obj
        context['form'] = form
    except BlogModel.DoesNotExist:
        context['error_message'] = "Blog does not exist"
    except Exception as e:
        # Handle any other exceptions
        print(e)
        context['error_message'] = "An error occurred"

    return render(request, 'update_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')

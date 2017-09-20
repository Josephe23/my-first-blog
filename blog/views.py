from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from .models import Publicacion
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Publicacion.objects.filter(fecha_creacion__lte=timezone.now()).order_by('fecha_publicacion')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    posts = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'blog/post_detail.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.fecha_creacion = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

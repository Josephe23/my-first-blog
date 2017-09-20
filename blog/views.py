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
            posts = form.save(commit=False)
            posts.autor = request.user
            posts.fecha_creacion = timezone.now()
            posts.save()
            return redirect('post_detail', pk=posts.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    posts = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=posts)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.autor = request.user
            posts.save()
            return redirect('post_detail', pk=posts.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

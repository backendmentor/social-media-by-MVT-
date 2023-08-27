from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .models import POST, Comment, Postlikes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from  .form import UpdateCommentForm, UpdatePostForm, CreateCommentForm, CreatePostForm, ReplyForm, SearchForm
from django.http import HttpResponse
from django.utils.text import slugify


class HomeView(View):
    search_form= SearchForm
    def get(self, request):
        posts= POST.objects.all()
        if request.GET.get("search"):
            posts= posts.filter(content__contains=request.GET["search"])
        return render(request, "home/index.html", {"posts":posts , "form":self.search_form})

class PostView(View):
    form_class = CreateCommentForm
    form_class_reply= ReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(POST, pk=kwargs["id_post"], slug=kwargs['slug_post'])
        return super().setup(request,*args, **kwargs)

    def get(self,request, *args, **kwargs):
        comments=self.post_instance.post_comment.filter(is_reply=False)
        return render(request, 'home/post_detail.html', {"post":self.post_instance, "comments": comments, "form":self.form_class, "reply_from": self.form_class_reply})

    def post(self,request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.user=request.user
            new_comment.post= self.post_instance
            new_comment.save()
            messages.success(request,"your send was successful", "success")
            return redirect("home:post_detail",self.post_instance.id, self.post_instance.slug )


class Postdelete(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(POST,pk=post_id)
        comments = Comment.objects.filter(post=post)
        if post.user == request.user:
            post.delete()
            comments.delete()
            messages.success(request, "Your post has been deleted", "success")
        else:
            messages.error(request, "There was something wrong", "info")
        return redirect("home:home")


class view_update(LoginRequiredMixin, View):
    class_form= UpdatePostForm
    class_form2=UpdateCommentForm
    def setup(self, request, *args, **kwargs):
        self.post_instance= get_object_or_404(POST,pk=kwargs["id_post"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post= self.post_instance
        coment=Comment.objects.filter(post=post)
        if not post.user.id == request.user.id:
            messages.error("your post is not yours", "danger")
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self, request, id_post):
        post =self.post_instance
        form = self.class_form(instance=post)
        content = Comment.objects.filter(post=post)
        return render(request, "home/templates/update_post.html", {"form":form, "content":content})

    def post(self, request, id_post):
        post = self.post_instance
        content= Comment.objects.filter(post=post)
        form= UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            new_post= form.save(commit=False)
            new_post.slug= slugify(form.cleaned_data["content"][:10])
            new_post.save()
            for obj in content:
                obj.save()
            messages.success(request,"your update is done", "success")
            return redirect("home:post_detail", post.id, post.slug)

class Creatview_post_comment(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CreatePostForm()
        return render(request, "home/create.html", {"form":form})
    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)
        comment = CreateCommentForm(request.POST)
        if form.is_valid() and comment.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data["content"][:30])
            new_post.user=request.user
            new_post.save()
            messages.success(request, "you added your post", "success")
            return redirect('home:post_detail', new_post.id, new_post.slug)


class ReplyView(LoginRequiredMixin, View):
    calss_form= ReplyForm
    def post(self, request, post_id, comment_id):
        post= get_object_or_404(POST,pk=post_id)
        comment=get_object_or_404(Comment,pk=comment_id)
        form=self.calss_form(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user =request.user
            reply.post=post
            reply.comment= comment
            reply.reply_is= True
            reply.save()
            messages.success(request, "the reply is done", "success")
            return redirect("home:post_detail",post.id, post.slug)



class LikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post= get_object_or_404(POST, pk=post_id)
        likes= Postlikes.objects.filter(post=post, user=request.user)
        if likes.exists():
            messages.error(request, "you already likes this post", "danger")
        else:
            Postlikes.objects.create(post=post, user= request.user)
            messages.success(request,"you likes this post", "success")
        return redirect("home:post_detail", post.id, post.slug)
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import register_user, LoginForm, EditForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from home.models import POST, Comment, User
from .models import Profile
from .models import Relationship
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy , reverse

class User_from_view(View):
    template_name = "accounts/register.html"
    form_class = register_user

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch( request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                User.objects.create_user(cd["Username"], cd["Email"], cd["Password1"])
                messages.success(request, "your register was successful", extra_tags="alert-success")
                return redirect("home:home")
            except IntegrityError:
                form.add_error(None, "This username is already taken. Please choose another one.", "warning")
                return render(request, self.template_name, {"form": form})
        else:
            # Change this line to re-render the existing form with any validation errors
            return render(request, self.template_name, {"form": form})

class LoginViewForm(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next", None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["Username"], password=cd["Password"])
            if user is not None:
                login(request, user)
                messages.success(request, "Your login was successful", "success")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            else:
                messages.error(request, "Your username does not exist", "warning")
                return render(request, self.template_name, {"form": form})

class logout_view_form(LoginRequiredMixin, View):
    def get(self, request):
            logout(request)
            messages.success(request, "you exit", "info")
            return redirect("home:home")

class LoginProfile(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if not request.user.is_authenticated:
            return redirect(f'/login?next={request.path}')
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = Relationship.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, "accounts/profile.html", {"user": user, "posts": posts, "is_following": is_following})

class Reset_password_view(auth_views.PasswordResetView):
    template_name ="accounts/poassword_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = 'accounts/poassword_reset_email.html'

class Reset_password_view_done(auth_views.PasswordResetDoneView ):
    template_name = "accounts/rese_password_done.html"

class Reset_password_view_confirm(auth_views.PasswordResetConfirmView):
    template_name= "accounts/password_reset_confirm.html"
    success_url= reverse_lazy("accounts:password_reset_complete")

class Reset_password_view_complete(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class Following_view( LoginRequiredMixin, View):
    def get(self, request, user_id):
        user= User.objects.get(pk=user_id)
        relation= Relationship.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "you already followed each other", "warning")
        else:
            Relationship(from_user=request.user, to_user=user).save()
            messages.success(request, "you follow this user", "success")
            return redirect("accounts:profile", user.id)
class Unfllowing_view(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relationship.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "you unfollow this user", "inform")
        else:
            messages.error(request, "you did not follow each other", "danger")
        return redirect("accounts:profile", user.id)

class EditeUserView(LoginRequiredMixin, View):
    class_form=EditForm
    def get(self, request):
        # profile = Profile.objects.get(user=request.user)
        form = self.class_form(instance=request.user.profile, initial={"email":request.user.email})
        return render(request, "accounts/accounts/edite.html", {"form": form})

    def post(self, request):
        form= self.class_form( request.POST, instance= request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email= form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "your edition was success", "success")
            return redirect("accounts:profile", request.user.id)

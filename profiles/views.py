from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from posts.forms import CommentCreateModelForm
from posts.models import Post
from posts.views_utils import add_comment_if_submitted

from .forms import MessageModelForm
from .models import Message, Profile, Relationship
from .views_utils import (
    check_if_friends,
    follow_unfollow,
    get_friends_of_user,
    get_profile_by_pk,
    get_profile_form_by_request_method,
    get_received_invites,
    get_received_messages,
    get_relationship_users,
    get_request_user_profile,
    get_sent_invites,
    redirect_back,
)


@login_required
def my_profile_view(request):

    profile = get_request_user_profile(request.user)

    form = get_profile_form_by_request_method(request, profile)

    posts = profile.posts.all()

    c_form = CommentCreateModelForm()

    if add_comment_if_submitted(request, profile):
        return redirect_back(request)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "Profile updated successfully!",
        )

        return redirect_back(request)

    context = {
        "profile": profile,
        "form": form,
        "posts": posts,
        "c_form": c_form,
    }

    return render(request, "profiles/my_profile.html", context)


@login_required
def received_invites_view(request):

    profile = get_request_user_profile(request.user)
    profiles = get_received_invites(profile)

    context = {
        "profiles": profiles,
    }

    return render(request, "profiles/received_invites.html", context)


@login_required
def sent_invites_view(request):

    profile = get_request_user_profile(request.user)
    profiles = get_sent_invites(profile)

    context = {
        "profiles": profiles,
    }

    return render(request, "profiles/sent_invites.html", context)


@login_required
def switch_follow(request):

    if request.method == "POST":
        my_profile = get_request_user_profile(request.user)
        profile = get_profile_by_pk(request)

        follow_unfollow(my_profile, profile)

    return redirect_back(request)


@login_required
def accept_invitation(request):

    if request.method == "POST":
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == "sent":
            rel.status = "accepted"
            rel.save()

    return redirect_back(request)


@login_required
def reject_invitation(request):

    if request.method == "POST":
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == "sent":
            rel.delete()

    return redirect_back(request)


@login_required
def my_friends_view(request):

    profile = get_request_user_profile(request.user)
    following = profile.following.all()

    profiles = Profile.objects.get_my_friends_profiles(request.user)

    context = {
        "following": following,
        "profiles": profiles,
    }

    return render(request, "profiles/my_friends.html", context)


@login_required
def search_profiles(request):

    search = request.GET.get("q", "")
    profiles = Profile.objects.filter(user__username__icontains=search)

    context = {
        "search": search,
        "profiles": profiles,
    }

    if search:
        return render(request, "profiles/search_profiles.html", context)

    return render(request, "profiles/search_profiles.html")


@login_required
def send_invitation(request):

    if request.method == "POST":
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        Relationship.objects.create(
            sender=sender,
            receiver=receiver,
            status="sent",
        )

    return redirect_back(request)


@login_required
def remove_friend(request):

    if request.method == "POST":
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver))
            | (Q(sender=receiver) & Q(receiver=sender)),
        )
        rel.delete()

    return redirect_back(request)


class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = "profiles/profile_detail.html"
    form_class = CommentCreateModelForm

    def get(self, request, *args, **kwargs):

        if Profile.objects.get(user=self.request.user) == self.get_object():
            return redirect("profiles:my-profile-view")

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = get_request_user_profile(self.request.user)
            instance.post = Post.objects.get(id=request.POST.get("post_id"))
            instance.save()

            form = CommentCreateModelForm()

            return redirect_back(self.request)

    def get_object(self):
        slug = self.kwargs.get("slug")
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_request_user_profile(self.request.user)
        following = profile.following.all

        invited_users, incoming_invite_users = get_relationship_users(profile)

        context["invited_users"] = invited_users
        context["incoming_invite_users"] = incoming_invite_users
        context["following"] = following
        context["form"] = self.form_class

        context["profile"] = self.get_object()
        context["request_user_profile"] = profile

        context["posts"] = self.get_object().posts.all()

        return context


class ProfileListView(LoginRequiredMixin, ListView):

    model = Profile
    template_name = "profiles/profile_list.html"

    def get_queryset(self):
        qs = Profile.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(user=self.request.user)
        following = profile.following.all

        invited_users, incoming_invite_users = get_relationship_users(profile)

        context["invited_users"] = invited_users
        context["incoming_invite_users"] = incoming_invite_users
        context["following"] = following
        context["profiles"] = self.get_queryset()

        return context


class MessengerListView(LoginRequiredMixin, ListView):

    model = Profile
    template_name = "profiles/messenger.html"

    def get_queryset(self):
        qs = get_friends_of_user(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profiles"] = self.get_queryset()

        return context


class ChatMessageView(LoginRequiredMixin, ListView):

    model = Message
    template_name = "profiles/chat.html"
    form_class = MessageModelForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = Profile.objects.get(user=self.request.user)
            instance.receiver = self.get_object()
            instance.save()

        return redirect_back(self.request)

    def get_object(self):
        slug = self.kwargs.get("slug")
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)

        sent = Message.objects.filter(
            sender=profile,
            receiver=self.get_object(),
        )
        received = Message.objects.filter(
            sender=self.get_object(),
            receiver=profile,
        )

        messages = sent | received
        ordered_messages = list(
            messages.order_by("-created").values_list("content", flat=True),
        )

        return ordered_messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["received"] = get_received_messages(
            self.get_object(),
            Profile.objects.get(user=self.request.user),
        )
        context["are_friends"] = check_if_friends(
            self.get_object(),
            self.request.user,
        )
        context["profile"] = self.get_object()
        context["form"] = self.form_class
        context["qs"] = self.get_queryset()

        return context

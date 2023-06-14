from profiles.models import Profile


def get_related_posts_queryset(profile, friends, following):
    from .models import Post

    unique_profiles = set()
    querysets = []
    post_pks = []

    for user in friends:
        unique_profiles.add(Profile.objects.get(user=user))

    for user in following:
        unique_profiles.add(Profile.objects.get(user=user))

    querysets.append(profile.posts.all())

    for unique_profile in unique_profiles:
        querysets.append(unique_profile.posts.all())

    for queryset in querysets:
        for post in queryset:
            post_pks.append(post.pk)

    result = Post.objects.filter(pk__in=post_pks).order_by("-created")
    return result

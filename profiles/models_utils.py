def get_list_of_profiles_by_user(users):
    result = []

    for user in users:

        from .models import Profile

        result.append(Profile.objects.get(user=user))

    return result


def get_likes_received_count(posts):
    total_liked = 0
    for post in posts:
        total_liked += post.liked.all().count()

    return total_liked

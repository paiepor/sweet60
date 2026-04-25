from .models import UserProfile


def user_avatar(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        return {'current_avatar': profile.avatar_b64 if profile else ''}
    return {'current_avatar': ''}

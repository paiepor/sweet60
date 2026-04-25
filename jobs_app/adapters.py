from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import UserProfile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        avatar_b64 = request.POST.get('avatar_b64', '')
        if avatar_b64:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.avatar_b64 = avatar_b64
            profile.save()
        return user

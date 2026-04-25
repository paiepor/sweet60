from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import UserProfile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        avatar_b64 = request.POST.get('avatar_b64', '')
        if avatar_b64:
            profile.avatar_b64 = avatar_b64
        id_card = request.FILES.get('id_card_image')
        if id_card:
            profile.id_card_image = id_card
        profile.no_criminal_record = 'no_criminal_record' in request.POST
        profile.consent_id_upload = 'consent_id_upload' in request.POST
        profile.save()
        return user

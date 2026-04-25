import base64
from django.core.files.base import ContentFile
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import UserProfile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        avatar_b64 = request.POST.get('avatar_b64', '')
        if avatar_b64:
            profile.avatar_b64 = avatar_b64
        id_card_b64 = request.POST.get('id_card_b64', '')
        if id_card_b64 and ';base64,' in id_card_b64:
            try:
                header, data = id_card_b64.split(';base64,', 1)
                profile.id_card_image = ContentFile(
                    base64.b64decode(data), name=f'id_card_{user.id}.jpg'
                )
            except Exception:
                pass
        profile.no_criminal_record = 'no_criminal_record' in request.POST
        profile.consent_id_upload = 'consent_id_upload' in request.POST
        profile.save()
        return user

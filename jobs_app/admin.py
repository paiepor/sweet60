from django.contrib import admin
from .models import JobListing, UserProfile, Event, ChatMessage

admin.site.register(JobListing)
admin.site.register(Event)
admin.site.register(ChatMessage)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthdate', 'no_criminal_record', 'consent_id_upload')
    list_filter = ('no_criminal_record', 'consent_id_upload')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('user',)
    fields = ('user', 'birthdate', 'experience', 'id_card_image', 'no_criminal_record', 'consent_id_upload')
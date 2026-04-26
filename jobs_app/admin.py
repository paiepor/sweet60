from django.contrib import admin
from .models import JobListing, UserProfile, Event, ChatMessage, Application, CommunityGroup, GroupPost, GroupPostLike

admin.site.register(Event)
admin.site.register(ChatMessage)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthdate', 'no_criminal_record', 'consent_id_upload')
    list_filter = ('no_criminal_record', 'consent_id_upload')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('user',)
    fields = ('user', 'birthdate', 'experience', 'id_card_image', 'no_criminal_record', 'consent_id_upload')


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'salary', 'is_active', 'author')
    list_filter = ('is_active',)
    search_fields = ('title', 'company_name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'applied_at')
    list_filter = ('applied_at',)
    search_fields = ('applicant__username', 'job__title')


@admin.register(CommunityGroup)
class CommunityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'creator', 'is_private', 'created_at')
    list_filter = ('category', 'is_private')
    search_fields = ('name', 'creator__username')


@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'group', 'created_at')
    search_fields = ('author__username', 'group__name')


@admin.register(GroupPostLike)
class GroupPostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
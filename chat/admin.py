from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('item__title', 'participants__email')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('sender__email', 'content', 'conversation__id')
    readonly_fields = ('sent_at', 'read_at')

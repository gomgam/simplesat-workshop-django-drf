from django.contrib import admin

from polls.models import Choice, Poll, Vote


class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice


class VoteInlineAdmin(admin.TabularInline):
    model = Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'question', 'created_by', 'pub_date', 'country']
    inlines = [ChoiceInlineAdmin, VoteInlineAdmin]

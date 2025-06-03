from django.contrib import admin
from .models import Profile, Category, Tag, Listing

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    raw_id_fields = ('author',)
    filter_horizontal = ('tags', 'favorited_by')
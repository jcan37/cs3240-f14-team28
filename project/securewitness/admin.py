from django.contrib import admin
from securewitness.models import Bulletin, File, Folder, Permission, Filing

class FileInline(admin.TabularInline):
	model = File
	extra = 3


class BulletinAdmin(admin.ModelAdmin):
	inlines = [FileInline]
	list_display = ['description', 'author', 'pub_date', 'location', 'encrypted']
	list_filter = ['pub_date']
	search_fields = ['description', 'author__username', 'location']


class FileAdmin(admin.ModelAdmin):
	list_display = ['name', 'bulletin', 'content_type', 'is_encrypted']
	search_fields = ['name', 'bulletin__description']


class FolderAdmin(admin.ModelAdmin):
        list_display = ['name', 'owner']
        search_fields = ['name', 'owner']


class PermissionAdmin(admin.ModelAdmin):
        list_display = ['user', 'bulletin']
        search_fields = ['user__username', 'bulletin__description']


class FilingAdmin(admin.ModelAdmin):
        list_display = ['folder', 'bulletin']
        search_fields = ['folder__name', 'folder__owner', 'bulletin__description', 'bulletin__author']


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Filing, FilingAdmin)

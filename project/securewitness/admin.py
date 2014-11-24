from django.contrib import admin
from securewitness.models import Bulletin, File, Folder, Permission

class BulletinInline(admin.TabularInline):
	model = Bulletin
	extra = 3


class FileInline(admin.TabularInline):
	model = File
	extra = 3


class BulletinAdmin(admin.ModelAdmin):
	inlines = [FileInline]
	list_display = ['description', 'author', 'pub_date', 'location', 'parent', 'encrypted']
	list_filter = ['pub_date']
	search_fields = ['description', 'author__username', 'location', 'parent__name']


class FileAdmin(admin.ModelAdmin):
	list_display = ['name', 'bulletin', 'content_type', 'is_encrypted']
	search_fields = ['name', 'bulletin__description']


class FolderAdmin(admin.ModelAdmin):
	inlines = [BulletinInline]
        search_fields = ['name']


class PermissionAdmin(admin.ModelAdmin):
        list_display = ['user', 'bulletin']
        search_fields = ['user__username', 'bulletin__description']


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Permission, PermissionAdmin)

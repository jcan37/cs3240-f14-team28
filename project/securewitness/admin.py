from django.contrib import admin
from securewitness.models import Bulletin, File

class FileInline(admin.TabularInline):
	model = File
	extra = 3


class BulletinAdmin(admin.ModelAdmin):
	inlines = [FileInline]
	list_display = ['description', 'author', 'pub_date', 'location', 'parent']
	list_filter = ['pub_date']
	search_fields = ['description', 'author', 'location', 'parent']


class FileAdmin(admin.ModelAdmin):
	list_display = ['url', 'bulletin', 'encrypted']
	search_fields = ['url', 'bulletin']


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(File, FileAdmin)

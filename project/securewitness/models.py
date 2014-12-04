import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

class Bulletin(models.Model):
	description = models.CharField(max_length=128)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	pub_date = models.DateTimeField('date published')
	location = models.CharField(max_length=128, default='Charlottesville, VA')
	encrypted = models.BooleanField(default=True)
        
        
        def file_list(self):
                all_files = File.objects.all()
                if all_files is None or len(all_files) == 0:
                        return []
                return all_files.filter(bulletin=self).order_by('name')


	def time_stamp(self):
                # timezone.activate(settings.TIME_ZONE)
                # now = timezone.now()
                # pub_date = self.pub_date
                now = timezone.now() - datetime.timedelta(hours=5)
                pub_date = self.pub_date - datetime.timedelta(hours=5)
                # **********
                diff = now - pub_date
                within_hour = now - datetime.timedelta(hours=1)
                if pub_date > within_hour:
                        mins = diff.days * 86400 + diff.seconds // 60
                        if mins == 1:
                                return str(mins) + ' minute ago'
                        return str(mins) + ' minutes ago'
                if pub_date.date() == now.date():
                        return 'Today at ' + pub_date.time().strftime('%-I:%M %p')
                yesterday = now - datetime.timedelta(days=1)
                if pub_date.date() == yesterday.date():
                        return 'Yesterday at ' + pub_date.time().strftime('%-I:%M %p')
                within_year = now - datetime.timedelta(weeks=52)
                if pub_date > within_year:
                        return pub_date.strftime('%b %-d at %-I:%M %p')
                return pub_date.strftime('%b %-d, %Y at %-I:%M %p')

        def __str__(self):
		return str(self.description)


class File(models.Model):
	name = models.CharField(max_length=128)
	bulletin = models.ForeignKey('Bulletin')
	encryption_key = models.CharField(max_length=32, default='', editable=False)
	content_type = models.CharField(max_length=128, default='')


        def is_encrypted(self):
                return self.bulletin.encrypted
        is_encrypted.boolean = True
        is_encrypted.short_description = 'Encrypted?'


	def __str__(self):
		return str(self.bulletin) + '/' + str(self.id) + '_' + str(self.name)


class Folder(models.Model):
        owner = models.ForeignKey(settings.AUTH_USER_MODEL)
        name = models.CharField(max_length=128)


        def bulletin_list(self):
                filings = Filing.objects.filter(folder=self)
                bulletin_list = Bulletin.objects.none()
                for filing in filings:
                        bulletin_list |= Bulletin.objects.filter(pk=filing.bulletin.pk)
                return bulletin_list.order_by('description')


        def __str__(self):
                return str(self.name)


class Permission(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        bulletin = models.ForeignKey('Bulletin')


        def __str__(self):
                return str(self.user.username) + ' can view ' + str(self.bulletin)


class Filing(models.Model):
        folder = models.ForeignKey('Folder')
        bulletin = models.ForeignKey('bulletin')

        
        def __str__(self):
                return str(self.bulletin) + ' is filed under ' + str(self.folder)

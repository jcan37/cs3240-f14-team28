from django.db import models
from django.conf import settings

class Bulletin(models.Model):
	description = models.CharField(max_length=128)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	pub_date = models.DateTimeField('date published')
	location = models.CharField(max_length=256, default='Charlottesville, VA')
	parent = models.ForeignKey('Folder', blank=True, null=True)


	def __str__(self):
		if self.parent is not None:
			return str(self.parent) + '/' + str(self.description)
		return str(self.description)


class File(models.Model):
	name = models.CharField(max_length=128)
	bulletin = models.ForeignKey('Bulletin')
	encryption_key = models.CharField(max_length=32, default='', editable=False)


        def is_encrypted(self):
                return self.encryption_key != ''
        is_encrypted.boolean = True
        is_encrypted.short_description = 'Encrypted?'


	def __str__(self):
		return str(self.bulletin) + '/' + str(self.name)


class Folder(models.Model):
        name = models.CharField(max_length=128)


        def __str__(self):
                return str(self.name)


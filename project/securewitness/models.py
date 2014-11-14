from django.db import models
from django.conf import settings

class Bulletin(models.Model):
	description = models.CharField(max_length=1000)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	pub_date = models.DateTimeField('date published')
	location = models.CharField(max_length=200, default='Charlottesville, VA')
	parent = models.ForeignKey('self', blank=True, null=True)

	def __str__(self):
		if self.parent is not None:
			return str(self.parent) + '/' + str(self.description)
		return str(self.description)


class File(models.Model):
	bulletin = models.ForeignKey(Bulletin)
	url = models.CharField(max_length=500)
	encrypted = models.BooleanField(default=True)	

	def __str__(self):
		return str(self.bulletin) + '/' + str(self.url)

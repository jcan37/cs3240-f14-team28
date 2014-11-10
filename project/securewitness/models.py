from django.db import models
from django.conf import settings

class Bulletin(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	pub_date = models.DateTimeField("date published")
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=200)
	encrypted = models.BooleanField(default=True)

	def __str__(self):
		return 'Author: ' + str(self.author) + '\nDate: ' + str(self.pub_date) + '\nDescription: ' + str(self.description) + '\nLocation: ' + str(self.location) + '\nEncrypted: ' + str(self.encrypted)


class File(models.Model):
	bulletin = models.ForeignKey(Bulletin)
	url = models.CharField(max_length=500)
	
	def __str__(self):
		return 'Bulletin: ' + str(self.bulletin) + '\nUrl: ' + str(self.url)

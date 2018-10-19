from django.db import models

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    dest = models.CharField(max_length=200)

    def publish(self):
        self.save()

    def __str__(self):
        return self.source

class Post2(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	source = models.CharField(max_length=200)
	dest = models.CharField(max_length=200)
	date = models.CharField(max_length=200)

	def publish(self):
		self.save()

	def __str__(self):
		return self.source
from django.db import models
import hashlib
from base64 import b64encode


class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    entry = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='entries')
    hash = models.TextField()

    def save(self, *args, **kwargs):
        sha256 = hashlib.sha256()
        sha256.update(self.entry.encode())
        self.hash = b64encode(sha256.digest())
        super(Entry, self).save(*args, **kwargs)


class Meta:
    ordering = ('created',)

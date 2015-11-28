from django.db import models



class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    entry = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='entries')


class Meta:
        ordering = ('created',)

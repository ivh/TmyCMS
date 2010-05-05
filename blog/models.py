from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import User

ENTRY_STATUS_CHOICES = (
('draft','draft'),
('published','published'),
('private','private'),
)

class Tag(models.Model):
    name=models.CharField(max_length=128)


class Entry(models.Model):
    datetime=model.DateTimeField()
    author=model.ForeignKey(User,default=User.objects.get(pk=1))
    title=models.CharField(max_length=512)
    text=models.CharField(max_length=512)
    tags=models.ManyToManyField(Tag,null=True,blank=True)
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

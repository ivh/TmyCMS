from django.utils.translation import ugettext_lazy as _
from django.db import models as m
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator

LANGUAGES=(
('g',_('German')),
('s',_('Swedish')),
('e',_('English')),
)

class Tag(m.Model):
    name=m.CharField(max_length=128)
    slug=m.SlugField(primary_key=True)
    def __unicode__(self):
        return u'Tag: %s'%self.name


class Entry(m.Model):
    pub_date=m.DateTimeField(null=True,blank=True)
    mod_date=m.DateTimeField(auto_now=True)
    author=m.ForeignKey(User,related_name='entries')
    lang=m.CharField(max_length=1,choices=LANGUAGES)
    title=m.CharField(max_length=512)
    slug=m.SlugField()
    body=m.CharField(max_length=512)
    enable_comments = m.BooleanField(default=True)
    tags=m.ManyToManyField(Tag,related_name='entries',null=True,blank=True)
    site = m.ManyToManyField(Site)
    objects = m.Manager()
    on_site = CurrentSiteManager()

    def publish(self):
        pass

    def __unicode__(self):
        return u'Entry %s: %s'%(self.id,self.title)

    class Meta:
        ordering = ["-pub_date"]
        


# see http://docs.djangoproject.com/en/dev/ref/contrib/comments/moderation/
class EntryModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'
    auto_moderate_field   = 'pub_date'
    moderate_after        = 31

moderator.register(Entry, EntryModerator)





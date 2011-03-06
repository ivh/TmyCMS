from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator

from django.db.models import *
from markupfield.fields import MarkupField

LANGUAGES=(
('g',_('German')),
('s',_('Swedish')),
('e',_('English')),
)

class Tag(Model):
    slug=SlugField(primary_key=True,unique=True)
    name=CharField(max_length=128)
    site=ManyToManyField(Site)
    def __unicode__(self):
        return u'Tag: %s'%self.name

    @permalink
    def get_absolute_url(self):
        return ('tag', [self.slug])

    class Meta:
        ordering = ["name"]

class Entry(Model):
    pub_date=DateTimeField(null=True,blank=True)
    mod_date=DateTimeField(auto_now=True)
    author=ForeignKey(User,related_name='entries')
    lang=CharField(max_length=1,choices=LANGUAGES)
    title=CharField(max_length=512)
    slug=SlugField()
    body=MarkupField(markup_type='textile')
    enable_comments = BooleanField(default=True)
    tags=ManyToManyField(Tag,related_name='entries',null=True,blank=True)
    site = ManyToManyField(Site)
    objects = Manager()
    on_site = CurrentSiteManager()

    def publish(self):
        pass

    def __unicode__(self):
        return u'Entry %s: %s'%(self.id,self.title)

    @permalink
    def get_absolute_url(self):
        return ('permalink', [str(self.pub_date.year),str(self.pub_date.month).zfill(2),str(self.pub_date.day).zfill(2),self.slug])

    class Meta:
        ordering = ["-pub_date"]



# see http://docs.djangoproject.com/en/dev/ref/contrib/comments/moderation/
class EntryModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'
    auto_moderate_field   = 'pub_date'
    moderate_after        = 31

moderator.register(Entry, EntryModerator)





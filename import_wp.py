#!/usr/bin/python

import MySQLdb
import sys,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyDjangoSites.settings'
from datetime import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from MyDjangoSites.blog.models import Entry, Tag

conn = MySQLdb.connect (host = "localhost",
                        user = "blogblog",
                        passwd = "aiN8dee2",
                        db = "blogblog")

cursor = conn.cursor ()


LANG='g'
SITE=Site.objects.get(name='BlogBlog')
AUTHOR=User.objects.get(pk=1)

cursor.execute('select name,slug from wp_terms;')
for name,slug in cursor.fetchall():
    #print name, slug
    Tag(name=name,slug=slug).save(force_insert=True)


cursor.execute('select ID,post_date,post_title,post_content,post_name from wp_posts where post_status="publish";')
posts=cursor.fetchall()

for ID,post_date,post_title,post_content,post_name in posts:
    entry=Entry(pub_date=post_date,title=post_title,lang=LANG,body=post_content,author=AUTHOR,slug=post_name)
    entry.save(force_insert=True)
    entry.site.add(SITE)
#    entry.tags.add(Tag)
    entry.save()

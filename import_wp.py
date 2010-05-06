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
    
    cursor.execute('select name,slug from wp_terms, wp_posts, wp_term_relationships, wp_term_taxonomy where wp_posts.ID="%s" AND wp_posts.ID=wp_term_relationships.object_ID AND wp_term_relationships.term_taxonomy_id=wp_term_taxonomy.term_taxonomy_id AND wp_term_taxonomy.term_id=wp_terms.term_id'%ID)
    tags=cursor.fetchall()
    for tag_name,tag_slug in tags:
        tag=Tag.objects.get(slug=tag_slug)
        entry.tags.add(Tag)
        print post_name,tag_slug,Tag

    entry.save()

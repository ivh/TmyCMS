#!/usr/bin/python

import MySQLdb
import sys,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyDjangoSites.settings'
from datetime import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

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
    entry.save()

    print ID
    cursor.execute('select name,slug from wp_terms, wp_posts, wp_term_relationships, wp_term_taxonomy where wp_posts.ID="%s" AND wp_posts.ID=wp_term_relationships.object_ID AND wp_term_relationships.term_taxonomy_id=wp_term_taxonomy.term_taxonomy_id AND wp_term_taxonomy.term_id=wp_terms.term_id and post_type="post"'%ID)
    tags=cursor.fetchall()
    for tag_name,tag_slug in tags:
        tag=Tag.objects.get(slug=tag_slug)
        entry.tags.add(tag)
    
    entry.save()

    cursor.execute('select comment_author,comment_author_email,comment_author_url,comment_author_IP,comment_date,comment_content from wp_comments where comment_approved=1 and comment_post_ID=%s'%ID)
    comments=cursor.fetchall()
    for comment_author,comment_author_email,comment_author_url,comment_author_IP,comment_date,comment_content in comments:
        comm=Comment(content_object=entry,site=SITE,user_name=comment_author,user_email=comment_author_email,user_url=comment_author_url,comment=comment_content,ip_address='127.0.0.1',submit_date=comment_date,is_public=True,is_removed=False)
        comm.save(force_insert=True)
        
    entry.save()

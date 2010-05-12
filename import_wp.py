#!/usr/bin/python

import MySQLdb
import sys,os
import string as s
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyDjangoSites.settings'
from datetime import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.db.utils import IntegrityError
from MyDjangoSites.blog.models import Entry, Tag

unic= lambda x: x #u'%s'%x.decode('latin1')

from random import choice
def RandStr(length=3, chars=s.letters + s.digits):
    return ''.join([choice(chars) for i in xrange(length)])

pwds=open('pwds').readlines()
pwds=map(s.strip,pwds)

blogs=[{'sitename':'BlogBlog','dbuser':'blogblog','dbname':'blogblog','pwd':pwds[0]},
       {'sitename':'Fiket','dbuser':'fiket','dbname':'fiket','pwd':pwds[1]},
       {'sitename':'Atheist','dbuser':'atheist','dbname':'atheistundgut','pwd':pwds[2]},
    ]


def do_tags(cursor):
    cursor.execute('select name,slug from wp_terms;')
    for name,slug in cursor.fetchall():
        print name, slug
        t=Tag(slug=slug)
        t.name=name
        t.save()
        t.site.add(SITE)
        t.save()
        

def do_comments(cursor,ID,entry):
    cursor.execute('select comment_author,comment_author_email,comment_author_url,comment_author_IP,comment_date,comment_content from wp_comments where comment_approved=1 and comment_post_ID=%s'%ID)
    comments=cursor.fetchall()
    for comment_author,comment_author_email,comment_author_url,comment_author_IP,comment_date,comment_content in comments:
        comm=Comment(content_object=entry,site=SITE,user_name=unic(comment_author),user_email=comment_author_email,user_url=comment_author_url,comment=unic(comment_content),ip_address='127.0.0.1',submit_date=comment_date,is_public=True,is_removed=False)
        comm.save(force_insert=True)


def do_entries(cursor):
    cursor.execute('select ID,post_date,post_title,post_content,post_name from wp_posts where post_status="publish" and (post_type="post");')
    posts=cursor.fetchall()
        
    for ID,post_date,post_title,post_content,post_name in posts:
        entry=Entry(pub_date=post_date,title=unic(post_title),lang=LANG,
                    body=unic(post_content),author=AUTHOR,slug=post_name)
        entry.save(force_insert=True)
        entry.site.add(SITE)
        
        try: entry.save()
        except IntegrityError,e:
            print e
            if 'column slug is not unique' in e:
                entry.slug=entry.slug+RandStr()
                entry.save()
                
    
    
        cursor.execute('select name,slug from wp_terms, wp_posts, wp_term_relationships, wp_term_taxonomy where wp_posts.ID="%s" AND wp_posts.ID=wp_term_relationships.object_ID AND wp_term_relationships.term_taxonomy_id=wp_term_taxonomy.term_taxonomy_id AND wp_term_taxonomy.term_id=wp_terms.term_id'%ID)
        tags=cursor.fetchall()
        for tag_name,tag_slug in tags:
            tag=Tag.objects.get(slug=tag_slug)
            entry.tags.add(tag)
            
        entry.save()
        do_comments(cursor,ID,entry)



for blog in blogs:
    conn = MySQLdb.connect (host = "localhost",
                             user = blog['dbuser'],
                             passwd = blog['pwd'],
                             db = blog['dbname'])
    
    cursor = conn.cursor ()


    LANG='g'
    SITE=Site.objects.get(name=blog['sitename'])
    AUTHOR=User.objects.get(pk=1)


    do_tags(cursor)
    do_entries(cursor)
    
    
####### special operations

# get entries tagged Europa into the EU-site
# and the other tags too.
et=Tag.objects.get(slug='europa')
eus=Site.objects.get(name='EU')
ee=Entry.objects.filter(tags=et)
for e in ee:
    e.site.add(eus)
    e.save()
    for t in e.tags.all():
        if t.slug != 'europa':
            t.site.add(eus)


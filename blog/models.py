import datetime
from flask import url_for
from blog import db

class Post(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	title = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)
	body = db.StringField(max_length=255, required=True)
	comments = db.ListField(db.EmbeddedDocumentField('Comment'))

	def get_absolute_url(self):
		return url_for('post', kwargs = { 'slug' : self.slug })

	def __unicode__(self):
		return self.title

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}


class Comment(db.EmbeddedDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	body = db.StringField(verbose_name='Comment', required=True)
	author = db.StringField(max_length=255, verbose_name='Name', required=True)
#coding=utf-8
from django_mongoengine import Document, EmbeddedDocument, fields

# Create your models here.
class start_time(Document):
    title = fields.StringField(blank=True)
    cover = fields.StringField(blank=True)
    time  = fields.ListField(fields.DictField())

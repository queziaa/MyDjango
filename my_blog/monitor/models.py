#coding=utf-8
from django_mongoengine import Document, EmbeddedDocument, fields

class time_emd(EmbeddedDocument):
    index = fields.IntField(blank=True)
    season_id = fields.IntField(blank=True)
    start = fields.IntField(blank=True)
    aid = fields.IntField(blank=True)
    hour = fields.IntField(blank=True)
    hour_freq = fields.IntField(blank=True)
    coin = fields.ListField()
    danmaku = fields.ListField()
    share = fields.ListField()
    view = fields.ListField()
    reply = fields.ListField()

class start_time_2(Document):
    title = fields.StringField(blank=True)
    cover = fields.StringField(blank=True)
    time = fields.ListField(fields.EmbeddedDocumentField('time_emd'), default=[])



# class int_emd(EmbeddedDocument):
#     i = fields.IntField(blank=True)
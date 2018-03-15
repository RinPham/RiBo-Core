from mongoengine import Document, fields
from mongoengine.document import EmbeddedDocument

class Event(Document):
    kind = fields.StringField()
    etag = fields.StringField()
    id_event = fields.ObjectIdField()
    status = fields.StringField()
    created = fields.DateTimeField()
    updated = fields.DateTimeField()
    summary = fields.StringField()
    creator = fields.EmbeddedDocumentField(Creator)
    organizer = fields.EmbeddedDocumentField(Organizer)
    start = fields.EmbeddedDocumentField(Time)
    end = fields.EmbeddedDocumentField(Time)
    iCalUID = fields.StringField()
    sequence = fields.IntField()
    reminders = fields.EmbeddedDocument(Reminder)
    location = fields.StringField()
    attachments = fields.EmbeddedDocumentListField(Attachment)
    attendees = fields.EmbeddedDocumentListField(Attendee)

class Creator(EmbeddedDocument):
    id = fields.StringField()
    email = fields.EmailField()
    self = fields.BooleanField()
    displayName = fields.StringField()

class Organizer(EmbeddedDocument):
    id = fields.StringField()
    email = fields.EmailField()
    self = fields.BooleanField()
    displayName = fields.StringField()

class Time(EmbeddedDocument):
    date = fields.DateTimeField()
    dateTime = fields.DateTimeField()
    timeZone = fields.StringField()

class Reminder(EmbeddedDocument):
    useDefault = fields.BooleanField()
    overrides = fields.EmbeddedDocumentListField(Override)

class Override(EmbeddedDocument):
    method = fields.StringField()
    minutes = fields.IntField()

class Attachment(EmbeddedDocument):
    fileUrl = fields.StringField()
    title = fields.StringField()
    mimeType = fields.StringField()
    iconLink = fields.StringField()
    fileId = fields.StringField()

class Attendee(EmbeddedDocument):
    id = fields.StringField()
    email = fields.StringField()
    displayName = fields.StringField()
    organizer = fields.BooleanField()
    self = fields.BooleanField()
    resource = fields.BooleanField()
    optional = fields.BooleanField()
    responseStatus = fields.StringField()
    comment = fields.StringField()
    additionalGuests = fields.IntField()
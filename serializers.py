from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str()
    password = fields.Str()
   

class NoteSchema(Schema):
    user = fields.Str()
    message = fields.Str()
    

import reprlib

class Challenge:
    def __init__(self, id_, name, description):
        self.id = id_
        self.name = name
        self.description = description

    @classmethod
    def fromjson(cls, json):
        id_ = json['id']
        name = json['name']
        description = json['description']
        return cls(id_, name, description)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

    def __repr__(self):
        return 'Challenge({}, {}, {})'.format(self.id, self.name, reprlib.repr(self.description))
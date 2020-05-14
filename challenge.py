import reprlib

class Challenge:
    def __init__(self, id_, name, kyu, description):
        self.id = id_
        self.name = name
        self.kyu = kyu
        self.description = description
        self.code = None

    @classmethod
    def fromjson(cls, json):
        id_ = json['id']
        name = json['name']
        kyu = json['rank']['name']
        description = json['description']
        return cls(id_, name, kyu, description)

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.name, self.kyu)

    def __repr__(self):
        return 'Challenge({}, {}, {}, {})'.format(self.id, self.name, self.kyu, reprlib.repr(self.description))
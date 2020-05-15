import reprlib


class Challenge:
    def __init__(self, id_, name, url, kyu, description):
        self.id = id_
        self.name = name
        self.url = url
        self.kyu = kyu
        self.description = description
        self.language = None
        self.code = None

    @classmethod
    def fromjson(cls, json):
        id_ = json['id']
        name = json['name']
        kyu = json['rank']['name']
        url = json['url']

        description_header = '# [{}]({})'.format(name, url)
        description_text = json['description']

        description = '\n'.join([description_header, description_text])

        return cls(id_, name, url, kyu, description)

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.name, self.kyu)

    def __repr__(self):
        return 'Challenge({}, {}, {}, {})'.format(self.id, self.name, self.kyu, reprlib.repr(self.description))

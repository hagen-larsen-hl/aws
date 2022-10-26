import json
from widget.CustomJSONEncoder import CustomJSONEncoder

class Widget:
    def __init__(self, id, owner, label, description, attributes):
        self.id = id
        self.owner = owner
        self.label = label
        self.description = description
        self.otherAttributes = attributes

    def toJson(self):
        return json.dumps(self.__dict__, cls=CustomJSONEncoder)

    def toDynamoDBItem(self):
        item = {
            'id': {'S': self.id},
            'owner': {'S': self.owner},
            'label': {'S': self.label},
            'description': {'S': self.description}
        }
        for attribute in self.otherAttributes:
            item[attribute.name] = {'S': attribute.value}
        return item
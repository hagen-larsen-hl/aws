class Widget:

    def __init__(self, owner, label, description):
        self.attributes = []
        self.id = id(self)
        self.owner = owner
        self.label = label
        self.description = description

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

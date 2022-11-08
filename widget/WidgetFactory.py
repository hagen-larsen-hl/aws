import logging
from widget.Widget import Widget
from widget.Attribute import Attribute
import json

logger = logging.getLogger("consumer")

class WidgetFactory:
    def createWidget(self, createRequest):
        widget = Widget(id=createRequest.widgetId, owner=createRequest.owner, label=createRequest.label, description=createRequest.description, attributes=createRequest.otherAttributes)
        return widget

    def updateWidget(self, widget, updates):
        widget = json.loads(widget)
        for update in updates:
            widget[update] = updates[update]
        id = widget['id']
        owner = widget['owner']
        label = widget['label']
        description = widget['description']
        del widget['id']
        del widget['owner']
        del widget['label']
        del widget['description']
        otherAttributes = []
        for attribute in widget:
            otherAttributes.append(Attribute(attribute, widget[attribute]))
        return Widget(id, owner, label, description, otherAttributes)

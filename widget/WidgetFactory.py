from widget.Widget import Widget
import logging

logger = logging.getLogger("consumer")

class WidgetFactory:
    def createWidget(self, createRequest):
        widget = Widget(id=createRequest.widgetId, owner=createRequest.owner, label=createRequest.label, description=createRequest.description, attributes=createRequest.otherAttributes)
        return widget

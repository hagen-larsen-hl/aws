from widget.Widget import Widget
import sys

class WidgetFactory:
    def createWidget(self, createRequest):
        print("Creating widget")
        widget = Widget(id=createRequest.widgetId, owner=createRequest.owner, label=createRequest.label, description=createRequest.description, attributes=createRequest.otherAttributes)
        return widget

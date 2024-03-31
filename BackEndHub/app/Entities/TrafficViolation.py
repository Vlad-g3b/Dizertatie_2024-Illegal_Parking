import json
from datetime import datetime

class TrafficViolation() :
    
    def __init__(self, id, desc, location, parking_site, date_ins, date_res, resolved):
        self.id = id
        self.description = desc
        if isinstance(location, str):
            self.location = json.loads(location)
        else:
            self.location = location
        self.parking_site_id = parking_site
        if date_ins is not None:
            self.date_ins = self.formatDate(date_ins)
        else:
            self.date_ins = date_ins
        if date_res is not None:
            self.date_res = self.formatDate(date_res)
        else:
            self.date_res = " "
        self.resolved = resolved

    def getJsonObject(self):
        string = {
            "id": self.id,
            "description" : self.description,
            "location": self.location,
            "parking_site_id": self.parking_site_id,
            "date_ins" : self.date_ins,
            "date_res" : self.date_res,
            "resolved" : self.resolved
        }
        return json.dumps(string)

    def formatDate(self, input:datetime):
        date_object = input
        return date_object.strftime("%A, %B %d, %Y %I:%M %p")

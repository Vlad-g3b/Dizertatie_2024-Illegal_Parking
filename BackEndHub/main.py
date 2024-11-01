from pickle import NONE
from typing import Annotated, Union
from uu import Error
from fastapi.security import OAuth2PasswordBearer
from pydantic import Json
import uvicorn
from fastapi import FastAPI
from starlette.types import Receive, Scope, Send
from fastapi import Request, Depends,HTTPException
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.Services.MainService import MainService
import app.Entities.BasicEntities as BE
import logging
import asyncio
import json
import sys

from random import randint

class SSEManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, response):
        self.subscriptions.append(response)

    def remove_subscription(self, response):
        self.subscriptions.remove(response)

    async def broadcast_message(self, message: dict):
        for response in self.subscriptions:
            await response.send_text(f"data: {json.dumps(message)}\n\n")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

sse_manager = SSEManager()
app = FastAPI()

STREAM_DELAY = 10  # second
RETRY_TIMEOUT = 15000  # milisecond
cnt = 0
data_to_be_sent = None

list_of_data_to_be_sent = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_coordinates = [[38.248736, 21.738931], [38.246637, 21.736243], [38.247328, 21.737185]]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info('API is starting up')

async def get_body(request: Request):
    return await request.body()


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/getAllTrafficViolation")
def getDataFromDb():
    ms = MainService()
    list_records = ms.getTrafficViolationList() 
    logger.debug(list_records)
    return {'TrafficViolationList' : list_records}

@app.post("/getAllNotes")
def getAllNotes(note: BE.Note):
    ms = MainService()
    list_records = ms.getNotesByUser(note.nt_user) 
    logger.debug(list_records)
    return list_records

@app.post("/getLatestNotes")
def getLatestNotes(note: BE.Note):
    ms = MainService()
    list_records = ms.getNotesByUserLatest(note.nt_user) 
    logger.debug(list_records)
    return list_records

@app.get("/getAllUnresolvedTrafficViolation")
def getDataFromDb2():
    ms = MainService()
    list_records = ms.getTrafficViolationListUnresolved() 
    logger.debug(list_records)
    return {'TrafficViolationList' : list_records}

@app.get("/getStats")
def getDataFromDb3():
    ms = MainService()
    output = {}
    list_records = ms.getTrafficViolationStats() 
    output['TrafficViolationStats'] = list_records 
    list_records = ms.getTrafficViolationStats1() 
    out = {}
    for item in list_records:
        parking_site = item[0] # type: ignore
        violation_type = str(item[1])  # type: ignore # Convert to string for JSON-like key
        count = item[2] # type: ignore
        if parking_site not in out:
            out[parking_site] = {}
        if violation_type not in out[parking_site]:
            out[parking_site][violation_type] = 0
        out[parking_site][violation_type] += count
    output['TrafficViolationStats1'] = out 
    list_records = ms.getTrafficViolationStats2()
    out = {}
    for item in list_records:
        parking_site = item[0] # type: ignore
        violation_type = str(item[1])  # type: ignore # Convert to string for JSON-like key
        count = item[2] # type: ignore
        if parking_site not in out:
            out[parking_site] = {}
        out[parking_site]["0"] = 0
        out[parking_site]["1"] = 0
        out[parking_site][violation_type] += count

    output['TrafficViolationStats2'] = out
    list_records = ms.getTrafficViolationStats3() 
    output['TrafficViolationStats3'] = list_records 
    return output

@app.get("/getAllTParkingSites")
def getDataFromDb4():
    ms = MainService()
    list_records = ms.getParkingSiteList() 
    logger.debug(list_records)
    return {"list" : list_records} # type: ignore

@app.post("/updateResolved")
def updateTFResolved(tf : BE.TrafficViolation):
    ms = MainService()
    ms.updateTFResolved(tf.tf_id, tf.is_resolved, tf.username) 
    logger.debug(tf)
    return tf

@app.patch("/editParkingSite")
def editParkingSite(ob : BE.ParkingSite):
    ms = MainService()
    ms.updateParkingSite(ob.ps_id, ob.ps_description, ob.ps_max_parking_spots) 
    logger.debug(ob)
    return ob

@app.delete("/deleteParkingSite")
def deleteParkingSite(ob : BE.ParkingSite):
    ms = MainService()
    ms.deleteParkingSite(ob.ps_id) 
    logger.debug(ob)
    return ob

@app.delete("/deleteNote")
def deleteNote(ob : BE.Note):
    ms = MainService()
    ms.deleteNote(ob.nt_id) 
    logger.debug(ob)
    return ob

@app.post("/getUser" )
def getUser(user : BE.User):
    ms = MainService()
    output = ms.getUserByEmail(user.usr_email) 
    if output == None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return output

@app.get("/getUsers" )
def getUsers():
    ms = MainService()
    output = ms.getUsers() 
    if output == None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return output

@app.get("/getLogs" )
def getLogs():
    ms = MainService()
    output = ms.getLogs() 
    if output == None:
        raise HTTPException(status_code=404, detail="Logs Not Found!")
    return output

@app.post("/getPolygon" )
def getPolygon(cam : BE.Camera):
    ms = MainService()
    output = ms.getCameraById(cam.cm_id) 
    if output == None:
        raise HTTPException(status_code=404, detail="Camera Details Not Found!")
    return output

@app.get("/getAllPolygons" )
def getAllPolygons():
    ms = MainService()
    output = ms.getAllCameras() 
    if output == None:
        raise HTTPException(status_code=404, detail="Error!")
    return output

@app.post("/insertOrUpdatePolygon" )
def insertOrUpdatePolygon(cam : BE.Camera):
    ms = MainService()
    print(cam)
    ms.insertOrUpdatePolygon(cam.cm_id, cam.cm_ps_id, cam.cm_polygon) 

@app.post("/insertUser" )
def insertUser(user : BE.User):
    ms = MainService()
    try:
        output = ms.insertUser(user) 
    except Error as e:
        raise HTTPException(status_code=305, detail="Something went wrong...")
    if output == None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return output

@app.post("/insertLog" )
def insertLog(log : BE.Log):
    ms = MainService()
    try:
        output = ms.insertLog(log) 
    except Error as e:
        print (e)
        raise HTTPException(status_code=305, detail="Something went wrong...")
    return output

@app.post("/insertNote" )
def insertNote(note : BE.Note):
    ms = MainService()
    try:
        output = ms.insertNotes(note) 
    except Error as e:
        print (e)
        raise HTTPException(status_code=305, detail="Something went wrong...")
    return output

@app.post("/notify")
def getDataFromContextBroker(body: bytes = Depends(get_body)):
    global data_to_be_sent, list_of_data_to_be_sent
    data_to_be_sent = body.decode('utf8')
    #list_of_data_to_be_sent.append(data_to_be_sent)
    ms = MainService()
    data_to_insert = json.loads(data_to_be_sent)['data']
    data_to_insert = data_to_insert[0]
    if data_to_insert['type'] == 'TrafficViolation':
        try:
            ms.insertTrafficViolation(data_to_insert['id'], data_to_insert['description']['value'],json.dumps(data_to_insert['location']['value']['coordinates']), json.dumps(data_to_insert['seeAlso']['value'][0]))
            value = {"TrafficViolationList": [
                        {
                            "id": data_to_insert['id'],
                            "description": data_to_insert['description']['value'],
                            "location": data_to_insert['location']['value']['coordinates'],
                            "resolved" : 0,
                            "type": "TrafficViolation"
                            }
                    ]
                }
            list_of_data_to_be_sent.append(json.dumps(value))
            logger.debug(list_of_data_to_be_sent)
        except Exception as e:
            print(e)
            #TODO: maybe do something later...
    if data_to_insert['type'] == 'OnStreetParking':
        try:
            ms.insertOnStreetParking(data_to_insert['id'], data_to_insert['description']['value'],json.dumps(data_to_insert['location']['value']['coordinates']), json.dumps(data_to_insert['totalSpotNumber']['value']))
        except Exception as e:
            print(e)
            #TODO: maybe do something later...

    return body


async def sse_generator():
    global list_of_data_to_be_sent, cnt
    deb = False
    if deb is True:
        while True:
            num_items = randint(1, 3)  # Generate a random number of items
            values = []
            for _ in range(num_items):
                value={"id": "ID_"+str(randint(1000000000,9999999999)), "type": "TrafficViolation", "location": {"value": {"type": "Point", "coordinates": fake_coordinates[randint(0, len(fake_coordinates)-1)]}, "type": "GeoProperty"}, "description": {"type": "String", "value": "Illegal parking"}, "seeAlso": {"value": [], "type": "array"}}
                values.append(value)
            yield f"data: {json.dumps(values)}\n\n"
            await asyncio.sleep(randint(1, 5))     
    else:    
        while True:
            if len(list_of_data_to_be_sent) != 0 :
                item = list_of_data_to_be_sent.pop()
                if item is not None:
                    cnt = cnt + 1
                    #message = {'id': cnt,'data': 'data_body'}
                    #message['data'] = item
                    #yield f"data: {json.dumps(message)}\n\n"
                    logger.debug("AICI")
                    logger.debug(item)
                    item = json.loads(item)
                    yield f"data: {json.dumps(item)}\n\n"
            await asyncio.sleep(1)
        # Adjust the sleep interval as needed
    
# Function to generate fake data
async def generate_fake_data():
    while True:
        num_items = randint(1, 3)  # Generate a random number of items
        values = []
        for _ in range(num_items):
            value={"id": "ID_"+str(randint(1000000000,9999999999)), "type": "TrafficViolation", "location": {"value": {"type": "Point", "coordinates": fake_coordinates[randint(0, len(fake_coordinates)-1)]}, "type": "GeoProperty"}, "description": {"type": "String", "value": "Illegal parking"}, "seeAlso": {"value": [], "type": "array"}}
            values.append(value)
        yield f"data: {json.dumps(values)}\n\n"
        await asyncio.sleep(randint(1, 5))  # Sleep for 1 second

# Define an endpoint to stream fake data
@app.get("/sseFake")
async def stream_fake_data(request: Request):
    async def fake_data_generator():
        async for item in generate_fake_data():
            yield item

    return StreamingResponse(fake_data_generator(), media_type="text/event-stream")


# when you want to run in on the host
"""
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
"""    
@app.get("/sse", response_class=StreamingResponse)
async def sse_endpoint(request: Request):
    response = StreamingResponse(sse_generator(), media_type="text/event-stream")
    sse_manager.add_subscription(response)
    logger.info(len(sse_manager.subscriptions))
    # Attach the disconnect event handler
    if await request.is_disconnected():
        sse_manager.remove_subscription(response)
        logger.debug("remove sub")
    
    return response
import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from opentelemetry import trace
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from utils import current_milli_time

# --------------------------------------
# Allows Auto Instrumentation to kick in
# --------------------------------------
PymongoInstrumentor().instrument()

async def do_insert(motor_db, name):
    await motor_db.test_collection.insert_one({
        "id": current_milli_time(),
        "name": name,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    })    

async def talk_to_mongo(name):
    tracer = trace.get_tracer("custom-tracer")
    with tracer.start_as_current_span("talk-to-mongo") as span:        
        motor_client = AsyncIOMotorClient("localhost", 27017)
        motor_db = motor_client["test-database"]
        motor_db["test-collection"]
        loop = motor_client.get_io_loop()
        loop.create_task(do_insert(motor_db, name))
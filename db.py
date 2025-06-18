from motor.motor_asyncio import AsyncIOMotorClient
#MONGO_CLIENT
MONGO_URI = "mongodb+srv://sufyan532011:2011@bey-wars.oji9phy.mongodb.net/?retryWrites=true&w=majority&appName=Bey-Wars"
mongo_client = AsyncIOMotorClient(MONGO_URI)
DB = mongo_client["BEYBLADE"]
#All Database
Users = DB["USERS"]
Banned = DB["BANNED USERS"]
Guilds = DB["GUILDS"]

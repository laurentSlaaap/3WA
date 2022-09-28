import email
from email.mime import base
import os
from fastapi import APIRouter, HTTPException, Depends, Request,status,File, UploadFile
from models.user import User, UserLogin, UserUpdate
from models.melody import Melody, MelodyUpdate
from config.db import client, database, collection_user, collection_melodies
from bson import ObjectId
from config.oauth import get_current_user
from config.jwttoken import create_access_token
from config.hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import serializeDict
from pydantic import BaseModel
from melody_generator.preprocess import main, create_mapping, MAPPING_PATH
from melody_generator.melodygenerator import MelodyGenerator, SEQUENCE_LENGTH
import base64

user = APIRouter()

# Retourne la liste de tout les user
@user.get('/')
async def find_all_users():
    users = []
    allUsers = collection_user.find({})
    async for user in allUsers:
        users.append(User(**user))
    return users

# Retourne la liste de toutes les melodies
@user.get('/melodies')
async def find_all_melodies():
    melodys = []
    allMelodys = collection_melodies.find({})
    async for melody in allMelodys:
        melodys.append(Melody(**melody))
    return melodys

# Get user par son email
@user.get("/{email}")
async def find_one_user_by_email(email):
    user = await collection_user.find_one({"email": email})
    return serializeDict(user)

# Demande de connexion, retourne un token d'acces et l'id du user
@user.post('/login')
async def login(request: UserLogin):
    user = await collection_user.find_one({"email":request.email})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"tokenValue": user["email"] })
    print(user['_id'])
    return {"access_token": access_token, "user_id": str(user['_id'])}

# Creation d'un nouvel user
@user.post("/register")
async def create_user(user: User):
    hashed_pass = Hash.bcrypt(user.password)
    emailTolower = user.email.lower()
    user_object = dict(user)
    user_object["password"] = hashed_pass
    user_object["email"] = emailTolower
    await collection_user.insert_one(user_object, id)
    return {"res":"User created"}

# Mise a jour d'un user existant
@user.put('/{id}')
async def update_user(id:str, user: UserUpdate):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        if 'password' in user:
           user['password'] = Hash.bcrypt(user['password'])
        update_result = await collection_user.update_one({"_id": ObjectId(id)}, {"$set" : user})
        if update_result.modified_count == 1:
            user_updated = await collection_user.find_one({"_id": ObjectId(id)})
            return serializeDict(user_updated)
    if (existing_user := await collection_user.find_one({"_id": ObjectId(id)})) is not None:
        return serializeDict(existing_user)
    raise HTTPException(status_code=404, detail=f"User {ObjectId(id)} not found")

# Suppression d'un user
@user.delete('/{id}')
async def delete_user(id, user: User):
    await collection_user.delete_one({"_id": ObjectId(id)})
    return True

# Supression d'un son
@user.delete('/melody/{id}')
async def delete_melody(id):
    await collection_melodies.delete_one({"_id" : ObjectId(id)})
    return True

class B64Song(BaseModel):
    value : str
    speedFactor: float

#Génération d'une melodie
@user.post('/generateSong/')
async def generateSong(b64Song: B64Song):
    
    b64Song.value = b64Song.value[22:]
    decoded = base64.b64decode(b64Song.value)
    print(b64Song)
    
    int_song = main(decoded)
    # create_mapping(int_song, MAPPING_PATH)
    mg = MelodyGenerator()
    render = mg.generate_melody(int_song, 5000, SEQUENCE_LENGTH, 0.5)
    current_number_of_songs = 0
    for path in os.listdir("songs"):
        # check if current path is a file
        if os.path.isfile(os.path.join('songs', path)):
            current_number_of_songs += 1
    current_number_of_songs += 1
    mg.save_melody(render, file_name=f"songs/song-{current_number_of_songs}.mid", speedFactor=b64Song.speedFactor)
    with open("C:/Users/laurent/Desktop/music_generator/backend/songs/song-"+str(current_number_of_songs)+".mid", "rb") as mid_file:
        melody_object = dict()
        r = base64.b64encode(mid_file.read())
        melody_object["melody_b64"] = r
        await collection_melodies.insert_one(melody_object, id)
        return r


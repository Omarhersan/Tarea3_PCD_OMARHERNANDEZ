import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.encoders import jsonable_encoder



# Duda, por qué preferimos usar la herencia desde BaseModel
# por sobre usar @dataclass?
class User(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: int
    recomendations: List[str]
    ZIP: Optional[int]

def check_id_uniqueness(id: int):
    global general_dict
    #new_key = randint(0,10000)
    if id in general_dict.keys():
        return False
    else:
        return True
    

# Inicialize values in the api
app = FastAPI()
general_dict = {}

@app.post('/create_user/')
async def create_user(user:User):
    new_user = user.model_dump()
    id = user.user_id
    if check_id_uniqueness(id):
        general_dict[id] = new_user
        return f'User {id} created. {user.user_name} is now in out database.'
    else:
        return f'{user.user_name} already exist.'

    
@app.put('/update_user/{user_id}')
async def update_user(user_id: str, user:User):
    user_id = int(user_id)
    # check if user exist bool
    if user_id not in general_dict.keys():
        return f'{user_id} does not exist.'
    
    updated_user = jsonable_encoder(user)
    general_dict[user_id] = updated_user
    return f'updated {user_id}.'

@app.get('/get_user/{user_id}')
async def get_user_info(user_id: str):
    
    user_id = int(user_id)
    # check if user exist bool
    if user_id not in general_dict.keys():
        return f'{user_id} not in our database'

    return general_dict[user_id]

@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: str):
    user_id = int(user_id)
    # check if user exist bool
    if user_id not in general_dict.keys():
        return f'{user_id} not in our database'
    
    popped = general_dict.pop(user_id)
    return f'The following data was deleted: \n {popped}'


if __name__ == "__main__":
    uvicorn.run(app = "main:app", host='0.0.0.0', port=5000, log_level='info', reload=False)
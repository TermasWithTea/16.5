from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')


users = {}


class User(BaseModel):
    username: str
    age: int
    id: int

@app.on_event("stertup")
async def startevent():
    users[1] = User(username='UrbanUser', age=24, id=1)
    users[2] = User(username='UrbanTest', age=22, id=2)
    users[3] = User(username='Capybara', age=60, id=3)

@app.get('/')
async def root(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse('users.html',{'request': request, "users": users.values()})


@app.get('/users/{user_id}')
async def get_reurn(request: Request, user_id: str) -> templates.TemplateResponse:
    user = users[user_id]
    return templates.TemplateResponse('users.html',{'request': request, 'users': users.values()})


@app.post('user/{username}/{age}')
async def post_ret(username: str, age: int) -> User:
    user_id = max(list(users.keys()), default=0) + 1
    user = User(username=username, age=age)
    users[user_id] = user
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: int, username: str, age: int) -> User:
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User was not found')
    user = User(username=username, age=age, id=user_id)
    users[user_id] = user
    return user


@app.delete('/user/{user_id}')
async def del_del(user_id: int) -> User:
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User was not found')

    del_del = users[user_id]
    del users[user_id]
    return del_del
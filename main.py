from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ctypes
import pathlib
import random

#sudo uvicorn main:app --host 0.0.0.0 --port 80 --ssl-keyfile=/etc/letsencrypt/live/spacequest.site/privkey.pem --ssl-certfile=/etc/letsencrypt/live/spacequest.site/fullchain.pemscre
#ssh alexander@64.225.77.42
app = FastAPI()
origins = [
    "http://localhost",
    "https://localhost:10888",
    "https://aprilquest.rogachev-a-v.now.sh"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

libname = pathlib.Path().absolute() / "libspacecraft.so"
c_lib = ctypes.CDLL(libname)
c_lib.CommonCalculations.restype = ctypes.c_void_p

#typedef struct
#{
#    bool resultSecondStep;
#    bool isSolution;
#    double hTurnOnEngineKm;
#    double engineForceNewtons;
#    double spacecraftMass;
#    double deltaT2Sec;
#    double V2MSec;
#    double fuelCostKg;
#} commonSolution;

class commonSolution(ctypes.Structure):
    _fields_ = [("resultSecondStepbool", ctypes.c_bool),
                ("isSolution", ctypes.c_bool ),
                ("hTurnOnEngineKm", ctypes.c_double),
                ("engineForceNewtons", ctypes.c_double),
                ("spacecraftMass", ctypes.c_double),
                ("deltaT2Sec", ctypes.c_double),
                ("V2MSec", ctypes.c_double),
                ("fuelCostKg", ctypes.c_double)]


#extern "C" {
#    commonSolution CommonCalculations(double, double);
#}


team_id = [i for i in range(1000, 100000)]  # быдлокод для выдачи рандомных АЙДИ командам - между с и с + 1 стоял await
random.shuffle(team_id)  # и двум командам бот дал один айди - никогда так не пишите и не делайте. Используйте
c = 0  # dp.storage.place("counter", counter) и его асинхронные методы .get и .update, тогда накладок не будет

USERS = {1828404201: 'shh'}  # schema - id: lead, user, agent, lead_choose, user_choose, new, ...
FORM = {} # schema - team_id: {1:0,2:} - dict if dicts
TEAMS = {}  # schema - team_id: team_name
LEADS = {}  # schema - user_id: team_id
MARKS = {}  # schema - team_id: {1:0,2:} - dict if dicts
FORM = {}
AGENTS = {}  # schema - id: stage
PROGRESS = {}  # schema - user_id: 1..10 idle - удобнейшая идея чтобы учитывать состояние человека в боте. На деле в
LEAGUE = {}  # schema: team_id: 1,2 or 3  ботах для телеграма есть МАШИНЫ СОСТОЯНИЙ, но я не смог их натянуть на бота ВК
ADMINS = {}
STORAGE = {} # can storage everything!

#@dp.message_handler(IsLeadChoose(True))  # обработка названий команды.
#async def handle_lead_chooses_team_name(message: types.Message, data: dict):
#    global c
#    USERS[message.from_id] = "league"
#    TEAMS[team_id[c]] = message.text
#    LEADS[message.from_id] = team_id[c]  # сам себе капитан
#    MARKS[team_id[c]] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
#    await message.answer("Ура, команда %s зарегистрирована!\n Осталось указать лигу и регистрация окончена. "
#                         "Чтобы члены твоей команды смогли к тебе присоединиться, "
#                         "пусть нажмут кнопку \"Я участник\" и напишут мне этот код: \n%s" %
#                         (TEAMS[team_id[c]], team_id[c]),
#                         keyboard=kb_league.get_keyboard())
#    c = c + 1


#@dp.message_handler(IsUserChoose(True))  # обработка названий команды
#async def handle_user_choose_team(message: types.Message, data: dict):
#    if int(message.text) in LEADS.values():
#        LEADS[message.from_id] = int(message.text)
#        USERS[message.from_id] = 'user'
#        await message.answer("Отлично, теперь вы член команды %s. Бегом в игру!" % TEAMS[int(message.text)],
#                             keyboard=kb_main.get_keyboard())
#    else:
#        await message.answer("Перепроверь, у капитана точно %s? Напиши мне как у него!" % message.text)



@app.get("/kk")
async def root():

    #answer = c_lib.CalcFuelCostKg(ctypes.c_float(100.0), ctypes.c_float(200.0))
    #print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
    return {"message": c_lib.CalcFuelCostKg(ctypes.c_double(1.0), ctypes.c_double(1.0))}


@app.get("/is_new_player/{id}")
async def read_item(id : int): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if id not in USERS.keys():
        return {"command_name": 'true'}
    else:
        return {"command_name": 'false'}

@app.get("/form_get/{id}/{com_name}/{planet}/{cb1}/{cb2}/{cb3}/{cb4}/{cb5}/{cb6}/{text1}/{text2}")
async def form_get(id : int, com_name: str, planet, cb1, cb2, cb3, cb4, cb5, cb6, text1: str, text2: str ): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if id not in USERS.keys():
        USERS[id] = 'user'
    if id not in FORM.keys():
        FORM[id] = {'status': 'new', 'com_name': com_name, 'planet': planet, 'cb1': cb1, 'cb2': cb2, 'cb3': cb3, 'cb4': cb4, 'cb5': cb5, 'cb6': cb6, "text1": text1, 'text2': text2}
    return FORM[id]


@app.get("/form_put/{id}/{com_name}/{planet}/{cb1}/{cb2}/{cb3}/{cb4}/{cb5}/{cb6}/{text1}/{text2}")
async def form_put(id : int, com_name: str, planet, cb1, cb2, cb3, cb4, cb5, cb6, text1: str, text2: str ): # http://127.0.0.1:8000/items/1234.09/kek is valid
    FORM[id] = {'status': 'change', 'com_name': com_name, 'planet': planet, 'cb1': cb1, 'cb2': cb2, 'cb3': cb3, 'cb4': cb4, 'cb5': cb5, 'cb6': cb6, 'text1': text1, 'text2': text2}
    return FORM[id]

@app.get("/items/{item_id}/{name}")
async def items(item_id : float, name: str): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"item_id": item_id, "command_name": name}

@app.get("/get_marks/{id}")
async def read_item(id : int): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"user_marks": MARKS[id]}

@app.get("/get_storage/{id}")
async def get_storage(id : int): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"user_marks": STORAGE[id]}

@app.get("/set_mark/{id}/{riddle_number}/{mark}")
async def rset_mark(id : int, riddle_number, mark): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if id not in MARKS.keys():
        MARKS[id] = {}
    MARKS[id][riddle_number] = mark
    return {"user_marks": MARKS[id]}

@app.get("/storage/{id}/{riddle_number}/{mark}")
async def storage(id : int, riddle_number, mark): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if id not in STORAGE.keys():
        STORAGE[id] = {}
    STORAGE[id][riddle_number] = mark
    return {"user_storage": STORAGE[id]}

@app.get("/admin/form")
async def admin_form(): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"Forms_data": FORM}


@app.get("/admin/users")
async def admin_users(): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"User_ids": USERS}


@app.get("/admin/marks")
async def admin_marks(): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"MARKS": MARKS}

@app.get("/admin/storage")
async def admin_storage(): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"STORAGE": STORAGE}


@app.get("/admin/all")
async def admin_all(): # http://127.0.0.1:8000/items/1234.09/kek is valid
    return {"Forms_data": FORM, "User_ids": USERS, "MARKS": MARKS, "STORAGE": STORAGE}


@app.get("/delete/form/{id}/{key}")
async def delete_form(id : int, key): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if key != 'kamaz23':
        return {"Suck your": 'tits'}
    else:
        del FORM[id]
        return {"is_deleted": 'done', 'form_data': FORM}

@app.get("/delete/users/{id}/{key}")
async def delete_users(id : int, key): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if key != 'kamaz23':
        return {"Suck your": 'tits'}
    else:
        del USERS[id]
        return {"is_deleted": 'done', 'users_data': USERS}

@app.get("/delete/marks/{id}/{key}")
async def delete_marks(id : int, key): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if key != 'kamaz23':
        return {"Suck your": 'tits'}
    else:
        del MARKS[id]
        return {"is_deleted": 'done', 'marks_data': MARKS}

@app.get("/delete/storage/{id}/{key}")
async def delete_storage(id : int, key): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if key != 'kamaz23':
        return {"Suck your": 'tits'}
    else:
        del STORAGE[id]
        return {"is_deleted": 'done', 'storage_data': STORAGE}


@app.get("/sandstorm/storage/{id}/{key}")
async def sandstorm(id : int, key): # http://127.0.0.1:8000/items/1234.09/kek is valid
    if key != 'kamaz23kamaz23':
        return {"Suck your": 'tits'}
    else:
        FORM = {} # schema - team_id: {1:0,2:} - dict if dicts
        TEAMS = {}  # schema - team_id: team_name
        LEADS = {}  # schema - user_id: team_id
        MARKS = {}  # schema - team_id: {1:0,2:} - dict if dicts
        FORM = {}
        AGENTS = {}  # schema - id: stage
        PROGRESS = {}  # schema - user_id: 1..10 idle - удобнейшая идея чтобы учитывать состояние человека в боте. На деле в
        LEAGUE = {}  # schema: team_id: 1,2 or 3  ботах для телеграма есть МАШИНЫ СОСТОЯНИЙ, но я не смог их натянуть на бота ВК
        ADMINS = {}
        STORAGE = {}
        return {"is_sandstormed": 'done'}


#if __name__ == "__main__":
    # Load the shared library into ctypes
#    libname = pathlib.Path().absolute() / "libspacecraft.so"
#    c_lib = ctypes.CDLL(libname)

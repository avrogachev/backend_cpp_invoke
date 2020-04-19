from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ctypes
import pathlib

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

class commonSolution(ctypes.Structure):
    _fields_ = [("resultSecondStep", ctypes.c_bool),
                ("isSolution", ctypes.c_bool ),
                ("hTurnOnEngineKm", ctypes.c_double),
                ("engineForceNewtons", ctypes.c_double),
                ("spacecraftMass", ctypes.c_double),
                ("deltaT2Sec", ctypes.c_double),
                ("V2MSec", ctypes.c_double),
                ("fuelCostKg", ctypes.c_double)]

libname = pathlib.Path().absolute() / "libspacecraft.so"
c_lib = ctypes.CDLL(libname)
c_lib.CommonCalculations.restype = commonSolution


@app.get("/")
async def root():
    return {"message": 'API обвязки С++'}

@app.get("/space/{H}/{F}")
async def space(H : float, F: float):
    answer = c_lib.CommonCalculations(ctypes.c_double(H), ctypes.c_double(F))
    return {"resultSecondStep": answer.resultSecondStep, "isSolution": answer.isSolution,
    "hTurnOnEngineKm": answer.hTurnOnEngineKm, "engineForceNewtons": answer.engineForceNewtons,
    "spacecraftMass": answer.spacecraftMass, "deltaT2Sec": answer.deltaT2Sec, "V2MSec": answer.V2MSec, "fuelCostKg": answer.fuelCostKg}

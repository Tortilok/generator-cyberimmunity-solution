from fastapi import FastAPI
from pydantic import BaseModel
from visual.pages.router import router as router_pages
from gen_template import gen

class Module(BaseModel):
    name: list | None = None #название полное на русском языке
    tag: list | None = None #его название которое будет использоваться в коде
    #func: list | None = None #список его функций
    #func_desc: list | None = None #описание его функций
    #dst: list | None = None #исходящая связь к другим модулям

class Solution(BaseModel):
    name_solution: str | None = "test"
    module: Module | None = None

app = FastAPI(
    title="Gyberimmunity prototype"
)

@app.post("/get_module")
def get_module(modules:list[Module]):
    return {"message": modules}

@app.post("/create_solution")
def get_module(modules: Solution):
    with open('data.json', 'w') as file:
        file.write(modules.model_dump_json())
        file.close()
    status = gen()
    return {"message": status}

app.include_router(router_pages)


from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="visual/templates")

@router.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

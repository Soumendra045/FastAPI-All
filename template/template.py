from fastapi import APIRouter, Request,BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import ProductBase
from custom_log import log

router = APIRouter(
    prefix='/template',
    tags=['templates']
)

templates = Jinja2Templates(directory='template')

@router.post('/products/{id}', response_class=HTMLResponse)
def get_product(id: str,product: ProductBase, request: Request,bt:BackgroundTasks):
    bt.add_task(log_template_call,f'Template read for product')
    return templates.TemplateResponse(
        "product.html",
        {
            'request': request,
            'id': id,
            'title': product.title,
            'description': product.description,
            'price': product.price
        }
    )

def log_template_call(message: str):
    log('MyApi',message)
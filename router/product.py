from fastapi import APIRouter,Header,Form
from fastapi.responses import Response,HTMLResponse,PlainTextResponse
from typing import Optional,List
from custom_log import log
import time

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch','camera','phone']

async def time_consumeing_functionality():
    time.sleep(5)
    return 'ok'


@router.post('/new')
def create_product(name: str=Form(...)):
    products.append(name)
    return products

@router.get('/all')
async def get_all_products():
    # log("my Api","call to get all log")
    await time_consumeing_functionality()
    
    data = " ".join(products)
    
    response= Response(content=data,media_type='text/plain')
    response.set_cookie(key='test-cookie',value='test_cookie_value')
    return response

@router.get('/withHeader')
def get_products(response: Response,
                custom_header:Optional[List] = Header(None)
                ):
    response.headers['custom_response_header']= ",".join(custom_header)
    return products

@router.get('/{id}',responses={
    200:{
        'content':{
            'text/html':{
                'example':'<div>product</div>'
            }
        },
        'description':'Return htnl response'
    },
    404:{
        'content':{
            'text/plain':{
                'example':'Product are not avilable'
            }
        },
        'description':'Return plain text'
    }
})
def get_product(id: int):
    if id>len(products):
        out = 'Product are not avilable'
        return PlainTextResponse(status_code=404,content=out,media_type='text/plain')
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
                .product {{
                    width: 500px;
                    height: 30px;
                    border: 2px inset green;
                    background-color: lightblue;
                    text-align: center;
                    line-height: 30px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="product">{product}</div>
        """
    return HTMLResponse(content=out,media_type="text/html")
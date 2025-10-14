from fastapi import APIRouter,status,Response
from enum import Enum
from typing import Optional

router=APIRouter(
    prefix='/blog',
    tags=['blog']
)


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"


@router.get( 
        "/all",
        summary='Retrive all blogs',
        description='This is api called retiving and fetching data',
        response_description='Here we have all list of blogs'
        )
def get_all_blog(page: Optional[int] = None, page_size=10):
    return {"message": f"All {page} of {page_size}"}


@router.get("/{id}/comments/{comment_id}",tags=['comment'])
def get_comment(
    id: int, comment_id: int, valid: bool = True, username: Optional[str] = None
):
    """
    Simulates retriving a comment of a blog

    - **id
    - ***comment
    - ****valid --optional
    - ******username --optional
    """
    return {
        "message": f"blod{id},comment{comment_id},valid {valid},username {username}"
    }


@router.get("/type/{type}")
def get_blog_type(type: BlogType):
    return {"message": f"Blog type {type}"}


@router.get("/{id}",status_code=status.HTTP_200_OK)
def get_blog(id: int,response:Response):
    if id>5:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message": f"blog with id {id} not found"}
    else:
        return {'message':f'Blog with id {id}'}

from fastapi import APIRouter, Query, Body,Path
from pydantic import BaseModel
from typing import Optional,List

router = APIRouter(prefix="/blog", tags=["blog"])


class BlogModel(BaseModel):
    title: str
    content: str
    publisher: Optional[bool] = True
    nb_comment: int


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"id": id, "data": blog, "version": version}


@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: str = Query(
        None,
        title="This is a comment",
        description="Some description for comment_id",
        alias="CommentTitle",
        deprecated=True,
    ),
    content: str = Body(
        ...,
        min_length=10,
        max_length=20,
    ),
    v:Optional[List[str]]=Query(None),
    comment_id: int = Path(...,gt=1,lt=10)
):
    return {"blog": blog, "id": id, "comment_id": comment_title, "content": content}

from schemas import ArticleBase
from sqlalchemy.orm.session import Session
from db.models import DbArticle
from fastapi import HTTPException,status
from exceptions import StoryException
def create_article(db: Session,request:ArticleBase):
    if request.content.startswith('Once upon a time'):
        raise StoryException('No stories Please')
    new_aricle = DbArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id
    )
    db.add(new_aricle)
    db.commit()
    db.refresh(new_aricle)
    return new_aricle

def get_article(db:Session,id):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Article with id {id} is not found')
    return article
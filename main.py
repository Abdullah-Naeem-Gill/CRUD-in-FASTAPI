from fastapi import FastAPI , Depends , status , Response,  HTTPException
import models
import schemas
from database import engine , SessionLocal
from sqlalchemy.orm import Session

app= FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 
models.Base.metadata.create_all(engine)
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.blog,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'done'




@app.get('/blog')
def read(db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}',status_code=200)
def show(id,response:Response, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} is not available"}

    return blog


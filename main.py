from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel
from database import engine,SessionLocal
from typing import Annotated
import auth
from auth import get_current_user

#jd 789
#sanketp25 123
app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()    

#db_dependency = Annotated(Session,Depends(get_db))
lead_dependency = Annotated[dict,Depends(get_current_user)]



@app.get("/",status_code=status.HTTP_200_OK)
async def get_leads(lead:lead_dependency,db:Session=Depends(get_db)):
    if lead is None:
        raise HTTPException(status_code=401)
    leads = db.query(models.Leads).all()
    return {'Lead':leads}

@app.get("/{id}",status_code=status.HTTP_200_OK)
async def get_leads_byId(lead_id:int,lead:lead_dependency,db:Session=Depends(get_db)):
    if lead is None:
        raise HTTPException(status_code=401)
    lead = db.query(models.Leads).filter(models.Leads.id == lead_id).first()
    if lead is None:
        raise HTTPException(
            status_code=404,
            detail=f'Lead: {lead_id}, does not exist in DB'
        )
    return {'Lead Name':lead.first_name.capitalize()+' '+lead.last_name.capitalize(),'Lead Email': lead.email, 'Lead State': lead.state}

@app.delete('/{lead_id}')
def delete_lead(id:int,lead:lead_dependency ,db: Session=Depends(get_db)):
    if lead is None:
        raise HTTPException(status_code=401)
    lead_model = db.query(models.Leads).filter(models.Leads.id == id).first()
    if lead_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Lead: {id}, does not exist in DB'
        )
    db.query(models.Leads).filter(models.Leads.id == id).delete()
    db.commit()

@app.put('/{lead_id}')
def update_leads(id:int,lead:lead_dependency ,db: Session=Depends(get_db)):
    if lead is None:
        raise HTTPException(status_code=401)
    lead_model = db.query(models.Leads).filter(models.Leads.id == id).first()
    if lead_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Lead: {id}, does not exist in DB'
        )
    lead_model.state = 'REACHED_OUT'
    db.commit()



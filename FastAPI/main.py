# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()
pickle_in = open("model.pkl", "rb")
model = pickle.load(pickle_in)

#bookworm class
class Bookworm(BaseModel):
    gender: int
    amount_purchased: int
    frequency: int
    last_purchase: int
    first_purchase: int
    p_child: int
    p_youth: int
    p_cook: int
    p_diy: int
    p_art: int


templates = Jinja2Templates(directory = 'htmldirectory')

#root route
@app.get("/")
async def root():
    return {"Hi Stef, welcome to my first API!"}

#html route, after home, add your name :)
@app.get("/home/{user_name}", response_class=HTMLResponse)
async def write_home(request: Request, user_name: str):
    return templates.TemplateResponse("index.htm", {"request": request, "username": user_name})


@app.post("/submitform")
async def handle_form(assignment: str = Form(...)):
    df = pd.read_excel(assignment)
    df.columns = map(str.lower, df.columns)
    df_=df.drop(['name', 'address', 'choice', 'observation'], axis=1)
    preds = pd.DataFrame(model.predict(df_), columns=['mail'])
    df_final=pd.concat([df, preds], axis=1)
    mail_index=(df_final['mail']==1)
    mailing_list=df_final[mail_index]
    mail_list=mailing_list[['name', 'address']]
    
    # please change the path to your local machine for this to work
    return(mail_list.to_excel(r'C:\Users\Anthony\Desktop\FastAPI\mailing_list.xlsx', index=False))

#prediction route, this was the first form of predictions i achieved. this was obviously not ideal :)
@app.post('/predict')
async def predict_type(data:Bookworm):
    data = data.dict()
    gender = data['gender']
    amount_purchased = data['amount_purchased']
    frequency = data['frequency']
    last_purchase = data['last_purchase']
    first_purchase = data['first_purchase']
    p_child = data['p_child']
    p_youth = data['p_youth']
    p_cook = data['p_cook']
    p_diy = data['p_diy']
    p_art = data['p_art']
    
    prediction = model.predict([[gender,
                                 amount_purchased,
                                 frequency,
                                 last_purchase,
                                 first_purchase,
                                 p_child,
                                 p_youth,
                                 p_cook,
                                 p_diy,
                                 p_art]])
    if prediction[0] > 0.5:
        prediction = 'Send mailer'
    else:
        prediction = 'Don\'t solicite'
    return{
        'prediction': prediction
    }




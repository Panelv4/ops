from fastapi import FastAPI
app=FastAPI(title='OpsPilotAI')
@app.get('/')
def root():
    return {'status':'ok','message':'OpsPilotAI backend running'}

from fastapi import FastAPI
from app.schemas import InputData
from app.worker import run_batched_prediction, start_batch_worker

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    start_batch_worker()  

@app.post("/predict")
async def predict(flow: InputData):
    flow_id = flow.FlowID
    prediction = await run_batched_prediction(flow)
    return {"FlowID": flow_id, "Prediction": prediction}

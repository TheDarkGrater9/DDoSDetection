import asyncio
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Any
from app.utils import load_artifacts, preprocess_input

MAX_WORKERS = 6
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

async def run_prediction(input_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _predict_sync, input_data)

def _predict_sync(data):
    processed = preprocess_input(data)
    model, _ = load_artifacts()
    pred = model.predict(processed)[0]
    return "BENIGN" if pred == 0 else "DDOS"

BATCH_QUEUE = asyncio.Queue()
BATCH_SIZE = 32        
BATCH_TIMEOUT = 0.05   

class BatchItem:
    def __init__(self, data, future):
        self.data = data
        self.future = future

async def run_batched_prediction(input_data):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await BATCH_QUEUE.put(BatchItem(input_data, future))
    return await future  

async def _batch_worker():
    while True:
        batch_items = []
        try:
            item = await BATCH_QUEUE.get()
            batch_items.append(item)

            for _ in range(BATCH_SIZE - 1):
                try:
                    item = await asyncio.wait_for(BATCH_QUEUE.get(), timeout=BATCH_TIMEOUT)
                    batch_items.append(item)
                except asyncio.TimeoutError:
                    break  

            inputs = [item.data for item in batch_items]
            processed = [preprocess_input(data) for data in inputs]
            model, _ = load_artifacts()
            batch_df = model.predict(np.vstack(processed))

            for item, pred in zip(batch_items, batch_df):
                label = "BENIGN" if pred == 0 else "DDOS"
                item.future.set_result(label)

        except Exception as e:
            for item in batch_items:
                if not item.future.done():
                    item.future.set_exception(e)

def start_batch_worker():
    asyncio.create_task(_batch_worker())

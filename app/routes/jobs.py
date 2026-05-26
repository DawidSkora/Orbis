from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

def heavy_job(name: str):
    import time
    time.sleep(3)
    print(f"Done processing: {name}")  # visible in server terminal

@router.post("/process")
def process(name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(heavy_job, name)
    return {"status": "started", "job": name}

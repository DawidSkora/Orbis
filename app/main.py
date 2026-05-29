import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import data, debug, messages, jobs, qa, gallery, auth, admin_gallery

app = FastAPI(title="Orbis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    print(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response

app.include_router(debug.router,    prefix="/debug")
app.include_router(data.router,     prefix="/data")
app.include_router(messages.router, prefix="/messages")
app.include_router(jobs.router,     prefix="/jobs")
app.include_router(qa.router,       prefix="/qa")
app.include_router(gallery.router,  prefix="/gallery")
app.include_router(auth.router,       prefix="/auth")
app.include_router(admin_gallery.router, prefix="/admin/gallery")
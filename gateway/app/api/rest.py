from fastapi import FastAPI, Query

from gateway.app.detection_repo import DetectionRepo


def build_app(repo: DetectionRepo) -> FastAPI:
    app = FastAPI(
        title="Fusion Gateway",
        description="Fusion Gateway API",
        version="1.0.0",
    )

    @app.get('/detections')
    async def get_detections(source: str = "fused", limit: int = Query(50, le=500)):
        detections = repo.list_recent(source=source, limit=limit)
        return detections

    @app.get("/healthz", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    return app

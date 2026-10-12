"""Prometheus metrics instrumentation."""
from prometheus_client import Counter, Gauge, Histogram, start_http_server, generate_latest
from fastapi import FastAPI
from fastapi.responses import Response

TRACKS_ACTIVE = Gauge("retailsense_tracks_active", "Current number of active tracks")
FUSION_LATENCY = Histogram("retailsense_fusion_latency_seconds", "Sensor fusion latency")
SENSOR_ERRORS = Counter("retailsense_sensor_errors_total", "Sensor errors", ["sensor_type"])
CAMERA_FPS = Gauge("retailsense_camera_fps", "Camera frames per second", ["camera_id"])
BLIND_SPOT_PREDICTIONS = Gauge("retailsense_blind_spot_predictions", "Active predictions in blind spots")

def start_metrics_server(port: int = 8001):
    """Start Prometheus metrics HTTP server."""
    start_http_server(port)

def metrics_endpoint():
    """FastAPI-compatible metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")
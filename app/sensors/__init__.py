"""Sensor adapter base and implementations."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class SensorAdapter(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_measurement(self) -> Dict[str, Any]:
        """Return timestamped measurement with confidence."""
        pass

class CameraAdapter(SensorAdapter):
    def start(self):
        # TODO: RTSP / OpenCV capture + detection
        pass

    def get_measurement(self):
        return {"type": "camera", "position": None, "confidence": 0.0}

class AudioAdapter(SensorAdapter):
    def start(self):
        # TODO: Energy / DOA
        pass

    def get_measurement(self):
        return {"type": "audio", "energy": 0.0, "doa": None}

class BLEAdapter(SensorAdapter):
    def start(self):
        # TODO: bleak RSSI scanning
        pass

    def get_measurement(self):
        return {"type": "ble", "rssi": None, "distance_estimate": None}

class EnvironmentalAdapter(SensorAdapter):
    def start(self):
        # TODO: MQTT or serial for CO/fire
        pass

    def get_measurement(self):
        return {"type": "environmental", "co_ppm": 0, "fire_detected": False}
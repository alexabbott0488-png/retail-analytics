[README.md](https://github.com/user-attachments/files/33358430/README.md)
# RetailSense

**Open-source multi-sensor retail analytics platform** for real-time customer and product tracking, interaction analysis, and behavior prediction. Designed to run on existing security cameras and additional sensors, with the long-term goal of reducing or replacing physical anti-theft devices.

RetailSense fuses video, audio, Bluetooth Low Energy (BLE), and environmental sensors so tracks continue even when people enter camera blind spots or move behind fixtures.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](docker-compose.yml)
[![Prometheus](https://img.shields.io/badge/Prometheus-metrics-orange.svg)](monitoring/)

## Features

- **Multi-edition architecture**
  - **Operator** — Clean, simple dashboard for store staff (alerts, live tracks, status)
  - **Admin** — Zone editor, sensor management, rules, and direct Grafana access
  - **Developer** — Debug overlays, raw event streams, plugin reloading, and full metrics
- **Probabilistic sensor fusion** — Kalman / particle filter tracking with constant-velocity prediction through camera occlusions and blind spots
- **Privacy-by-design** — Anonymous track IDs, face blurring, no raw audio or BLE storage by default, edge processing
- **Monitoring & alerting** — Prometheus metrics scraped by a separate Grafana stack (Admin and Developer editions only)
- **Modular sensors** — Pluggable adapters for camera (RTSP), audio, BLE proximity, and environmental (CO/fire) sensors
- **Deployment flexible** — Docker Compose on Rocky Linux (SELinux-aware); designed for bare-metal Kubernetes or cloud (EKS/AKS/GKE)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Rocky Linux (or other RHEL-compatible) recommended for production; SELinux should remain enforcing
- Optional: NVIDIA Container Toolkit if using GPU inference

### Run the Application

```bash
git clone https://github.com/your-org/retail-analytics.git
cd retail-analytics

# Operator edition (default)
docker compose up -d

# Or choose an edition
EDITION=admin docker compose up -d
EDITION=developer docker compose up -d
```

### Run the Monitoring Stack (optional)

```bash
cd monitoring
docker compose up -d
```

### Access

| Service              | URL                        | Notes                                      |
|----------------------|----------------------------|--------------------------------------------|
| Application UI       | http://localhost:8080      | Operator / Admin / Developer               |
| API                  | http://localhost:8000      |                                            |
| Prometheus metrics   | http://localhost:8001/metrics |                                            |
| Grafana              | http://localhost:3000      | Default login: `admin` / `admin`           |
| MQTT                 | localhost:1883             |                                            |

On Rocky Linux, volume mounts use the `:z` SELinux flag so containers can access host directories while SELinux remains enforcing.

## Editions

Control the edition with the `EDITION` environment variable or the corresponding config file.

| Feature                    | Operator | Admin | Developer |
|----------------------------|----------|-------|-----------|
| Live tracks & alerts       | Yes      | Yes   | Yes       |
| Zone editing               | No       | Yes   | Yes       |
| Sensor configuration       | Limited  | Full  | Full      |
| Grafana dashboard link     | No       | Yes   | Yes       |
| Debug overlays / raw events| No       | No    | Yes       |
| Plugin / model reload      | No       | No    | Yes       |

## Architecture Overview

```
Sensors (Camera, Audio, BLE, Environmental)
        ↓
Measurement Adapters (timestamped, zone-aware, confidence)
        ↓
MQTT Event Bus
        ↓
Fusion Engine (Kalman / Particle Filter + Prediction)
        ↓
Edition-specific UI + Event Log
        ↓
Prometheus /metrics  →  Grafana (separate stack)
```

Tracks persist through camera blind spots using audio energy/DOA and BLE RSSI updates. Environmental sensors can raise high-priority safety events that influence prediction confidence.

## Sensors

| Sensor        | Primary Role                          | Blind-spot Continuity | Notes                              |
|---------------|---------------------------------------|-----------------------|------------------------------------|
| Camera        | Detection, tracking, pose, zones      | No                    | RTSP from existing security cameras |
| Audio         | Energy / Direction of Arrival         | Yes                   | Microphone arrays or zone energy   |
| BLE           | RSSI proximity / zone presence        | Yes                   | Kalman-smoothed distance estimates |
| Environmental | CO, fire, temperature                 | Context               | Safety prioritization              |

## Configuration

Edition-specific behavior is controlled by YAML files in `configs/`:

- `base.yaml` — Shared defaults (privacy, fusion limits)
- `operator.yaml` — Restricted UI
- `admin.yaml` — Full configuration + Grafana link
- `developer.yaml` — Debug mode + Grafana link

Key privacy defaults (override only with explicit intent):

```yaml
privacy:
  blur_faces: true
  store_raw_audio: false
  anonymize_tracks: true
```

## Monitoring

The application exposes Prometheus metrics at `/metrics` (port 8001 by default):

- `retailsense_tracks_active`
- `retailsense_fusion_latency_seconds`
- `retailsense_sensor_errors_total`
- `retailsense_camera_fps`
- `retailsense_blind_spot_predictions`

Example alerts (see `monitoring/prometheus/alerts.yml`):

- High fusion latency (p95 > 200 ms)
- Sensor error rate spike
- Camera FPS drop
- Unexpected track loss

## Deployment Options

| Option                        | Best For                          | Notes                                      |
|-------------------------------|-----------------------------------|--------------------------------------------|
| Docker Compose                | Pilot / single store / edge       | Current default; SELinux-aware             |
| Bare-metal Kubernetes         | On-prem multi-node, HA            | Persistent volumes, resource isolation     |
| Cloud (EKS / AKS / GKE)       | Multi-store scale, managed ops    | Managed Prometheus/Grafana, elastic scale  |
| Hybrid                        | Edge inference + cloud analytics  | Models and selective data only to cloud    |

## Privacy & Compliance

RetailSense is designed for privacy-preserving operation:

- Anonymous track identifiers (no biometric storage)
- Face blurring enabled by default
- Raw audio and BLE identifiers are not stored
- Processing occurs at the edge by default
- Configurable retention and audit logging for the Admin edition

Operators are responsible for complying with local surveillance, biometric, and audio recording laws.

## Development

```bash
# Developer edition with live source mount
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

See `docs/CONTRIBUTING.md` for contribution guidelines. New sensors should implement the `SensorAdapter` interface. All editions share the same core fusion and metrics code.

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.

## Roadmap

- [ ] Full Streamlit / FastAPI operator and admin UIs
- [ ] Production Kalman / particle filter implementation
- [ ] Camera coverage polygon editor
- [ ] Grafana dashboard provisioning
- [ ] Kubernetes Helm chart
- [ ] Optional learned trajectory predictor
- [ ] Multi-camera handoff

---

**RetailSense** — Continuous awareness, even when cameras can't see.

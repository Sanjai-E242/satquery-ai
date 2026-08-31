# SATQUERY AI — Production Deployment Guide

## 1. Primary Architecture Overview

```
USER BROWSER
    │
    ▼
VERCEL (Edge / Serverless CDN)  ──► https://frontend-ten-inky-48.vercel.app
    │
    ├─► Next.js 14 App Router Frontend (`/`)
    │
    └─► API Proxy / Dynamic Client Calls (`/api/*`)
            │
            ▼
    FASTAPI BACKEND HOST (Render / Railway / Docker / Cloud VM)
            │
            ├─► AI Model Routing & Dynamic Inference (Florence-2, ResNet-18, Fusion Attention)
            ├─► Geospatial Metadata & Multi-Modal Dataset Service (Sentinel-2, Sentinel-1 SAR)
            ├─► Confidence Engine Calibration (`[0.60, 0.99]`)
            └─► Automated PDF & JSON Intelligence Dossier Reporting
```

---

## 2. Live Deployed Endpoints

- **Vercel Production Frontend:** [`https://frontend-ten-inky-48.vercel.app`](https://frontend-ten-inky-48.vercel.app)
- **Vercel Project Dashboard:** `https://vercel.com/sanjai-e242s-projects/frontend`
- **GitHub Repository:** [`https://github.com/Sanjai-E242/satquery-ai.git`](https://github.com/Sanjai-E242/satquery-ai.git)
- **Local Development Frontend:** `http://localhost:3000`
- **Local Development Backend:** `http://127.0.0.1:8000`

---

## 3. Environment Variables Specification

### Frontend (`frontend/.env.local` / Vercel Environment Variables)
| Variable | Description | Example (Production) | Default (Local) |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Public-facing URL of the deployed FastAPI backend | `https://satquery-ai-backend.onrender.com` | `http://127.0.0.1:8000` |
| `BACKEND_API_URL` | Server-side App Router proxy target URL | `https://satquery-ai-backend.onrender.com` | `http://127.0.0.1:8000` |

### Backend (`backend/.env` / Host Environment Variables)
| Variable | Description | Example (Production) | Default (Local) |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | Service Identifier | `SATQUERY AI` | `SATQUERY AI` |
| `FRONTEND_URL` | Allowed origin for CORS | `https://frontend-ten-inky-48.vercel.app` | `http://localhost:3000` |
| `DEMO_MODE` | Active PyTorch VLM inference mode | `true` | `true` |
| `MODEL_DEVICE` | Hardware device allocation | `cpu` or `cuda` | `auto` |
| `MAX_UPLOAD_SIZE_MB` | Maximum allowed payload upload size | `50` | `50` |

---

## 4. Frontend Deployment to Vercel

The frontend is deployed on Vercel with:
- **Root Directory:** `frontend`
- **Framework Preset:** `Next.js`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Production URL:** `https://frontend-ten-inky-48.vercel.app`

---

## 5. Backend Deployment (Render / Docker / Railway)

### Deploying with Docker
```bash
# Build the production container
docker build -t satquery-ai-backend .

# Run container exposing port 8000
docker run -p 8000:8000 -e FRONTEND_URL="https://frontend-ten-inky-48.vercel.app" satquery-ai-backend
```

### Deploying on Render (using `render.yaml`)
1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect `https://github.com/Sanjai-E242/satquery-ai.git`.
3. Render automatically reads `render.yaml`:
   - **Environment:** `Python 3.9+`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set `FRONTEND_URL` to `https://frontend-ten-inky-48.vercel.app`.

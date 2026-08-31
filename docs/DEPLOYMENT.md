# SATQUERY AI — Production Deployment Guide

## 1. Primary Architecture Overview

```
USER BROWSER
    │
    ▼
VERCEL (Edge / Serverless CDN)
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

## 2. Environment Variables Specification

### Frontend (`frontend/.env.local` / Vercel Environment Variables)
| Variable | Description | Example (Production) | Default (Local) |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Public-facing URL of the deployed FastAPI backend | `https://satquery-ai-backend.onrender.com` | `http://127.0.0.1:8000` |
| `BACKEND_API_URL` | Server-side App Router proxy target URL | `https://satquery-ai-backend.onrender.com` | `http://127.0.0.1:8000` |

### Backend (`backend/.env` / Host Environment Variables)
| Variable | Description | Example (Production) | Default (Local) |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | Service Identifier | `SATQUERY AI` | `SATQUERY AI` |
| `FRONTEND_URL` | Allowed origin for CORS | `https://satquery-ai.vercel.app` | `http://localhost:3000` |
| `DEMO_MODE` | Active PyTorch VLM inference mode | `true` | `true` |
| `MODEL_DEVICE` | Hardware device allocation | `cpu` or `cuda` | `auto` |
| `MAX_UPLOAD_SIZE_MB` | Maximum allowed payload upload size | `50` | `50` |

---

## 3. Frontend Deployment to Vercel

### Step-by-Step Vercel Setup
1. **Import Git Repository:** In your Vercel Dashboard, import `https://github.com/Sanjai-E242/satquery-ai.git`.
2. **Project Settings:**
   - **Framework Preset:** `Next.js`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
   - **Install Command:** `npm install`
3. **Environment Variables:**
   - Add `NEXT_PUBLIC_API_URL` = `https://<YOUR_BACKEND_URL>`
   - Add `BACKEND_API_URL` = `https://<YOUR_BACKEND_URL>`
4. **Deploy:** Click **Deploy**. Vercel will automatically build and publish the frontend.

---

## 4. Backend Deployment (Render / Docker / Railway)

### Deploying with Docker
```bash
# Build the production container
docker build -t satquery-ai-backend .

# Run container exposing port 8000
docker run -p 8000:8000 -e FRONTEND_URL="https://satquery-ai.vercel.app" satquery-ai-backend
```

### Deploying on Render (using `render.yaml`)
1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect `https://github.com/Sanjai-E242/satquery-ai.git`.
3. Render automatically reads `render.yaml`:
   - **Environment:** `Python 3.9+`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set `FRONTEND_URL` to your Vercel frontend URL.

---

## 5. Local Development Quickstart

```bash
# 1. Start Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 2. Start Frontend
cd frontend
npm install
npm run dev # (or npm run build && npm run start)
```

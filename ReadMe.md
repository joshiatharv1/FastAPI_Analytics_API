# 📊 FastAPI Web Traffic Analytics Microservice

A production-ready analytics API built with Python and FastAPI to process, store, and analyze web traffic data using a time-series database architecture. The system enables efficient ingestion of event data and supports analytical queries for tracking application usage patterns.

---

## 🚀 Overview

Modern web applications generate large volumes of event data such as page views, clicks, and user activity. This project demonstrates how to build a scalable analytics backend capable of ingesting, storing, and analyzing such data.

The API exposes endpoints to:

- Ingest web traffic events
- Store time-series metrics
- Perform time-based aggregations
- Query analytics insights for dashboards

The platform is containerized and deployable as a production-ready microservice.

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL, TimescaleDB |
| **ORM** | SQLModel |
| **Infrastructure** | Docker, Railway |
| **Language** | Python |

---

## 🏗 Architecture

```
Client / Web App
        │
        ▼
FastAPI Analytics API
        │
        ▼
Data Validation (Pydantic Models)
        │
        ▼
SQLModel ORM Layer
        │
        ▼
TimescaleDB (PostgreSQL)
        │
        ▼
Time-Series Aggregation Queries
```

**Key features:**

- Event ingestion API
- Time-series hypertables
- Aggregation queries for analytics
- Containerized deployment

---

## 📦 Features

### Event Tracking
Store application traffic events such as:
- Page views
- User interactions
- Session activity
- Timestamped analytics metrics

### Time-Series Data Processing
Uses TimescaleDB hypertables for optimized analytics queries.

### Data Aggregation
Supports queries such as:
- Traffic per hour/day
- Top pages
- Session activity trends

### Scalable API Design
- Async endpoints
- Typed schemas
- Optimized database queries

---

## 📂 Project Structure

```
analytics-api
│
├── app
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── api
│       └── routes.py
│
├── docker
│   └── Dockerfile
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/analytics-api
cd analytics-api
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🐳 Run with Docker

Build and run the service:

```bash
docker-compose up --build
```

This will start:
- FastAPI service
- PostgreSQL + TimescaleDB

---

## ▶️ Run Locally

Start the API server:

```bash
uvicorn app.main:app --reload
```

API will run at: `http://localhost:8000`

Interactive documentation: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Ingest Event

```
POST /events
```

**Example request:**

```json
{
  "user_id": "123",
  "page": "/home",
  "event_type": "page_view",
  "timestamp": "2026-01-10T12:30:00"
}
```

### Query Traffic Analytics

```
GET /analytics/traffic
```

Returns aggregated metrics such as:
- Page visits
- Time buckets
- Event counts

---

## 📈 Example Use Cases

- Web traffic analytics
- Application usage monitoring
- Product feature tracking
- Data pipeline experimentation
- Backend analytics services

---

## 🚀 Deployment

The service can be deployed using:
- Docker containers
- Railway cloud platform
- AWS container services

**Steps:**
1. Build container
2. Configure environment variables
3. Deploy container image

---

## 🔮 Future Improvements

- [ ] Real-time streaming analytics
- [ ] Dashboard visualization integration
- [ ] Authentication & API keys
- [ ] Kafka event ingestion pipeline
- [ ] Rate limiting & caching

---

## 👨‍💻 Author

**Atharv Joshi** — Backend & Distributed Systems Engineer

*Technologies: Python, FastAPI, Distributed Systems, Data Pipelines, AWS*
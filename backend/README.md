# FinTrack — Financial Analytics Platform

Production-grade financial analytics application that parses bank/credit card statements, categorizes transactions using LLM, and presents spending insights via an interactive dashboard.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CloudFront CDN                          │
│                    (React SPA from S3)                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (HTTP)                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Lambda Proxy
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS Lambda (FastAPI)                          │
│                                                                 │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐    │
│  │ API Layer│  │ Service Layer│  │ Infrastructure Layer   │    │
│  │ (Routes) │──│ (Business    │──│ (DynamoDB, S3, LLM)    │    │
│  │          │  │  Logic)      │  │                        │    │
│  └──────────┘  └──────────────┘  └────────────────────────┘    │
│                       │                                         │
│              ┌────────┴────────┐                                │
│              │  Domain Layer   │                                │
│              │ (Models, Enums) │                                │
│              └─────────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
         │              │                    │
         ▼              ▼                    ▼
    ┌─────────┐   ┌──────────┐   ┌───────────────────┐
    │DynamoDB │   │  S3      │   │ LLM Provider      │
    │(Users,  │   │(Uploads) │   │ (OpenAI / Grok)   │
    │ Txns,   │   │          │   │                   │
    │ Files)  │   │          │   │                   │
    └─────────┘   └──────────┘   └───────────────────┘
```

## File Processing Pipeline

```
Upload → S3 Storage → Type Detection → Parse (CSV/PDF)
    → Extract Transactions → Normalize → LLM Categorization → DynamoDB
```

---

## Folder Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point
│   │   ├── config.py                   # Environment config (Pydantic Settings)
│   │   ├── api/
│   │   │   ├── deps.py                 # DI: auth, DB, services
│   │   │   └── routes/
│   │   │       ├── auth.py             # POST /signup, /login
│   │   │       ├── files.py            # POST /upload, /process, GET /status
│   │   │       ├── transactions.py     # GET /transactions
│   │   │       └── dashboard.py        # GET /dashboard
│   │   ├── domain/
│   │   │   ├── models.py              # Pydantic models
│   │   │   ├── enums.py               # Category, FileType enums
│   │   │   └── exceptions.py          # Domain exceptions
│   │   ├── services/
│   │   │   ├── auth_service.py        # JWT + bcrypt auth
│   │   │   ├── file_upload_service.py # S3 upload + validation
│   │   │   ├── parser_service.py      # CSV + PDF parsing
│   │   │   ├── categorization_service.py # LLM + rule-based fallback
│   │   │   ├── transaction_service.py # Full pipeline orchestration
│   │   │   └── dashboard_service.py   # Aggregation logic
│   │   └── infrastructure/
│   │       ├── database.py            # DynamoDB client
│   │       ├── storage.py             # S3 client
│   │       ├── llm/
│   │       │   ├── base.py            # Abstract LLMProvider
│   │       │   ├── openai_provider.py
│   │       │   ├── grok_provider.py
│   │       │   └── factory.py         # Provider factory
│   │       └── repositories/
│   │           ├── user_repository.py
│   │           ├── transaction_repository.py
│   │           └── file_repository.py
│   ├── tests/
│   ├── lambda_handler.py              # Mangum adapter
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                       # Axios client + endpoints
│   │   ├── store/                     # Zustand auth store
│   │   ├── hooks/                     # React Query hooks
│   │   ├── pages/                     # Login, Signup, Dashboard, Upload
│   │   └── components/                # Charts, tables, file uploader
│   ├── package.json
│   └── vite.config.ts
├── infra/
│   ├── main.tf                        # Module composition
│   ├── modules/
│   │   ├── s3/                        # Frontend + uploads buckets
│   │   ├── cloudfront/                # CDN distribution
│   │   ├── dynamodb/                  # Users, Transactions, Files tables
│   │   ├── lambda/                    # API function
│   │   ├── api_gateway/               # HTTP API
│   │   └── iam/                       # Lambda role + GitHub OIDC
│   └── terraform.tfvars.example
└── .github/workflows/
    ├── deploy-frontend.yml            # Build → S3 → CloudFront invalidation
    └── deploy-backend.yml             # Test → Package → Lambda deploy
```

---

## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit with your config
uvicorn app.main:app --reload --port 8080
```

### Frontend

```bash
cd frontend
npm install
npm run dev                # Starts on http://localhost:5173
```

### Run Tests

```bash
cd backend
pip install -r requirements-test.txt
python -m pytest tests/ -v
```

---

## API Endpoints

| Method | Path                           | Auth | Description                    |
|--------|--------------------------------|------|--------------------------------|
| POST   | `/api/v1/auth/signup`          | No   | Create account                 |
| POST   | `/api/v1/auth/login`           | No   | Login, returns JWT             |
| POST   | `/api/v1/files/upload`         | Yes  | Upload PDF/CSV                 |
| POST   | `/api/v1/files/{id}/process`   | Yes  | Parse + categorize file        |
| GET    | `/api/v1/files/{id}/status`    | Yes  | Check processing status        |
| GET    | `/api/v1/transactions`         | Yes  | List all transactions          |
| GET    | `/api/v1/dashboard`            | Yes  | Aggregated spending data       |
| GET    | `/health`                      | No   | Health check                   |

### Example Requests

**Signup:**
```bash
curl -X POST http://localhost:8080/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
# Returns: {"access_token": "eyJ...", "token_type": "bearer"}
```

**Upload file:**
```bash
curl -X POST http://localhost:8080/api/v1/files/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@statement.csv"
# Returns: {"file_id": "uuid", "filename": "statement.csv", "status": "pending"}
```

**Process file:**
```bash
curl -X POST http://localhost:8080/api/v1/files/<file_id>/process \
  -H "Authorization: Bearer <token>"
# Returns: {"file_id": "...", "status": "completed", "transaction_count": 42}
```

**Dashboard:**
```bash
curl http://localhost:8080/api/v1/dashboard \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "total_spending": 3245.67,
  "transaction_count": 42,
  "monthly_spending": [
    {
      "month": "2025-01",
      "total": 1523.45,
      "categories": [
        {"category": "Food", "total": 342.50, "count": 12, "percentage": 22.5}
      ]
    }
  ],
  "category_breakdown": [
    {"category": "Food", "total": 845.30, "count": 28, "percentage": 26.0},
    {"category": "Bills", "total": 650.00, "count": 4, "percentage": 20.0}
  ]
}
```

---

## LLM Categorization Prompt

The system uses this structured prompt for transaction categorization:

```
You are a financial transaction categorizer.
Classify the following transaction into EXACTLY ONE of these categories:
["Food", "Travel", "Groceries", "Bills", "Shopping", "Entertainment",
 "Healthcare", "Education", "Transportation", "Other"]

Transaction description: STARBUCKS STORE #1234
Amount: $5.50

Respond ONLY with valid JSON in this exact format:
{"category": "<category>", "confidence": <0.0-1.0>}
Do not include any other text or explanation.
```

The provider is pluggable — switch between **OpenAI** and **Grok** via the `LLM_PROVIDER` env var. When no LLM key is configured, the system falls back to a keyword-based rule engine.

---

## Infrastructure Deployment

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars  # Edit values
terraform init
terraform plan
terraform apply
```

### GitHub Secrets Required

| Secret                       | Description                              |
|------------------------------|------------------------------------------|
| `AWS_DEPLOY_ROLE_ARN`        | IAM role ARN for GitHub OIDC             |
| `FRONTEND_S3_BUCKET`         | S3 bucket name for frontend              |
| `CLOUDFRONT_DISTRIBUTION_ID` | CloudFront distribution ID               |
| `API_URL`                    | API Gateway URL                          |
| `LAMBDA_FUNCTION_NAME`       | Lambda function name                     |

---

## DynamoDB Table Design

**Users** — `PK: user_id` | GSI: `email-index`
| Field         | Type   |
|---------------|--------|
| user_id       | String |
| email         | String |
| password_hash | String |
| created_at    | String |

**Transactions** — `PK: transaction_id` | GSI: `user-id-index`
| Field          | Type    |
|----------------|---------|
| transaction_id | String  |
| user_id        | String  |
| date           | String  |
| description    | String  |
| amount         | Number  |
| category       | String  |
| file_id        | String  |

**Files** — `PK: file_id` | GSI: `user-id-index`
| Field             | Type   |
|-------------------|--------|
| file_id           | String |
| user_id           | String |
| filename          | String |
| file_type         | String |
| s3_path           | String |
| status            | String |
| upload_date       | String |
| transaction_count | Number |
| error_message     | String |

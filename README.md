# Flask Supabase Backend Template

A production-ready Flask backend template with Supabase integration, Redis caching, Celery for async tasks, and comprehensive monitoring.

## Features

- **Backend Framework**: Flask with Blueprints architecture
- **API**: Flask-Smorest (OpenAPI/Swagger) with Marshmallow validation
- **Database**: Supabase Postgres (primary) + SQLAlchemy for direct queries
- **Authentication**: Supabase Auth (email/password, OAuth) with JWT verification
- **Caching & Queue**: Redis for caching/rate limiting + Celery for async tasks
- **Blog System**: Markdown-backed content with Supabase Storage
- **Monitoring**: Sentry error tracking + OpenTelemetry tracing
- **Infrastructure**: Docker, nginx, gunicorn
- **Admin**: Optional Flask-Admin interface

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration classes
│   ├── extensions.py        # Flask extensions (DB, Redis, Celery, etc.)
│   ├── middleware.py        # JWT auth, request logging
│   ├── monitoring.py        # Sentry & OpenTelemetry setup
│   ├── blueprints/
│   │   ├── web/            # SSR routes (Jinja2)
│   │   ├── api/            # REST API endpoints
│   │   ├── blog/           # Blog routes
│   │   └── auth/           # Auth endpoints
│   ├── services/           # Business logic
│   ├── models/             # SQLAlchemy models
│   ├── tasks/              # Celery async tasks
│   ├── admin/              # Flask-Admin setup
│   └── templates/          # Jinja2 templates
├── migrations/             # Alembic database migrations
├── content/                # Blog content directory
├── nginx/                  # nginx configuration
├── scripts/                # Setup and utility scripts
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Supabase)
- Redis
- Docker & Docker Compose (optional)

### Setup

1. **Clone and setup**:
```bash
git clone <your-repo-url>
cd THL007-flask-supabase-backend-template-v2026
./scripts/setup.sh
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

3. **Set up Supabase**:
   - Create a Supabase project at [supabase.com](https://supabase.com)
   - Get your project URL, anon key, service role key, and JWT secret
   - Run the SQL script in `scripts/init_db.sql` in your Supabase SQL editor
   - Create a storage bucket named `blog-content` (or update `BLOG_STORAGE_BUCKET` in config)

4. **Run database migrations** (if using SQLAlchemy models):
```bash
source venv/bin/activate
alembic upgrade head
```

5. **Start the application**:
```bash
# Development
python run.py

# Or with Docker Compose
docker-compose up
```

6. **Start Celery worker** (in a separate terminal):
```bash
# Development
celery -A celery_worker.celery worker --loglevel=info

# Or with Docker Compose (already included)
docker-compose up celery
```

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for full list):

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Supabase anon key
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key (for admin operations)
- `SUPABASE_JWT_SECRET`: JWT secret for token verification
- `DATABASE_URL`: Direct Postgres connection string (for SQLAlchemy)
- `REDIS_URL`: Redis connection URL
- `CELERY_BROKER_URL`: Celery broker URL (usually Redis)
- `SENTRY_DSN`: Sentry DSN for error tracking (optional)
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OpenTelemetry endpoint (optional)

### Supabase Setup

1. **Create tables**: Run `scripts/init_db.sql` in Supabase SQL editor
2. **Storage bucket**: Create a bucket named `blog-content` (or update config)
3. **Row Level Security**: RLS policies are included in the SQL script
4. **Authentication**: Configure auth providers in Supabase dashboard

## API Documentation

Once running, access:
- **Swagger UI**: `http://localhost:5000/api/swagger-ui`
- **OpenAPI Spec**: `http://localhost:5000/api/openapi.json`

## Authentication

### Using Supabase Auth

The backend verifies Supabase JWT tokens. To use protected endpoints:

```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token in protected endpoints
curl http://localhost:5000/api/v1/protected \
  -H "Authorization: Bearer <access_token>"
```

### JWT Verification

The `@require_auth` decorator verifies Supabase JWTs:

```python
from app.middleware import require_auth

@api_bp.route("/protected")
@require_auth
def protected_endpoint():
    from flask import g
    return {"user_id": g.current_user_id}
```

## Blog System

The blog system supports Markdown content stored in:
- **Supabase tables**: For metadata and inline content
- **Supabase Storage**: For large markdown files

### Creating Blog Posts

1. Insert into `blog_posts` table via Supabase dashboard or API
2. Upload markdown files to `blog-content` storage bucket
3. Set `content_storage_path` to the file path

### Blog API

- `GET /blog` - List all posts (SSR)
- `GET /blog/<slug>` - View post (SSR)
- `GET /blog/api/posts` - List posts (JSON API)
- `GET /blog/api/posts/<slug>` - Get post (JSON API)

## Celery Tasks

Example async task:

```python
from app.tasks.example_tasks import example_task

# Call task asynchronously
result = example_task.delay({"key": "value"})

# Get result
print(result.get())
```

### Running Celery

```bash
# Worker
celery -A celery_worker.celery worker --loglevel=info

# Beat (scheduled tasks)
celery -A celery_worker.celery beat --loglevel=info

# Flower (monitoring)
celery -A celery_worker.celery flower
```

## Docker Deployment

### Development

```bash
docker-compose up
```

Services:
- `web`: Flask application (port 5000)
- `celery`: Celery worker
- `celery-beat`: Scheduled tasks
- `flower`: Celery monitoring (port 5555)
- `db`: PostgreSQL
- `redis`: Redis
- `nginx`: Reverse proxy (port 80)

### Production

1. **Build image**:
```bash
docker build -t flask-supabase-backend .
```

2. **Run with environment variables**:
```bash
docker run -d \
  -p 5000:5000 \
  --env-file .env \
  flask-supabase-backend
```

3. **Or use docker-compose** (update for production):
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Deployment

### Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Create app: `fly launch`
4. Set secrets: `fly secrets set SUPABASE_URL=...`
5. Deploy: `fly deploy`

### Render

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy automatically on push

### Hetzner

1. Create a VM
2. Install Docker
3. Clone repository
4. Configure `.env`
5. Run `docker-compose up -d`

## Monitoring

### Sentry

Set `SENTRY_DSN` in environment variables. Errors are automatically tracked.

### OpenTelemetry

Set `OTEL_EXPORTER_OTLP_ENDPOINT` to send traces to your observability platform.

### Logging

Structured JSON logging is enabled in production. Logs include:
- Request ID for tracing
- Request/response details
- Error stack traces

## Rate Limiting

Rate limiting is configured via Flask-Limiter with Redis backend:

- API endpoints: 10 requests/second
- General endpoints: 30 requests/second
- Configurable in `app/config.py`

## Frontend Integration

### Web (SSR)

Flask serves Jinja2 templates with progressive enhancement. Templates are in `app/templates/`.

### SPA (React/Vite)

Consume the Flask API:

```javascript
// Example API call
fetch('http://localhost:5000/api/v1/health')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Mobile (React Native/Expo)

Use `@supabase/supabase-js` for auth/data and call Flask API for complex flows:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Auth with Supabase
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password'
});

// Call Flask API with token
fetch('http://your-api.com/api/v1/protected', {
  headers: {
    'Authorization': `Bearer ${data.session.access_token}`
  }
});
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
flake8 .
mypy .
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### Supabase Connection Issues

- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check Supabase project is active
- Ensure RLS policies allow your operations

### Redis Connection Issues

- Verify Redis is running: `redis-cli ping`
- Check `REDIS_URL` format: `redis://localhost:6379/0`

### Celery Not Processing Tasks

- Ensure Celery worker is running
- Check Redis connection
- Verify task is registered: `celery -A celery_worker.celery inspect registered`

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.

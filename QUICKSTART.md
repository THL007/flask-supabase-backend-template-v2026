# Quick Start Guide

## 1. Initial Setup

```bash
# Run setup script
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate
```

## 2. Configure Environment

```bash
# Copy and edit .env file
cp .env.example .env
# Edit .env with your Supabase credentials
```

Required Supabase credentials:
- `SUPABASE_URL`: Your project URL
- `SUPABASE_KEY`: Anon/public key
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key (for admin)
- `SUPABASE_JWT_SECRET`: JWT secret (from Supabase dashboard)

## 3. Set Up Supabase Database

1. Go to your Supabase project SQL editor
2. Run `scripts/init_db.sql` to create the blog_posts table
3. Create a storage bucket named `blog-content` (or update config)

## 4. Start Services

### Option A: Docker Compose (Recommended)

```bash
docker-compose up
```

This starts:
- Flask app on port 5000
- Celery worker
- Redis
- PostgreSQL
- nginx on port 80

### Option B: Local Development

Terminal 1 - Flask:
```bash
python run.py
```

Terminal 2 - Celery:
```bash
celery -A celery_worker.celery worker --loglevel=info
```

Terminal 3 - Redis (if not running):
```bash
redis-server
```

## 5. Verify Installation

- Web: http://localhost:5000
- API Health: http://localhost:5000/api/v1/health
- Swagger UI: http://localhost:5000/api/swagger-ui
- Flower (Celery): http://localhost:5555 (if running)

## 6. Test Authentication

```bash
# Sign up
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use token
curl http://localhost:5000/api/v1/protected \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 7. Create a Blog Post

Via Supabase Dashboard:
1. Go to Table Editor → blog_posts
2. Insert a new row with:
   - title: "My First Post"
   - slug: "my-first-post"
   - author: "John Doe"
   - published: true
   - excerpt: "This is my first blog post"

Or via SQL:
```sql
INSERT INTO blog_posts (title, slug, author, published, excerpt, content)
VALUES (
  'My First Post',
  'my-first-post',
  'John Doe',
  true,
  'This is my first blog post',
  '# My First Post\n\nThis is the content...'
);
```

## 8. View Blog

- List: http://localhost:5000/blog
- Post: http://localhost:5000/blog/my-first-post
- API: http://localhost:5000/blog/api/posts

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize blueprints in `app/blueprints/`
- Add your own Celery tasks in `app/tasks/`
- Configure monitoring (Sentry, OpenTelemetry)
- Deploy to production (Fly.io, Render, Hetzner)


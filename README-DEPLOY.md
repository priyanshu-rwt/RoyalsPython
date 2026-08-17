# Royals Webtech Backend

Production-ready Flask backend for:
- Contact enquiry API
- Career application API
- Supabase PostgreSQL database
- Supabase Storage for resumes
- Gmail SMTP notifications
- Render deployment

## 1. Supabase database

Open the same Supabase project used by the Java backend.

Run `supabase/schema.sql` once in Supabase SQL Editor.

Then create a **private** Storage bucket named `resumes`.

## 2. Environment variables

Use the values from the same Supabase project:

DATABASE_URL=the Supabase **Session Pooler** PostgreSQL connection string (port 5432)
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=the server-side service role key
SUPABASE_BUCKET=resumes

Email:
MAIL_USERNAME=your Gmail address
MAIL_PASSWORD=your Gmail App Password
HR_EMAIL=the HR recipient address

Frontend:
ALLOWED_ORIGINS=https://your-frontend-domain.com

For local development, copy `.env.example` to `.env`.

## 3. Important Supabase connection choice

For Render, use the Supabase **Session Pooler** connection string from
Supabase Dashboard -> Connect. Use the pooler host with port `5432`.
Do not use the direct `db.<project>.supabase.co:5432` URL on a normal
Supabase project without IPv4 support, because Render's network is IPv4-oriented.

## 4. Local run

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Health:
GET /health

Database:
GET /api/test-db

## 5. Render

Create a new Web Service from this repository.

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

Add every variable from `.env` to Render Environment Variables.

Do not upload `.env` or the Supabase service-role key to GitHub.

## API endpoints

POST /api/contact
POST /api/career/apply
GET /api/test-db
GET /health

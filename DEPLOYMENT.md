# Mobile Mart deployment

## Render
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Add environment variable `SECRET_KEY` with a long random value.
- Do not upload `.env` or API keys.

The included SQLite database contains the current demo data. SQLite on a free cloud web service is suitable for a demo, but its filesystem is not persistent across some redeploys/restarts. For production, move the database to a managed PostgreSQL database.

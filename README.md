# Ruhiyat — psychology learning platform

Django 5.2 + templates + PostgreSQL, Jazzmin admin, 4 languages (O‘zbek, Qaraqalpaq, Русский, English),
optional AI feedback through OpenRouter. Ready for Render's free plan.

## What it does

- **Roles**: administrators, psychologists, clients. Registration asks for the role.
  Psychologists start unverified; an admin verifies them in the admin panel
  (Users → select → *Verify selected psychologists*), which gives them access to the studio.
- **Topics** created by psychologists in the studio (`/admin/`), each made of steps:
  lesson, test (scored, with low/medium/high interpretations), reflection question,
  breathing game, flip-card game. Psychologists only see their own topics and their clients' results.
- **Choose a psychologist (any age)**: a directory filtered by age group (children, teens, adults,
  seniors) and consultation language. A client sends a request; once the psychologist accepts,
  they talk in a private chat, the psychologist can recommend topics right in the chat and sees the
  client's progress, test results and mood history.
- **Tests & games hub** (`/practice/`): every test and game in one place — tests to learn about
  yourself, and interactive games (breathing, flip cards, and a "what would you do?" situation game
  with feedback on each choice) to practise solutions to real problems.
- **Daily mood check-in** on the client dashboard with a 14-day mood chart.
- **Clients** pick a topic, go step by step (any step can be opened directly), get test results,
  write reflections (optionally with supportive AI feedback, limited by `AI_DAILY_LIMIT` per user per day).
- **Stopped halfway?** After `ABANDON_AFTER_DAYS` (default 3) without activity the dashboard shows
  the topic with related-topic suggestions. Users can pause any topic and set a reminder:
  it appears in the dashboard calendar and bell badge, and can be added to Google Calendar
  or the phone calendar (.ics with an alarm).
- **Languages**: switcher in the header. Interface strings live in `tools/translations.py`
  and `tools/translations_care.py`;
  content is translated per field in the admin (`title [uz]`, `title [kaa]`, …).

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
copy .env.example .env            # set DJANGO_SUPERUSER_PASSWORD
python manage.py compile_translations
python manage.py migrate
python manage.py setup_roles      # Psychologists group + admin from .env
python manage.py seed_demo        # optional demo content
python manage.py runserver
```

Tests: `python manage.py test learning`

Translations: edit `tools/translations.py`, then
`python tools/build_po.py && python manage.py compile_translations`.

## Deploy to Render (free)

1. Push this folder to a GitHub repository.
2. Render dashboard → **New → Blueprint** → choose the repository. `render.yaml` creates a free
   web service and a free PostgreSQL database.
3. When asked, fill in `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`
   (and optionally `OPENROUTER_API_KEY` for AI feedback). Then click **Apply**.
4. The first build installs everything, migrates, creates the admin and demo content.
   Open `https://<service>.onrender.com/admin/` and log in.

Free-plan limits to know: the site sleeps after 15 minutes without visitors (first request then
takes about a minute), the free database expires 30 days after creation, and there is no
persistent disk, so the app stores no uploaded files (topics use emoji and colour themes instead).

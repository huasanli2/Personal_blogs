# AGENTS.md

Two-person private blog/chat (Chinese: "我们的小窝" / OurNest). Django 4.2 + Channels (Daphne) + HTMX + Tailwind CDN. Single project, no monorepo.

## Doc vs. reality (trust the code)

`docs/requirements.md` is the original spec and is **partially stale**. When in conflict, the code wins:

- Stack is **Django 4.2.x** (`requirements.txt` pins `>=4.2,<5.0`), **not** Django 5.x.
- **No Django REST Framework** is installed or used. Views return `HttpResponse` / `JsonResponse` / rendered templates directly.
- Apps live **at the repo root** (`accounts/`, `chat/`, `daily/`, `moments/`, `plans/`, `storage/`), **not** under an `apps/` package. There is no `apps/` directory.
- **No `forms.py` anywhere.** Views read `request.POST` / `request.FILES` directly. Match this pattern when adding features; do not introduce `forms.py` unless asked.
- Only **HTMX** is loaded in `templates/base.html` (HTMX + `ws.js` extension). **Alpine.js is not used** despite the spec mentioning it.

## Layout

- `config/` — Django project (`settings.py`, `urls.py`, `asgi.py`, `wsgi.py`). Single settings module, no dev/prod split.
- `accounts/` — Custom user (`accounts.User` extending `AbstractUser` with `nickname`/`avatar`/`bio`). `AUTH_USER_MODEL = 'accounts.User'` — always use `settings.AUTH_USER_MODEL` or `get_user_model()`, never import `User` from `django.contrib.auth.models`.
- `moments/` — Posts + images + comments + likes (the "朋友圈" feed). Has `templatetags/post_filters.py` exposing the `|has_liked:user` filter.
- `daily/` — `FoodLog`, `FoodLike`, `DailyLog`, `Whisper`.
- `plans/` — `Place`, `Movie` (travel + watch lists).
- `chat/` — WebSocket chat via Channels. Models: `Message` (with `is_recalled`). `routing.py` registers `ws/chat/`.
- `storage/` — Read-only search/filter view over `moments.Post`. `storage/models.py` is intentionally empty; the app owns no models.
- `templates/` — Project-level templates (`DIRS = [BASE_DIR / 'templates']`). HTMX partials live under `templates/<app>/partials/`.
- `static/` is empty in-repo; `staticfiles/` is the `collectstatic` output (gitignored, but auto-populated by `build.sh`).
- `media/` — User uploads, gitignored. Production must mount a writable volume at this path.

## Commands

```bash
# Local dev (HTTP only; WebSocket works via Channels' InMemoryChannelLayer when REDIS_URL is unset):
python manage.py runserver

# Full ASGI (matches production):
daphne config.asgi:application

# Migrations
python manage.py makemigrations <app>
python manage.py migrate

# Tests (Django test runner; there is no pytest config)
python manage.py test                                                                       # all apps
python manage.py test chat                                                                  # single app
python manage.py test chat.tests.ChatConsumerTest                                            # single class
python manage.py test chat.tests.MessageRecallTest.test_message_is_recalled_field_default   # single test

# Collect static (Whitenoise serves them in prod)
python manage.py collectstatic --noinput
```

There is **no lint, formatter, typecheck, or pre-commit** configured. Don't invent commands; ask before adding tooling.

## Settings & environment

- Reads `.env` via `python-dotenv` (`load_dotenv()` at top of `config/settings.py`). Template lives at `.env.example`.
- `DATABASE_URL` -> Postgres via `dj-database-url`; **unset -> SQLite at `db.sqlite3`**.
- `REDIS_URL` -> `channels_redis`; **unset -> `InMemoryChannelLayer`** (fine for local single-process; useless across multiple workers).
- Production gate is `DEBUG=False`. In that branch `config/settings.py` reads `ALLOWED_HOSTS`, appends `RAILWAY_PUBLIC_DOMAIN` if set, and trusts `X-Forwarded-Proto`.
- `LANGUAGE_CODE='zh-hans'`, `TIME_ZONE='Asia/Shanghai'`, `USE_TZ=True`. User-facing strings are Chinese — keep new ones consistent.
- `AUTH_PASSWORD_VALIDATORS` only enforces `min_length=4` (matches `accounts/views.py:change_password`).
- `LOGIN_URL = '/login/'`. The dark theme is forced via `<html class="dark">` in `base.html`; there is no light-mode toggle.

## Deployment (Railway / Procfile / Nixpacks)

- `Procfile`, `railway.toml`, and `nixpacks.toml` all funnel into **`bash build.sh`** as the start command.
- `build.sh` is the production entrypoint. It:
  1. Runs a diagnostic `ls -ld /app/media` + write test (production assumes media is mounted at `/app/media`).
  2. `python manage.py migrate --noinput`
  3. `python manage.py collectstatic --noinput`
  4. **Creates/updates two hardcoded users via `manage.py shell`**: `user1` (nickname `宝宝`, staff + superuser) and `user2` (nickname `贝贝`, normal). Both passwords are reset to `123456` on every deploy. This is intentional for a two-person private app — don't "fix" it without asking.
  5. `exec daphne config.asgi:application --port $PORT --bind 0.0.0.0`
- `runtime.txt` pins **Python 3.11.6** for buildpack-based platforms.
- In production, media is served by Django itself (`django.views.static.serve` wired up in `config/urls.py`).

## Patterns & conventions

- **HTMX-first**: Views check `request.headers.get('HX-Request')` to return partial HTML vs a full page. Keep this pattern. Several delete views set `HX-Trigger` response headers (`postDeleted`, `foodDeleted`, etc.) for client-side hooks.
- **Delete authorization**: `obj.author != request.user and not request.user.is_staff` — staff can delete anything. Unauthorized delete returns 403 `JsonResponse({'error': 'permission denied'})`, **not** a 302 redirect. `moments` is slightly different: it uses `get_object_or_404(Post, pk=pk, author=request.user)` so non-owners get 404, not 403 — match the surrounding app's pattern.
- **Chat room**: There is exactly one chat room. `room_name` is hardcoded as `'chat_room'` in `chat/consumers.py`. `chat/views.py` also exposes HTTP endpoints (`send/`, `upload/`, `load/`) that call `broadcast_message()` via the channel layer. WebSocket is the primary transport; HTTP is the fallback.
- **Custom template filter**: `|has_liked:user` in `moments/templatetags/post_filters.py` — load via `{% load post_filters %}` in templates.
- **No separate API layer**: Everything is server-rendered HTML or HTMX partials. Don't build REST endpoints unless asked.
- **`db.sqlite3` is tracked in git** despite the `.gitignore` entry. Don't add data to it via deploys, but don't remove it unless asked.

## Testing

- `accounts/tests.py`, `moments/tests.py`, and `storage/tests.py` are **empty stubs** — `TestCase` imported but no tests.
- `chat/tests.py` has the most tests: `MessageRecallTest` (Django `TestCase`) + `ChatConsumerTest` (Channels `TransactionTestCase` with `async` methods using `WebsocketCommunicator`).
- `daily/tests.py` covers delete authorization for `FoodLog`, `DailyLog`, `Whisper`. Uses `django.test.Client` + `reverse()`.
- `plans/tests.py` similarly covers delete authorization for `Place` and `Movie`.
- Run tests with `python manage.py test`. Channels async tests rely on `daphne`/`channels` being in `INSTALLED_APPS` (they are).

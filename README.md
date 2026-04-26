# PortfolioProject

A Django-based personal portfolio web application with a cyberpunk/terminal aesthetic.

This project includes:
- Public portfolio pages (home, about, hobbies, projects(in future), contact)
- Email-based authentication with account activation
- Password reset and password change flows
- Contact form with rate limiting and terminal-style system messages
- Japanese and English localization support

Repository: https://github.com/MainCharacter55/Portfolio
URL: https://mc55.pythonanywhere.com/

## Tech Stack

- Backend: Python 3.13, Django 5.2.8
- Security: django-axes, CSRF, token-based account activation
- Database (dev): SQLite
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- i18n: Django locale framework (en, ja)
- Optional frontend linting: stylelint

## Project Structure

- PortfolioProject/ - Django project settings and root URLs
- accounts/ - user model, auth flows, forms, email activation, lockout
- portfolio_app/ - portfolio pages and contact page
- templates/ - app templates
- static/ - source static assets
- locale/ - translation files

## Prerequisites

- Python 3.13+
- pip
- (Optional) Node.js + npm for CSS linting

## Local Setup

1. Clone and enter the repo

```bash
git clone https://github.com/MainCharacter55/Portfolio.git
cd Portfolio
```

2. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv venv
venv\Scripts
activate.bat
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

4. Create .env in the project root

Example:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_app_password
```

Notes:
- Keep DEBUG=True only for local development.
- In production, set DEBUG=False and provide a real ALLOWED_HOSTS value.
- .env is ignored by git and should never be committed.

5. Apply migrations and run server

```bash
python manage.py migrate
python manage.py runserver
```

## Development Commands

Health and test checks:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

### Translations (i18n)

When translatable strings are changed:

```bash
python manage.py makemessages -l ja
python manage.py compilemessages
```

### Static Collection (deployment simulation)

```bash
python manage.py collectstatic --noinput
```

## Frontend Linting (Optional)

Install Node dependencies:

```bash
npm install
```

Run CSS lint:

```bash
npm run lint:css
```

Auto-fix CSS lint issues:

```bash
npm run lint:css:fix
```

## Security and Auth Notes

- Email is the primary login identifier.
- New accounts are created inactive and require activation via emailed token.
- Authentication is protected with django-axes against brute-force attempts.
- Contact form submission is rate-limited.
- User-facing error/success messages follow terminal-style wording.

## Deployment Notes (PythonAnywhere)

Environment values for production should include:

- DEBUG=False
- ALLOWED_HOSTS=your-pythonanywhere-domain
- SECRET_KEY set to a strong secret
- EMAIL_USER and EMAIL_PASS configured

Typical deployment flow:

1. Pull latest code
2. Install dependencies
3. Run migrations
4. Compile messages (if changed)
5. Collect static files
6. Reload web app

## Current Dependencies

From requirements.txt:

- asgiref==3.10.0
- Django==5.2.8
- django-axes==8.1.0
- python-dotenv==1.2.1
- sqlparse==0.5.3

## License

No license file is currently defined in this repository.
If you plan to open-source this project, add a LICENSE file.

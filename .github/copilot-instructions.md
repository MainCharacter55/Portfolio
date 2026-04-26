# Project Overview
A Django-based web portfolio with a "Cyberpunk/Hacker Terminal" aesthetic. It features a home page, user authentication (email-based), and a contact system with rate limiting. The goal is to create a central hub for all professional and personal social platforms.

# Tech Stack
- Backend: Python 3.13.3 / Django 5.2.8
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5 (with Media Queries)
- Security: django-axes (Brute force protection), CSRF, Token-based email activation
- Database: SQLite (Dev) / SQL (Prod)
- Deployment: WSGI compatible (e.g., PythonAnywhere)

# Coding Guidelines
## Documentation & Formatting
- **Focus:** Focus on writing scalable, maintainable, and readable code with necessary comments based on best practices.
- **File Location:** Always include a comment with the file path at the very top (e.g., `# accounts/views.py`).
- **Docstrings:** Use Google-style docstrings for every class and function/method to describe its purpose, arguments, and return values.
- **Top-level Docstrings:** Every file must have a module-level docstring describing the overall logic and features.
- **Comments:** Use concise comments in necessary places to explain "why" logic exists (e.g., rate limit logic).

## Aesthetic & UX (Terminal Theme)
- **Messaging:** All system messages must use a sci-fi/terminal aesthetic.
  - Correct: "SIGNAL_DISPATCHED: Transmission Successful."
  - Incorrect: "Your message has been sent."
- **Headers:** Use clear visual separators like `# --- Section Name ---` for large code blocks.

## Security Standards
- **User Enumeration:** Never distinguish between "user not found" and "wrong password" in error messages to prevent enumeration attacks.
- **Rate Limiting:** Always implement throttling (e.g., max 5 messages/hour) for public-facing forms.
- **Authentication:** Use Email as the primary login ID, with `is_active=False` until email verification is complete.

# Project Structure
- `.github/`: Configuration and Copilot instructions.
- `accounts/`: Custom user model, authentication logic, and forms.
- `portfolio_app/`: Core portfolio pages (home, about, contact).
- `templates/`: HTML templates organized by app folder.
- `static/` & `staticfiles/`: CSS, JS, and terminal-theme assets.

# Do Not Use
- Do not use standard Django messages; always wrap them in the "TERMINAL_SIGNAL" or "SYSTEM_ERROR" format.
- Do not use hardcoded secret keys or credentials; always use `.env` variables.
- Avoid using function-based views for registration/login; prefer Class-Based Views (CBVs) like `CreateView` or `TemplateView`.

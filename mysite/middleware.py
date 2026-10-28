"""Project-specific middleware.

Keep authentication, CSRF handling, and DEBUG configuration in Django settings.
Never mutate process-wide settings during an individual HTTP request.
"""

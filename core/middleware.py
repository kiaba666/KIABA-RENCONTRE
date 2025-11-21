from django.http import HttpRequest
from django.shortcuts import redirect


class AgeGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = request.path
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        
        # Detect search engine crawlers and allow them to bypass age gate
        is_search_engine = any(
            bot in user_agent
            for bot in [
                "googlebot",
                "bingbot",
                "slurp",  # Yahoo
                "duckduckbot",
                "baiduspider",
                "yandexbot",
                "sogou",
                "exabot",
                "facebot",
                "ia_archiver",  # Alexa
            ]
        )
        
        if not request.COOKIES.get("age_gate_accepted") and not is_search_engine:
            # Allow age-gate, admin, auth, static/media, SEO endpoints
            # Use direct path instead of reverse() to avoid errors during startup
            allowed = (
                path.startswith("/age-gate/")
                or path.startswith("/admin/")
                or path.startswith("/auth/")
                or path.startswith("/static/")
                or path.startswith("/media/")
                or path == "/robots.txt"
                or path == "/sitemap.xml"
                or path.startswith("/google")
            )
            if not allowed:
                # Use direct path to avoid reverse() errors
                return redirect("/age-gate/")
        return self.get_response(request)

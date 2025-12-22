from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.conf import settings


class RedirectMiddleware:
    """
    Middleware pour gérer les redirections :
    - HTTP vers HTTPS
    - www vers non-www (ou vice versa)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Vérifier HTTPS en tenant compte des proxies (Render, etc.)
        # Vérifier d'abord le header X-Forwarded-Proto (pour les proxies)
        forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO', '')
        is_https = request.is_secure() or forwarded_proto == 'https'
        
        # Redirection HTTP vers HTTPS (sauf en DEBUG pour le développement local)
        # Cette redirection ne se fait QUE si :
        # 1. La requête n'est PAS en HTTPS
        # 2. On n'est PAS en mode DEBUG (donc en production)
        if not is_https and not settings.DEBUG:
            url = request.build_absolute_uri().replace('http://', 'https://', 1)
            return HttpResponsePermanentRedirect(url)
        
        # Redirection www vers non-www (ou l'inverse selon votre préférence)
        host = request.get_host()
        if host.startswith('www.'):
            # Rediriger www.ci-kiaba.com vers ci-kiaba.com
            url = request.build_absolute_uri().replace('www.', '', 1)
            return HttpResponsePermanentRedirect(url)
        
        # Si on arrive ici, la requête est valide (HTTPS ou DEBUG)
        # On laisse passer normalement
        return self.get_response(request)


class AgeGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = request.path
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        
        # Detect search engine crawlers and allow them to bypass age gate
        # Amélioration : détecter aussi les variantes de Googlebot
        is_search_engine = any(
            bot in user_agent
            for bot in [
                "googlebot",
                "google-inspectiontool",  # Google Search Console
                "bingbot",
                "slurp",  # Yahoo
                "duckduckbot",
                "baiduspider",
                "yandexbot",
                "sogou",
                "exabot",
                "facebot",
                "ia_archiver",  # Alexa
                "ahrefsbot",
                "semrushbot",
                "mj12bot",
            ]
        )
        
        # Vérifier aussi l'IP de Google (optionnel mais plus sûr)
        # Les IPs de Google commencent souvent par 66.249.x.x
        client_ip = request.META.get('REMOTE_ADDR', '')
        if client_ip.startswith('66.249.') or client_ip.startswith('64.233.') or client_ip.startswith('72.14.'):
            is_search_engine = True
        
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

from django.http import HttpResponse
from django.shortcuts import render


def robots_txt(_: object) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /auth/",
        "Disallow: /accounts/password/",
        "Disallow: /accounts/email/",
        "Disallow: /dashboard/",
        "Allow: /ads/",
        "Allow: /static/",
        "Allow: /media/",
        "Allow: /",
        "",
        "# Sitemaps",
        "Sitemap: https://ci-kiaba.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def google_verification(_: object) -> HttpResponse:
    """Serve Google Search Console verification file"""
    return HttpResponse(
        "google-site-verification: googleb96ecc9cfd50e4a1.html",
        content_type="text/html; charset=utf-8",
    )

from ads.models import Ad, City
from django.conf import settings
from django.db import models


def site_metrics(request):
    """Expose site-wide lightweight metrics to templates."""
    # Default values - always return these to prevent template errors
    total_approved_ads = 0
    popular_cities = []
    
    try:
        # Try to query database - catch all exceptions
        total_approved_ads = Ad.objects.filter(status=Ad.Status.APPROVED).count()
        
        # Get top 6 cities by ad count for footer internal linking
        popular_cities = list(
            City.objects.filter(ad__status=Ad.Status.APPROVED)
            .annotate(ad_count=models.Count("ad"))
            .filter(ad_count__gt=0)
            .order_by("-ad_count")[:6]
        )
    except Exception:
        # Silently fail and use default values - prevents 500 errors
        # The page will still load with 0 ads count and empty cities list
        pass
    
    # Google Analytics Measurement ID
    ga_measurement_id = getattr(settings, "GA_MEASUREMENT_ID", None)
    
    return {
        "total_approved_ads": total_approved_ads,
        "GA_MEASUREMENT_ID": ga_measurement_id,
        "popular_cities_footer": popular_cities,
    }

"""
Commande pour appliquer le filigrane aux images existantes
"""
from django.core.management.base import BaseCommand
from ads.models import AdMedia
from django.db import transaction


class Command(BaseCommand):
    help = "Applique le filigrane du logo à toutes les images existantes qui n'en ont pas encore"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui sera fait sans modifier les images',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limite le nombre d\'images à traiter',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        
        # Récupérer toutes les images
        all_media = AdMedia.objects.all()
        if limit:
            all_media = all_media[:limit]
        
        total = all_media.count()
        self.stdout.write(f"Traitement de {total} image(s)...")
        
        processed = 0
        errors = 0
        
        for media in all_media:
            try:
                if not media.image:
                    continue
                
                # Réinitialiser le flag pour forcer l'application du filigrane
                media._watermark_applied = False
                
                if dry_run:
                    self.stdout.write(f"  [DRY-RUN] Traiterait: {media.image.name} (Ad #{media.ad_id})")
                else:
                    # Appliquer le filigrane
                    result = media._add_watermark()
                    if result:
                        # Sauvegarder l'image modifiée
                        media.save()
                        processed += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Filigrane appliqué: {media.image.name} (Ad #{media.ad_id})")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"  ⚠ Impossible d'appliquer le filigrane: {media.image.name}")
                        )
                        errors += 1
                        
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Erreur pour {media.image.name if media.image else 'image inconnue'}: {str(e)}")
                )
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f"\n[DRY-RUN] {total} image(s) seraient traitées"))
        else:
            self.stdout.write(self.style.SUCCESS(f"\n✓ {processed} image(s) traitées avec succès"))
            if errors > 0:
                self.stdout.write(self.style.WARNING(f"⚠ {errors} erreur(s) rencontrée(s)"))


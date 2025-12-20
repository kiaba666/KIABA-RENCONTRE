"""
Script de management Django pour créer des utilisateurs et annonces
Crée 100 utilisateurs avec 300 annonces au total
"""
import os
import random
from io import BytesIO
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import transaction
from ads.models import City, Ad, AdMedia
from accounts.models import Profile
import bleach

try:
    from PIL import Image
except ImportError:
    Image = None

User = get_user_model()

# Noms ivoiriens pour créer des utilisateurs variés
IVOIRIAN_NAMES = [
    "Akoua", "Aminata", "Fatou", "Kadiatou", "Mariam", "Aissatou", "Hawa", "Aicha",
    "Kouassi", "Koffi", "Yao", "Kouame", "Kouadio", "Kouakou", "Yapi", "N'Guessan",
    "Aya", "Bintou", "Djeneba", "Fanta", "Kadija", "Maimouna", "Oumou", "Ramatou",
    "Amadou", "Bakary", "Boubacar", "Ibrahima", "Mamadou", "Ousmane", "Sekou", "Tidiane",
    "Adama", "Awa", "Diaby", "Diallo", "Doumbia", "Keita", "Konate", "Sangare",
    "Traore", "Toure", "Cisse", "Coulibaly", "Diakite", "Kone", "Sidibe", "Sylla",
]

FIRST_NAMES = [
    "Marie", "Sophie", "Julie", "Sarah", "Emma", "Laura", "Camille", "Lea",
    "Thomas", "Pierre", "Jean", "Paul", "Marc", "Luc", "Antoine", "Nicolas",
    "Aminata", "Fatou", "Mariam", "Aissatou", "Hawa", "Aicha", "Kadiatou",
    "Amadou", "Bakary", "Ibrahima", "Mamadou", "Ousmane", "Sekou", "Tidiane",
]

# Données d'annonces réalistes basées sur le style de ci.jedolo.com
ANNOUNCE_DATA = [
    {
        "title": "Belle jeune femme disponible à Abidjan",
        "description": "Jeune femme élégante et discrète, disponible pour vous accompagner dans vos moments de détente. Service de qualité avec professionnalisme.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage relaxant et thérapeutique",
        "description": "Massage professionnel pour vous détendre après une longue journée. Techniques variées selon vos besoins. Cadre agréable et discret.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage Relaxant", "Massage sensuel ou érotique"],
    },
    {
        "title": "Accompagnement élégant et discret",
        "description": "Service d'accompagnement pour vos sorties et événements. Présence élégante et discrète garantie. Disponible selon vos besoins.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage Ivoirien traditionnel",
        "description": "Découvrez les bienfaits du massage traditionnel ivoirien. Techniques ancestrales pour votre bien-être. Expérience unique et authentique.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage Ivoirien"],
    },
    {
        "title": "Service premium et personnalisé",
        "description": "Service haut de gamme adapté à vos préférences. Discrétion absolue et professionnalisme. Contactez-moi pour plus d'informations.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage sportif et récupération",
        "description": "Massage spécialisé pour sportifs. Aide à la récupération musculaire et à la détente. Techniques professionnelles appliquées.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage sportif"],
    },
    {
        "title": "Rencontre agréable et chaleureuse",
        "description": "Recherche rencontre sincère et agréable. Échange convivial dans un cadre respectueux. Disponible pour discuter et partager.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Cherche Homme"],
    },
    {
        "title": "Massage chinois traditionnel",
        "description": "Massage chinois avec techniques ancestrales. Équilibre énergétique et bien-être garanti. Expérience relaxante et revitalisante.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage chinois"],
    },
    {
        "title": "Accueil chaleureux et professionnel",
        "description": "Service de qualité avec un accueil personnalisé. Environnement confortable et discret. Disponible selon vos disponibilités.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage intégral et complet",
        "description": "Massage complet du corps pour une détente totale. Techniques variées pour votre bien-être. Moment de relaxation garanti.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage Intégral"],
    },
    {
        "title": "Gentleman attentionné et discret",
        "description": "Accompagnement par un gentleman courtois et attentionné. Service personnalisé selon vos besoins. Discrétion assurée.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Boys"],
    },
    {
        "title": "Rencontre pour moments privilégiés",
        "description": "Recherche compagnie agréable pour partager des moments privilégiés. Échange respectueux et convivial. Disponible sur rendez-vous.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Cherche Femme"],
    },
    {
        "title": "Service de qualité exceptionnelle",
        "description": "Service haut de gamme avec attention aux détails. Professionnalisme et discrétion garantis. Expérience mémorable assurée.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage pour votre bien-être",
        "description": "Prenez soin de vous avec un massage adapté à vos besoins. Techniques professionnelles dans un cadre apaisant. Réservation recommandée.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage Relaxant"],
    },
    {
        "title": "Accompagnement pour vos événements",
        "description": "Service d'accompagnement pour vos soirées et événements. Présence élégante et adaptée à l'occasion. Contactez-moi pour discuter.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Massage sensuel et relaxant",
        "description": "Massage sensuel pour une détente complète. Techniques douces et apaisantes. Moment de bien-être personnalisé.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage sensuel ou érotique"],
    },
    {
        "title": "Service discret et professionnel",
        "description": "Service professionnel avec discrétion absolue. Respect de vos préférences et besoins. Disponibilité flexible.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
    {
        "title": "Rencontre sincère et respectueuse",
        "description": "Recherche rencontre basée sur le respect et la sincérité. Échange agréable et convivial. Disponible pour discuter.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Cherche Homme"],
    },
    {
        "title": "Massage thérapeutique personnalisé",
        "description": "Massage adapté à vos besoins spécifiques. Techniques thérapeutiques pour soulager tensions et stress. Consultation préalable.",
        "category": Ad.Category.MASSAGES_SERVICES,
        "subcategories": ["Massage Relaxant"],
    },
    {
        "title": "Accompagnement élégant et raffiné",
        "description": "Service d'accompagnement haut de gamme. Présence élégante pour vos occasions spéciales. Professionnalisme garanti.",
        "category": Ad.Category.RENCONTRES_ESCORTES,
        "subcategories": ["Escort Girls"],
    },
]


class Command(BaseCommand):
    help = "Crée 100 utilisateurs avec 300 annonces au total"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=100,
            help="Nombre d'utilisateurs à créer (défaut: 100)",
        )
        parser.add_argument(
            "--ads",
            type=int,
            default=300,
            help="Nombre total d'annonces à créer (défaut: 300)",
        )

    def handle(self, *args, **options):
        num_users = options["users"]
        total_ads = options["ads"]
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Début de l'import: {num_users} utilisateurs, {total_ads} annonces au total"
            )
        )

        # Récupérer ou créer les villes
        cities = self.get_or_create_cities()

        # Créer les utilisateurs et annonces
        self.create_users_and_ads(num_users, total_ads, cities)

        self.stdout.write(self.style.SUCCESS("Import terminé avec succès!"))

    def get_or_create_cities(self):
        """Récupère ou crée les villes principales de Côte d'Ivoire"""
        cities_data = [
            ("Abidjan", "Lagunes"),
            ("Bouaké", "Gbêkê"),
            ("Yamoussoukro", "Lacs"),
            ("San-Pédro", "Bas-Sassandra"),
            ("Korhogo", "Poro"),
            ("Man", "Tonkpi"),
            ("Divo", "Loh-Djiboua"),
            ("Gagnoa", "Gôh"),
            ("Abengourou", "Indénié-Djuablin"),
            ("Daloa", "Haut-Sassandra"),
        ]
        cities = []
        for name, region in cities_data:
            city, _ = City.objects.get_or_create(name=name, defaults={"region": region})
            cities.append(city)
        return cities

    def get_jedolo_images(self):
        """Récupère la liste des images téléchargées depuis jedolo"""
        from pathlib import Path
        from django.conf import settings
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        # Chercher d'abord dans static/jedolo_images (images dans le repo)
        static_images_dir = base_dir / "static" / "jedolo_images"
        # Puis dans media/jedolo_images (images téléchargées)
        media_images_dir = base_dir / "media" / "jedolo_images"
        
        image_files = []
        
        # Chercher dans static/
        if static_images_dir.exists():
            for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.gif"]:
                image_files.extend(static_images_dir.glob(ext))
                image_files.extend(static_images_dir.glob(ext.upper()))
        
        # Chercher dans media/ si static/ est vide
        if not image_files and media_images_dir.exists():
            for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.gif"]:
                image_files.extend(media_images_dir.glob(ext))
                image_files.extend(media_images_dir.glob(ext.upper()))
        
        return sorted(image_files)
    
    def create_fake_image(self):
        """Crée une image fictive si aucune image jedolo n'est disponible"""
        if Image is None:
            return None
        
        try:
            buf = BytesIO()
            # Créer une image avec une couleur aléatoire
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255),
            )
            image = Image.new("RGB", (600, 400), color=color)
            image.save(buf, format="JPEG", quality=70)
            return buf.getvalue()
        except Exception:
            return None

    def generate_username(self, index):
        """Génère un nom d'utilisateur unique"""
        first = random.choice(FIRST_NAMES)
        last = random.choice(IVOIRIAN_NAMES)
        username = f"{first.lower()}{last.lower()}{index}"
        return username

    @transaction.atomic
    def create_users_and_ads(self, num_users, total_ads, cities):
        """Crée les utilisateurs et leurs annonces"""
        from django.db.models.signals import post_save
        from accounts.signals import on_user_saved
        
        created_users = 0
        created_ads = 0
        
        # Désactiver temporairement le signal d'envoi d'email
        post_save.disconnect(on_user_saved, sender=User)
        
        try:
            # Calculer le nombre d'annonces par utilisateur
            ads_per_user = total_ads // num_users
            extra_ads = total_ads % num_users
            
            # Préparer le pool d'annonces
            ad_pool = ANNOUNCE_DATA * ((total_ads // len(ANNOUNCE_DATA)) + 1)
            random.shuffle(ad_pool)
            ad_index = 0
            
            for i in range(num_users):
                username = self.generate_username(i + 1)
                
                # Vérifier si l'utilisateur existe déjà
                if User.objects.filter(username=username).exists():
                    username = f"{username}_{i+1}_{random.randint(1000, 9999)}"
                
                # Créer l'utilisateur sans déclencher le signal d'email
                user = User.objects.create(
                    username=username,
                    email=f"{username}@example.com",
                    role=User.Role.PROVIDER,
                    is_active=True,
                    is_verified=random.choice([True, False]),
                )
                user.set_password("password123")
                user.save()
                
                # Créer le profil
                profile = Profile.objects.get(user=user)
                profile.display_name = f"{random.choice(FIRST_NAMES)} {random.choice(IVOIRIAN_NAMES)}"
                profile.city = random.choice(cities)
                profile.country = "CI"
                profile.contact_prefs = random.sample(["sms", "whatsapp", "call"], random.randint(1, 3))
                profile.bio_sanitized = "Profil créé automatiquement"
                profile.save()
                
                created_users += 1
                
                # Calculer le nombre d'annonces pour cet utilisateur
                num_user_ads = ads_per_user + (1 if i < extra_ads else 0)
                
                # Créer les annonces pour cet utilisateur
                for j in range(num_user_ads):
                    if ad_index >= len(ad_pool):
                        # Réutiliser le pool si nécessaire
                        ad_index = 0
                        random.shuffle(ad_pool)
                    
                    ad_data = ad_pool[ad_index].copy()
                    ad_index += 1
                    
                    # Varier légèrement le titre pour éviter les doublons
                    title = ad_data["title"]
                    if j > 0:
                        title = f"{title} {j+1}"
                    
                    # Sanitizer la description
                    description = bleach.clean(
                        ad_data["description"],
                        tags=[],
                        attributes={},
                        strip=True,
                    )
                    
                    # Créer l'annonce
                    ad = Ad.objects.create(
                        user=user,
                        title=title[:140],
                        description_sanitized=description[:2000],
                        category=ad_data["category"],
                        subcategories=ad_data["subcategories"][:3],
                        city=random.choice(cities),
                        area=random.choice(["Cocody", "Yopougon", "Marcory", "Plateau", "Abobo", ""]),
                        status=Ad.Status.APPROVED,
                        is_verified=random.choice([True, False]),
                        expires_at=timezone.now() + timezone.timedelta(days=random.randint(14, 30)),
                    )
                    
                    # Ajouter des images depuis le dossier jedolo_images
                    jedolo_images = self.get_jedolo_images()
                    images_added = 0
                    max_images_per_ad = min(5, len(jedolo_images) if jedolo_images else 1)
                    
                    if jedolo_images:
                        # Utiliser des images aléatoires du dossier
                        selected_images = random.sample(jedolo_images, min(max_images_per_ad, len(jedolo_images)))
                        
                        for img_idx, img_path in enumerate(selected_images):
                            try:
                                with open(img_path, "rb") as f:
                                    img_content = f.read()
                                
                                # Vérifier la taille (max 5MB)
                                if len(img_content) > 5 * 1024 * 1024:
                                    continue
                                
                                ext = img_path.suffix or ".jpg"
                                filename = f"ad_{ad.id}_{images_added+1}{ext}"
                                
                                AdMedia.objects.create(
                                    ad=ad,
                                    image=ContentFile(img_content, name=filename),
                                    is_primary=(images_added == 0),
                                )
                                images_added += 1
                                
                                if images_added >= 5:  # Maximum 5 images par annonce
                                    break
                                    
                            except Exception as e:
                                self.stdout.write(
                                    self.style.WARNING(f"Erreur lors de l'ajout de l'image {img_path}: {str(e)}")
                                )
                    
                    # Si aucune image jedolo n'a été ajoutée, créer une image fictive
                    if images_added == 0:
                        img_content = self.create_fake_image()
                        if img_content:
                            try:
                                AdMedia.objects.create(
                                    ad=ad,
                                    image=ContentFile(img_content, name=f"ad_{ad.id}_1.jpg"),
                                    is_primary=True,
                                )
                            except Exception:
                                pass
                    
                    created_ads += 1
                    
                    if created_ads % 50 == 0:
                        self.stdout.write(f"  → {created_ads} annonces créées...")
                
                if created_users % 25 == 0:
                    self.stdout.write(f"  → {created_users} utilisateurs créés...")
        
        finally:
            # Réactiver le signal d'envoi d'email
            post_save.connect(on_user_saved, sender=User)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nRésumé:\n"
                f"  - {created_users} utilisateurs créés\n"
                f"  - {created_ads} annonces créées\n"
            )
        )

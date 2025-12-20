"""
Script de management Django pour importer des annonces depuis ci.jedolo.com
Crée 546 utilisateurs avec au moins 2 annonces chacun
"""
import os
import re
import random
import requests
from io import BytesIO
from urllib.parse import urljoin, urlparse
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import transaction
from ads.models import City, Ad, AdMedia
from accounts.models import Profile
import bleach

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

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

# Prénoms supplémentaires
FIRST_NAMES = [
    "Marie", "Sophie", "Julie", "Sarah", "Emma", "Laura", "Camille", "Lea",
    "Thomas", "Pierre", "Jean", "Paul", "Marc", "Luc", "Antoine", "Nicolas",
    "Aminata", "Fatou", "Mariam", "Aissatou", "Hawa", "Aicha", "Kadiatou",
    "Amadou", "Bakary", "Ibrahima", "Mamadou", "Ousmane", "Sekou", "Tidiane",
]


class Command(BaseCommand):
    help = "Importe des annonces depuis ci.jedolo.com et crée 546 utilisateurs avec des annonces"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=546,
            help="Nombre d'utilisateurs à créer (défaut: 546)",
        )
        parser.add_argument(
            "--ads-per-user",
            type=int,
            default=2,
            help="Nombre minimum d'annonces par utilisateur (défaut: 2)",
        )
        parser.add_argument(
            "--max-ads",
            type=int,
            default=5,
            help="Nombre maximum d'annonces par utilisateur (défaut: 5)",
        )

    def handle(self, *args, **options):
        if BeautifulSoup is None:
            self.stdout.write(
                self.style.ERROR("BeautifulSoup4 n'est pas installé. Installez-le avec: pip install beautifulsoup4")
            )
            return

        num_users = options["users"]
        min_ads = options["ads_per_user"]
        max_ads = options["max_ads"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Début de l'import: {num_users} utilisateurs, {min_ads}-{max_ads} annonces par utilisateur"
            )
        )

        # Récupérer ou créer les villes
        cities = self.get_or_create_cities()

        # Scraper les annonces depuis ci.jedolo.com
        self.stdout.write("Scraping des annonces depuis ci.jedolo.com...")
        scraped_ads = self.scrape_jedolo_ads()

        if not scraped_ads:
            self.stdout.write(
                self.style.WARNING("Aucune annonce scrapée. Création d'annonces fictives...")
            )
            scraped_ads = self.generate_fake_ads(cities)

        # Créer les utilisateurs et annonces
        self.create_users_and_ads(num_users, min_ads, max_ads, scraped_ads, cities)

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

    def scrape_jedolo_ads(self, max_pages=10):
        """Scrape les annonces depuis ci.jedolo.com"""
        scraped_ads = []
        base_url = "https://ci.jedolo.com"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            # Essayer de scraper la page d'accueil et les pages de liste
            for page in range(1, max_pages + 1):
                if page == 1:
                    url = f"{base_url}/"
                else:
                    url = f"{base_url}/?page={page}"

                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    # Chercher les liens vers les annonces individuelles
                    ad_links = soup.find_all("a", href=re.compile(r"/annonce/|/ad/|/detail/"))
                    
                    for link in ad_links[:20]:  # Limiter à 20 annonces par page
                        ad_url = urljoin(base_url, link.get("href", ""))
                        ad_data = self.scrape_ad_detail(ad_url, headers)
                        if ad_data:
                            scraped_ads.append(ad_data)
                            
                    if not ad_links:
                        break
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Erreur lors du scraping de la page {page}: {str(e)}")
                    )
                    break

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Erreur lors du scraping: {str(e)}")
            )

        self.stdout.write(f"  → {len(scraped_ads)} annonces scrapées")
        return scraped_ads

    def scrape_ad_detail(self, url, headers):
        """Scrape les détails d'une annonce"""
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extraire le titre
            title_elem = soup.find("h1") or soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else "Annonce"
            
            # Extraire la description
            desc_elem = soup.find("div", class_=re.compile(r"description|content|text"))
            if not desc_elem:
                desc_elem = soup.find("p")
            description = desc_elem.get_text(strip=True) if desc_elem else "Description de l'annonce"
            
            # Extraire les images
            images = []
            img_tags = soup.find_all("img", src=re.compile(r"\.(jpg|jpeg|png|webp)", re.I))
            for img in img_tags[:5]:  # Maximum 5 images
                img_url = img.get("src") or img.get("data-src")
                if img_url:
                    img_url = urljoin(url, img_url)
                    # Filtrer les logos et images système
                    if not any(x in img_url.lower() for x in ["logo", "icon", "avatar", "default"]):
                        images.append(img_url)
            
            # Déterminer la catégorie basée sur le titre/description
            category = self.determine_category(title, description)
            subcategories = self.determine_subcategories(title, description)
            
            return {
                "title": title[:140],
                "description": description[:2000],
                "category": category,
                "subcategories": subcategories,
                "images": images,
            }
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Erreur lors du scraping de {url}: {str(e)}")
            )
            return None

    def determine_category(self, title, description):
        """Détermine la catégorie basée sur le titre et la description"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ["massage", "relaxant", "sportif", "chinois", "ivoirien"]):
            return Ad.Category.MASSAGES_SERVICES
        elif any(word in text for word in ["sextoy", "jouet", "lubrifiant", "aphrodisiaque", "parfum"]):
            return Ad.Category.PRODUITS_ADULTES
        else:
            return Ad.Category.RENCONTRES_ESCORTES

    def determine_subcategories(self, title, description):
        """Détermine les sous-catégories"""
        text = (title + " " + description).lower()
        subcats = []
        
        subcategory_mapping = {
            "massage sensuel": "Massage sensuel ou érotique",
            "massage ivoirien": "Massage Ivoirien",
            "massage relaxant": "Massage Relaxant",
            "massage sportif": "Massage sportif",
            "massage chinois": "Massage chinois",
            "massage intégral": "Massage Intégral",
            "sextoy": "Sextoy - Jouet Sexuel",
            "jouet": "Sextoy - Jouet Sexuel",
            "lubrifiant": "Lubrifiants – Huiles",
            "aphrodisiaque homme": "Aphrodisiaques homme",
            "aphrodisiaque femme": "Aphrodisiaques Femme",
            "parfum": "Parfums adultes",
            "cherche homme": "Cherche Homme",
            "cherche femme": "Cherche Femme",
            "escort": "Escort Girls",
        }
        
        for keyword, subcat in subcategory_mapping.items():
            if keyword in text and subcat not in subcats:
                subcats.append(subcat)
                if len(subcats) >= 3:  # Maximum 3 sous-catégories
                    break
        
        return subcats if subcats else ["Escort Girls"]

    def generate_fake_ads(self, cities):
        """Génère des annonces fictives si le scraping échoue"""
        fake_ads = []
        
        titles = [
            "Belle jeune femme disponible",
            "Massage relaxant professionnel",
            "Service de qualité et discret",
            "Accompagnement élégant",
            "Massage thérapeutique",
            "Rencontre agréable",
            "Service premium",
            "Accueil chaleureux",
        ]
        
        descriptions = [
            "Service de qualité avec professionnalisme et discrétion. Disponible pour vous satisfaire.",
            "Massage relaxant dans un cadre agréable. Expérience inoubliable garantie.",
            "Accompagnement élégant et discret. Disponible selon vos besoins.",
            "Service professionnel avec une approche personnalisée. Contactez-moi pour plus d'informations.",
        ]
        
        for i in range(100):  # Générer 100 annonces fictives
            fake_ads.append({
                "title": random.choice(titles) + f" {i+1}",
                "description": random.choice(descriptions),
                "category": random.choice(list(Ad.Category.choices))[0],
                "subcategories": random.sample(Ad.SUBCATEGORY_CHOICES, min(2, len(Ad.SUBCATEGORY_CHOICES))),
                "images": [],
            })
        
        return fake_ads

    def download_image(self, url, headers):
        """Télécharge une image depuis une URL"""
        try:
            response = requests.get(url, headers=headers, timeout=10, stream=True)
            response.raise_for_status()
            
            # Vérifier que c'est bien une image
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                return None
            
            # Limiter la taille à 5MB
            content = response.content
            if len(content) > 5 * 1024 * 1024:
                return None
            
            return content
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Erreur lors du téléchargement de {url}: {str(e)}")
            )
            return None

    def create_fake_image(self):
        """Crée une image fictive si le téléchargement échoue"""
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
    def create_users_and_ads(self, num_users, min_ads, max_ads, scraped_ads, cities):
        """Crée les utilisateurs et leurs annonces"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        created_users = 0
        created_ads = 0
        
        # Réutiliser les annonces scrapées
        ad_pool = scraped_ads * ((num_users * max_ads) // len(scraped_ads) + 1)
        random.shuffle(ad_pool)
        ad_index = 0
        
        for i in range(num_users):
            username = self.generate_username(i + 1)
            
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                username = f"{username}_{i+1}_{random.randint(1000, 9999)}"
            
            # Créer l'utilisateur
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
            
            # Créer les annonces pour cet utilisateur
            num_user_ads = random.randint(min_ads, max_ads)
            
            for j in range(num_user_ads):
                if ad_index >= len(ad_pool):
                    # Générer une annonce fictive si on a épuisé le pool
                    ad_data = {
                        "title": f"Annonce {i+1}-{j+1}",
                        "description": "Description de l'annonce",
                        "category": random.choice(list(Ad.Category.choices))[0],
                        "subcategories": random.sample(Ad.SUBCATEGORY_CHOICES, min(2, len(Ad.SUBCATEGORY_CHOICES))),
                        "images": [],
                    }
                else:
                    ad_data = ad_pool[ad_index].copy()
                    ad_index += 1
                
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
                    title=ad_data["title"][:140],
                    description_sanitized=description[:2000],
                    category=ad_data["category"],
                    subcategories=ad_data["subcategories"][:3],  # Maximum 3
                    city=random.choice(cities),
                    area=random.choice(["Cocody", "Yopougon", "Marcory", "Plateau", "Abobo", ""]),
                    status=Ad.Status.APPROVED,
                    is_verified=random.choice([True, False]),
                    expires_at=timezone.now() + timezone.timedelta(days=random.randint(14, 30)),
                )
                
                # Ajouter les images
                images_added = 0
                max_images = min(5, len(ad_data.get("images", [])))
                
                for img_url in ad_data.get("images", [])[:max_images]:
                    if images_added >= 5:
                        break
                    
                    img_content = self.download_image(img_url, headers)
                    
                    if not img_content:
                        img_content = self.create_fake_image()
                    
                    if img_content:
                        try:
                            ext = "jpg"
                            if img_url:
                                parsed = urlparse(img_url)
                                ext = os.path.splitext(parsed.path)[1][1:] or "jpg"
                            
                            filename = f"ad_{ad.id}_{images_added+1}.{ext}"
                            AdMedia.objects.create(
                                ad=ad,
                                image=ContentFile(img_content, name=filename),
                                is_primary=(images_added == 0),
                            )
                            images_added += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(f"Erreur lors de l'ajout de l'image: {str(e)}")
                            )
                
                # Si aucune image n'a été ajoutée, créer une image fictive
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
            
            if created_users % 50 == 0:
                self.stdout.write(f"  → {created_users} utilisateurs créés...")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nRésumé:\n"
                f"  - {created_users} utilisateurs créés\n"
                f"  - {created_ads} annonces créées\n"
            )
        )


"""
Service d'intégration CinetPay pour les paiements
"""
import hashlib
import hmac
import json
import requests
import logging
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


class CinetPayService:
    """Service pour gérer les paiements via CinetPay"""
    
    @staticmethod
    def get_config():
        """Récupère la configuration CinetPay depuis les settings"""
        site_id = getattr(settings, "CINETPAY_SITE_ID", "") or ""
        api_key = getattr(settings, "CINETPAY_API_KEY", "") or ""
        site_key = getattr(settings, "CINETPAY_SITE_KEY", "") or ""
        
        # Debug: logger les valeurs (sans exposer les clés complètes)
        logger.debug(f"CinetPay config - SITE_ID: {site_id[:5]}... (len: {len(site_id)})")
        logger.debug(f"CinetPay config - API_KEY: {api_key[:5]}... (len: {len(api_key)})")
        logger.debug(f"CinetPay config - SITE_KEY: {site_key[:5]}... (len: {len(site_key)})")
        
        return {
            "site_id": site_id,
            "api_key": api_key,
            "site_key": site_key,
            "notify_url": getattr(
                settings,
                "CINETPAY_NOTIFY_URL",
                "https://ci-kiaba.com/accounts/payment/cinetpay/notify/"
            ),
            "return_url": getattr(
                settings,
                "CINETPAY_RETURN_URL",
                "https://ci-kiaba.com/accounts/payment/cinetpay/return/"
            ),
        }

    @staticmethod
    def generate_transaction_id(user_id, transaction_id):
        """Génère un ID de transaction unique pour CinetPay"""
        return f"KIABA_{user_id}_{transaction_id}_{int(timezone.now().timestamp())}"

    @staticmethod
    def create_payment_link(transaction, amount, description):
        """Crée un lien de paiement CinetPay"""
        config = CinetPayService.get_config()
        
        # Vérifier que toutes les clés nécessaires sont présentes
        missing = []
        if not config["site_id"]:
            missing.append("CINETPAY_SITE_ID")
        if not config["api_key"]:
            missing.append("CINETPAY_API_KEY")
        
        if missing:
            raise ValueError(
                f"Configuration CinetPay incomplète. Variables manquantes: {', '.join(missing)}"
            )
        
        transaction_id = CinetPayService.generate_transaction_id(
            transaction.user_id,
            transaction.id
        )
        
        # Paramètres pour CinetPay
        params = {
            "apikey": config["api_key"],
            "site_id": config["site_id"],
            "transaction_id": transaction_id,
            "amount": str(int(float(amount))),
            "currency": "XOF",  # FCFA
            "description": description[:255],
            "notify_url": config["notify_url"],
            "return_url": config["return_url"],
            "channels": "ALL",  # Tous les canaux de paiement
        }
        
        # Générer la signature
        signature_data = (
            f"{params['amount']}{params['apikey']}{params['site_id']}"
            f"{params['transaction_id']}{params['currency']}"
        )
        signature = hashlib.sha256(signature_data.encode()).hexdigest()
        params["signature"] = signature
        
        # URL de l'API CinetPay
        api_url = "https://api.cinetpay.com/v1/payment"
        
        try:
            response = requests.post(api_url, json=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == "201":
                # Sauvegarder l'ID de transaction CinetPay
                transaction.cinetpay_transaction_id = transaction_id
                transaction.save()
                
                return data.get("data", {}).get("payment_url")
            else:
                raise ValueError(f"Erreur CinetPay: {data.get('message', 'Erreur inconnue')}")
        except requests.RequestException as e:
            raise ValueError(f"Erreur de connexion à CinetPay: {str(e)}")

    @staticmethod
    def verify_payment(cinetpay_transaction_id):
        """Vérifie le statut d'un paiement CinetPay"""
        config = CinetPayService.get_config()
        
        # Vérifier que toutes les clés nécessaires sont présentes
        missing = []
        if not config["site_id"]:
            missing.append("CINETPAY_SITE_ID")
        if not config["api_key"]:
            missing.append("CINETPAY_API_KEY")
        
        if missing:
            raise ValueError(
                f"Configuration CinetPay incomplète. Variables manquantes: {', '.join(missing)}"
            )
        
        params = {
            "apikey": config["api_key"],
            "site_id": config["site_id"],
            "transaction_id": cinetpay_transaction_id,
        }
        
        # Générer la signature
        signature_data = (
            f"{params['apikey']}{params['site_id']}{params['transaction_id']}"
        )
        signature = hashlib.sha256(signature_data.encode()).hexdigest()
        params["signature"] = signature
        
        api_url = "https://api.cinetpay.com/v1/payment/check"
        
        try:
            response = requests.post(api_url, json=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == "00":
                payment_data = data.get("data", {})
                return {
                    "status": payment_data.get("status"),
                    "amount": payment_data.get("amount"),
                    "currency": payment_data.get("currency"),
                    "payment_method": payment_data.get("payment_method"),
                }
            else:
                return None
        except requests.RequestException:
            return None

    @staticmethod
    def verify_webhook_signature(data, signature):
        """Vérifie la signature d'un webhook CinetPay"""
        config = CinetPayService.get_config()
        
        # Construire la chaîne à signer
        signature_data = (
            f"{data.get('cpm_trans_id')}{config['site_key']}"
            f"{data.get('cpm_amount')}{data.get('cpm_currency')}"
        )
        
        expected_signature = hmac.new(
            config["site_key"].encode(),
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)


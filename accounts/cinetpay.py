"""
Service d'intégration CinetPay pour les paiements
Utilise le SDK officiel CinetPay
"""
import logging
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

try:
    from cinetpay_sdk.s_d_k import Cinetpay
    CINETPAY_SDK_AVAILABLE = True
except ImportError:
    CINETPAY_SDK_AVAILABLE = False
    logger.warning("CinetPay SDK non disponible. Installation: pip install -i https://test.pypi.org/simple/ cinetpay-sdk==0.1.1")


class CinetPayService:
    """Service pour gérer les paiements via CinetPay en utilisant le SDK officiel"""
    
    @staticmethod
    def get_client():
        """Crée et retourne un client CinetPay"""
        if not CINETPAY_SDK_AVAILABLE:
            raise ValueError("CinetPay SDK non installé. Exécutez: pip install -i https://test.pypi.org/simple/ cinetpay-sdk==0.1.1")
        
        api_key = getattr(settings, "CINETPAY_API_KEY", "") or ""
        site_id = getattr(settings, "CINETPAY_SITE_ID", "") or ""
        
        if not api_key or not site_id:
            missing = []
            if not site_id:
                missing.append("CINETPAY_SITE_ID")
            if not api_key:
                missing.append("CINETPAY_API_KEY")
            raise ValueError(
                f"Configuration CinetPay incomplète. Variables manquantes: {', '.join(missing)}"
            )
        
        return Cinetpay(api_key, site_id)
    
    @staticmethod
    def generate_transaction_id(user_id, transaction_id):
        """Génère un ID de transaction unique pour CinetPay"""
        return f"KIABA_{user_id}_{transaction_id}_{int(timezone.now().timestamp())}"

    @staticmethod
    def create_payment_link(transaction, amount, description):
        """Crée un lien de paiement CinetPay"""
        try:
            client = CinetPayService.get_client()
        except ValueError as e:
            raise ValueError(str(e))
        
        # Générer l'ID de transaction
        transaction_id = CinetPayService.generate_transaction_id(
            transaction.user_id,
            transaction.id
        )
        
        # Récupérer les URLs depuis les settings
        notify_url = getattr(
            settings,
            "CINETPAY_NOTIFY_URL",
            "https://ci-kiaba.com/accounts/payment/cinetpay/notify/"
        )
        return_url = getattr(
            settings,
            "CINETPAY_RETURN_URL",
            "https://ci-kiaba.com/accounts/payment/cinetpay/return/"
        )
        
        # Récupérer les informations utilisateur
        user = transaction.user
        customer_name = user.first_name or user.username
        customer_surname = user.last_name or ""
        
        # Préparer les données pour l'initialisation du paiement
        data = {
            'amount': int(float(amount)),  # Montant en entier
            'currency': "XOF",  # FCFA
            'transaction_id': transaction_id,
            'description': description[:255],
            'return_url': return_url,
            'notify_url': notify_url,
            'customer_name': customer_name[:50] if customer_name else "Client",
            'customer_surname': customer_surname[:50] if customer_surname else "",
        }
        
        try:
            # Initialiser le paiement via le SDK
            response = client.PaymentInitialization(data)
            
            # Le SDK retourne généralement un dictionnaire avec 'code' et 'data'
            if isinstance(response, dict):
                if response.get('code') == '201' or response.get('code') == 201:
                    # Sauvegarder l'ID de transaction CinetPay
                    transaction.cinetpay_transaction_id = transaction_id
                    transaction.save()
                    
                    # Retourner l'URL de paiement
                    payment_url = response.get('data', {}).get('payment_url') or response.get('payment_url')
                    if payment_url:
                        return payment_url
                    else:
                        raise ValueError("URL de paiement non trouvée dans la réponse CinetPay")
                else:
                    error_msg = response.get('message', response.get('description', 'Erreur inconnue'))
                    raise ValueError(f"Erreur CinetPay: {error_msg}")
            else:
                # Si la réponse est directement l'URL
                if isinstance(response, str) and response.startswith('http'):
                    transaction.cinetpay_transaction_id = transaction_id
                    transaction.save()
                    return response
                else:
                    raise ValueError(f"Réponse CinetPay inattendue: {response}")
                    
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du paiement CinetPay: {str(e)}")
            raise ValueError(f"Erreur de connexion à CinetPay: {str(e)}")

    @staticmethod
    def verify_payment(cinetpay_transaction_id):
        """Vérifie le statut d'un paiement CinetPay"""
        try:
            client = CinetPayService.get_client()
        except ValueError as e:
            logger.error(f"Erreur de configuration CinetPay: {str(e)}")
            return None
        
        try:
            # Vérifier avec l'ID de transaction
            response = client.TransactionVerfication_trx(cinetpay_transaction_id)
            
            if isinstance(response, dict):
                if response.get('code') == '00' or response.get('code') == 0:
                    payment_data = response.get('data', {})
                    return {
                        "status": payment_data.get("status"),
                        "amount": payment_data.get("amount"),
                        "currency": payment_data.get("currency"),
                        "payment_method": payment_data.get("payment_method"),
                    }
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du paiement CinetPay: {str(e)}")
            return None

    @staticmethod
    def verify_webhook_signature(data, signature):
        """Vérifie la signature d'un webhook CinetPay"""
        site_key = getattr(settings, "CINETPAY_SITE_KEY", "") or ""
        
        if not site_key:
            logger.warning("CINETPAY_SITE_KEY non configuré, impossible de vérifier la signature")
            return False
        
        # Construire la chaîne à signer selon la documentation CinetPay
        import hmac
        import hashlib
        
        signature_data = (
            f"{data.get('cpm_trans_id', '')}{site_key}"
            f"{data.get('cpm_amount', '')}{data.get('cpm_currency', 'XOF')}"
        )
        
        expected_signature = hmac.new(
            site_key.encode(),
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)

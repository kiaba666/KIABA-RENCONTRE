from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpRequest, HttpResponse
from .models import Profile
from .forms import (
    ProfileEditForm,
    CustomPasswordChangeForm,
    PasswordChangeOTPRequestForm,
)
from .tasks import send_profile_validation_email, send_password_change_email
from .models import EmailOTP


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """Page de modification du profil utilisateur"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            # Sauvegarder le profil
            profile = form.save(commit=False)
            # Gérer contact_prefs manuellement
            profile.contact_prefs = form.cleaned_data.get("contact_prefs", [])
            profile.save()
            # Sauvegarder le numéro de téléphone dans l'utilisateur
            if form.cleaned_data.get("phone_e164"):
                request.user.phone_e164 = form.cleaned_data["phone_e164"]
                request.user.save()

                # Envoyer un email de validation de profil
                send_profile_validation_email.delay(profile.id)

            messages.success(request, "Profil mis à jour avec succès !")
            return redirect("/dashboard/")
    else:
        form = ProfileEditForm(instance=profile)
        # Pré-remplir le numéro de téléphone depuis l'utilisateur
        form.fields["phone_e164"].initial = request.user.phone_e164

    return render(request, "accounts/profile_edit.html", {"form": form})


@login_required
def password_change(request: HttpRequest) -> HttpResponse:
    """Modification du mot de passe en 2 étapes: 1) vérif ancien/nouveau; 2) OTP email."""
    # Étape 2 sera gérée sur une page dédiée

    # Étape 1: valider ancien/nouveau, puis envoyer un code OTP et demander le code
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Stocker le nouveau mot de passe en session (temporaire) et envoyer OTP
            cleaned = form.cleaned_data
            request.session["pending_pwd_change"] = {
                "new_password1": cleaned.get("new_password1"),
            }

            req_form = PasswordChangeOTPRequestForm(user=request.user)
            otp = req_form.save()

            from django.core.mail import send_mail
            from django.conf import settings

            # Utiliser le nouveau service d'email
            from .email_service import EmailService
            EmailService.send_email(
                subject="Code de confirmation pour changement de mot de passe",
                to_emails=[request.user.email],
                text_content=f"""Bonjour {request.user.username},

Vous avez demandé à changer votre mot de passe sur KIABA.

Votre code de confirmation est : {otp.code}

Ce code est valide pendant 10 minutes.

Si vous n'avez pas demandé ce changement, veuillez ignorer cet email ou nous contacter à support@ci-kiaba.com

Cordialement,
L'équipe KIABA""",
                fail_silently=False,
            )
            # Log dev
            print(f"[OTP] Password change code for user {request.user.id}: {otp.code}")
            messages.info(
                request, "Code envoyé par email. Saisissez-le pour confirmer le changement."
            )
            return redirect("accounts:password_change_confirm")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "accounts/password_change.html", {"form": form})


@login_required
def password_change_confirm(request: HttpRequest) -> HttpResponse:
    if not request.session.get("pending_pwd_change"):
        messages.warning(request, "Session expirée. Recommencez la modification du mot de passe.")
        return redirect("accounts:password_change")

    if request.method == "POST":
        code = (request.POST.get("code") or "").strip()
        pending = request.session.get("pending_pwd_change")
        otp = (
            EmailOTP.objects.filter(
                user=request.user,
                purpose=EmailOTP.Purpose.PASSWORD_CHANGE,
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )
        if not otp or not otp.is_valid(code):
            messages.error(request, "Code OTP incorrect ou expiré")
            return render(request, "accounts/password_change_confirm.html")

        new_password = pending.get("new_password1")
        request.user.set_password(new_password)
        request.user.save()
        otp.is_used = True
        otp.save(update_fields=["is_used"])
        request.session.pop("pending_pwd_change", None)

        update_session_auth_hash(request, request.user)
        send_password_change_email.delay(request.user.id)
        messages.success(request, "Mot de passe modifié avec succès !")
        return redirect("/dashboard/")

    return render(request, "accounts/password_change_confirm.html")


@login_required
def resend_password_change_code(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        req_form = PasswordChangeOTPRequestForm(request.POST or None, user=request.user)
        otp = req_form.save()
        
        # Utiliser le nouveau service d'email
        from .email_service import EmailService
        EmailService.send_email(
            subject="Code de confirmation pour changement de mot de passe",
            to_emails=[request.user.email],
            text_content=f"""Bonjour {request.user.username},

Vous avez demandé un nouveau code de confirmation pour changer votre mot de passe sur KIABA.

Votre code de confirmation est : {otp.code}

Ce code est valide pendant 10 minutes.

Si vous n'avez pas demandé ce changement, veuillez ignorer cet email ou nous contacter à support@ci-kiaba.com

Cordialement,
L'équipe KIABA""",
            fail_silently=False,
        )
        messages.info(request, "Nouveau code envoyé par email.")
    return redirect("accounts:password_change_confirm")


def validate_profile(request: HttpRequest, profile_id: int) -> HttpResponse:
    """Valider un profil via email"""
    profile = get_object_or_404(Profile, id=profile_id)

    # Marquer le profil comme validé
    profile.is_verified = True
    profile.save()

    messages.success(request, f"Profil de {profile.display_name} validé avec succès !")
    return redirect("/dashboard/")

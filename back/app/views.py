from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework import generics, permissions
import uuid
import random
from django.db.models import Avg
from django.conf import settings

from rest_framework.generics import get_object_or_404
# At the top of your views.py
from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from .models import PasswordResetToken
from .permissions import IsGerant, IsClient
from .models import Salle
from rest_framework import mixins, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db.models import F
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D  # D pour Distance
from django.db.models import Q, Avg, Min
from rest_framework import mixins, viewsets
from .permissions import IsGerant
from .services.geocoding import GeocodingService, geocode_and_save_salle

from .models import (
    Utilisateur,
    Client,
    Gerant,
    VerificationCode,
    PasswordResetToken,
    historiqueRecherche,
    Service, SalleService,
    Avis,
    Concerne,
    CritereNotation,
    Equipement,
    SalleEquipement,
    Formule_Abonnement,
    concerneEquipement, concerneServices,
    Course,
    Schedule,
    SallePhoto,
    HoraireOuverture,
    ConcerneCourse,
)
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializer import (
    RegisterSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    UtilisateurSerializer,
    ClientSerializer,
    GerantSerializer,
    SalleSerializer,
    ForgotPasswordSerializer,
    VerifyResetCodeSerializer,
    ResetPasswordSerializer,
    historiqueSerializer,
    ServiceSerializer,
    SalleServiceSerializer,
    SalleServiceBulkSerializer,
    SalleWithServicesSerializer,
    AvisSerializer,
    criterNotationSerializer,
    concernSerializer,
    EquipmentSerializer,
    SalleEquipementSerializer, GerantUpdateFullNameSerializer, ChangePasswordSerializer, concernEquipmentSerializer, filterSalleSerializer, FormuleAbonnementSerializer, ConcerneServicesSerializer,
    SalleSearchSerializer,
    SalleEquipementSerializer, filterSalleSerializer, FormuleAbonnementSerializer,
    CourseSerializer, ScheduleSerializer, SallePhotoSerializer, GeocodeSerializer, ConcerneCourseSerializer,
    HoraireOuvertureSerializer, GeocodeSerializer,  # ✅ Ajouté
    SallePublicDetailSerializer,  # ✅ Nouveau serializer pour les détails publics
)
from django.contrib.auth import login, logout
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# app/views.py - Add this view

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def get_authenticated_user(request):
    """
    Returns the authenticated user's information after Google OAuth
    This endpoint is called by the frontend callback component
    """
    print(f"🔍 Fetching user info for: {request.user} (Authenticated: {request.user.is_authenticated})")
    
    # Check if user is authenticated (via session from OAuth or URL token)
    if not request.user.is_authenticated:
        return Response({
            'error': 'Not authenticated'
        }, status=401)

    user = request.user

    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)

    # Get user profile if it exists
    profil = None
    if hasattr(user, 'profil'):
        profil = {
            'nom': user.profil.nom if hasattr(user.profil, 'nom') else None,
            'prenom': user.profil.prenom if hasattr(user.profil, 'prenom') else None,
            # Add other profile fields as needed
        }

    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'email': user.email,
            'type_utilisateur': user.type_utilisateur,
            'is_active': user.is_active,
        },
        'profil': profil
    })


# Add this to back/app/views.py


def custom_google_login(request):
    """
    Custom Google OAuth login that ensures redirect to frontend
    """
    # Store the frontend callback URL in session
    request.session['socialaccount_redirect_url'] = settings.LOGIN_REDIRECT_URL

    # Redirect to the standard Google OAuth endpoint
    return redirect('/accounts/google/login/')


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class SPARegisterView(RegisterView):
    # Prevent redirect to template
    def get_response_data(self, user):
        return {
            "key": self.get_response_data(user).get("key"),
            "user": {
                "id": user.id,
                "email": user.email,
            },
        }


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        existing_user = Utilisateur.objects.filter(email=email).first()

        if existing_user:
            if existing_user.email_verified:
                return Response({
                    "error": "Un compte existe déjà avec cet email. Veuillez vous connecter.",
                    "code": "EMAIL_ALREADY_VERIFIED"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Supprimer l'ancien compte non vérifié
            VerificationCode.objects.filter(email=email).delete()

            if hasattr(existing_user, 'client_profile'):
                existing_user.client_profile.delete()

            if hasattr(existing_user, 'gerant_profile'):
                if existing_user.gerant_profile.certificat_nif:
                    existing_user.gerant_profile.certificat_nif.delete()
                existing_user.gerant_profile.delete()

            existing_user.delete()
            print(f"🗑️ Ancien compte supprimé, nouveau créé : {email}")

        # Créer le nouveau compte
        serializer = RegisterSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Inscription réussie. Un code de vérification a été envoyé.",
                "email": email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        verification = serializer.validated_data['verification']

        # Activer l'email vérifié
        user.email_verified = True

        if user.type_utilisateur == 'client':
            user.is_active = True
        elif user.type_utilisateur == 'gerant':
            user.is_active = False

        user.save()

        # Marquer le code comme utilisé
        verification.is_used = True
        verification.save()

        # ✅ AJOUTER ICI : Envoyer email admin si gérant
        if user.type_utilisateur == 'gerant':
            try:
                gerant = user.gerant_profile

                print("=" * 60)
                print("ENVOI EMAIL ADMIN (APRES VERIFICATION)")
                print(f"Gerant: {user.email}")
                print(f"Email verifie: OUI")

                gerant.send_admin_notification()

                print("EMAIL ADMIN ENVOYE AVEC SUCCES")
                print(f"Token: {gerant.approval_token}")
                print("=" * 60)

            except Exception as e:
                print(f"ERREUR envoi email admin: {e}")
                # Ne pas bloquer la vérification si l'email échoue

        # Préparer la réponse
        user_data = UtilisateurSerializer(user).data

        if user.type_utilisateur == 'gerant':
            message = "Email vérifié ! Votre demande a été transmise à l'administrateur."
        else:
            message = "Email vérifié avec succès ! Vous pouvez maintenant vous connecter."

        return Response({
            "message": message,
            "user": user_data,
            "can_login": user.is_active,
            "needs_approval": user.type_utilisateur == 'gerant'
        }, status=status.HTTP_200_OK)


class ResendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response({
                "error": "Aucun compte associé à cet email"
            }, status=status.HTTP_404_NOT_FOUND)

        if user.email_verified:
            return Response({
                "error": "Cet email est déjà vérifié. Veuillez vous connecter.",
                "code": "EMAIL_ALREADY_VERIFIED"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Anti-spam : 1 code par minute
        recent_code = VerificationCode.objects.filter(
            email=email,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).first()

        if recent_code:
            temps_ecoule = (timezone.now() - recent_code.created_at).seconds
            temps_restant = 60 - temps_ecoule

            return Response({
                "error": f"Veuillez patienter {temps_restant} secondes",
                "code": "TOO_MANY_REQUESTS",
                "retry_after": temps_restant
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Vérifier si code encore valide
        code_valide = VerificationCode.objects.filter(
            email=email,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=15)
        ).first()

        if code_valide:
            temps_restant = (15 * 60) - (timezone.now() -
                                         code_valide.created_at).seconds
            minutes = temps_restant // 60
            secondes = temps_restant % 60

            return Response({
                "message": "Un code valide existe déjà. Vérifiez votre email.",
                "code": "CODE_STILL_VALID",
                "expires_in": {
                    "minutes": minutes,
                    "seconds": secondes,
                    "total_seconds": temps_restant
                }
            }, status=status.HTTP_200_OK)

        # Code expiré → nouveau code
        VerificationCode.objects.filter(
            email=email, is_used=False).update(is_used=True)

        code = str(random.randint(100000, 999999))
        VerificationCode.objects.create(email=email, code=code)

        send_mail(
            subject="🔄 Nouveau code de vérification - DZ-Fit",
            message=f"""
Bonjour {user.full_name},

Votre nouveau code de vérification : {code}

Ce code est valable pendant 15 minutes.

Cordialement,
L'équipe DZ-Fit
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )

        return Response({
            "message": "Un nouveau code a été envoyé à votre email",
            "code": "NEW_CODE_SENT",
            "valid_for_minutes": 15
        }, status=status.HTTP_200_OK)

# API LOGIN
# ===============================


class LoginView(APIView):
    """
    API pour se connecter
    POST /api/auth/login/

    Body: {
        "email": "user@example.com",
        "password": "motdepasse"
    }

    Response: {
        "message": "Connexion réussie",
        "token": "abc123...",
        "user": { ... },
        "profil": { ... }
    }
    """
    permission_classes = [AllowAny]  # Tout le monde peut accéder

    def post(self, request):
        # Valider les données avec le serializer
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )

        # Si les données sont invalides, retourner les erreurs
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer l'utilisateur validé
        user = serializer.validated_data['user']

        # Créer ou récupérer le token d'authentification
        token, created = Token.objects.get_or_create(user=user)

        # Connecter l'utilisateur à la session Django
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Préparer les données de l'utilisateur
        user_data = UtilisateurSerializer(user).data

        # Récupérer le profil spécifique (client ou gérant)
        profil_data = None

        if user.type_utilisateur == 'client':
            try:
                profil = user.client_profile
                profil_data = ClientSerializer(profil).data
            except:
                profil_data = None

        elif user.type_utilisateur == 'gerant':
            try:
                profil = user.gerant_profile
                profil_data = GerantSerializer(profil).data
            except:
                profil_data = None

        # Retourner la réponse
        return Response({
            'message': 'Connexion réussie',
            'token': token.key,
            'user': user_data,
            'profil': profil_data
        }, status=status.HTTP_200_OK)

    # ===============================
# API LOGOUT
# ===============================


class LogoutView(APIView):
    """
    API pour se déconnecter
    POST /api/auth/logout/

    Headers: {
        "Authorization": "Token abc123..."
    }

    Response: {
        "message": "Déconnexion réussie"
    }
    """
    permission_classes = [
        IsAuthenticated]  # Seulement les utilisateurs connectés

    def post(self, request):
        try:
            # Supprimer le token de l'utilisateur
            request.user.auth_token.delete()
        except Exception as e:
            pass

        # Déconnecter l'utilisateur de la session Django
        logout(request)

        return Response({
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)


# ===============================
# ÉTAPE 1 : DEMANDER LE CODE (inchangée)
# ===============================
class ForgotPasswordView(APIView):
    """
    Envoie un code de réinitialisation par email
    POST /api/auth/forgot-password/

    Body: {
        "email": "user@example.com"
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        code = str(random.randint(1000, 9999))

        # Invalider les anciens codes pour cet email
        PasswordResetToken.objects.filter(email=email, is_used=False).delete()

        # Créer le nouveau token
        PasswordResetToken.objects.create(
            email=email,
            token=code
        )

        # Envoyer l'email
        try:
            send_mail(
                "Réinitialisation de votre mot de passe",
                f"Votre code de réinitialisation est : {code}\n\nCe code est valable pendant 15 minutes.",
                settings.DEFAULT_FROM_EMAIL,   # ✅ هنا
                [email],
                fail_silently=False
            )

            return Response({
                "message": "Un code de réinitialisation a été envoyé à votre email"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Erreur lors de l'envoi de l'email"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ===============================
# ÉTAPE 2 : VÉRIFIER LE CODE ✅ MODIFIÉE
# ===============================
class VerifyResetCodeView(APIView):
    """
    Vérifie le code et retourne un reset_token
    POST /api/auth/verify-reset-code/

    Body: {
        "email": "user@example.com",
        "code": "123456"
    }

    Response: {
        "message": "Code valide",
        "reset_token": "abc123..."  ✅ Token pour l'étape suivante
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        # Récupérer le token
        reset_entry = PasswordResetToken.objects.get(
            email=email,
            token=code,
            is_used=False,
            is_verified=False
        )

        # Générer un reset_token unique
        reset_token = str(uuid.uuid4())

        # Marquer comme vérifié et sauvegarder le reset_token
        reset_entry.is_verified = True
        reset_entry.reset_token = reset_token
        reset_entry.save()

        return Response({
            "message": "Code valide",
            "reset_token": reset_token  # ✅ On retourne ce token au frontend
        }, status=status.HTTP_200_OK)


# ===============================
# ÉTAPE 3 : CHANGER LE MOT DE PASSE ✅ MODIFIÉE
# ===============================
class ResetPasswordView(APIView):
    """
    Réinitialise le mot de passe avec le reset_token
    POST /api/auth/reset-password/

    Body: {
        "reset_token": "abc123...",  ✅ Plus besoin de email ni code
        "new_password": "nouveaumotdepasse",
        "confirm_password": "nouveaumotdepasse"
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        reset_token = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['new_password']

        # Récupérer l'entrée de réinitialisation
        try:
            reset_entry = PasswordResetToken.objects.get(
                reset_token=reset_token,
                is_used=False,
                is_verified=True
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"error": "Token invalide ou expiré"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer l'utilisateur
        try:
            user = Utilisateur.objects.get(email=reset_entry.email)
        except Utilisateur.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Changer le mot de passe
        user.set_password(new_password)
        user.save()

        # Marquer comme utilisé
        reset_entry.is_used = True
        reset_entry.save()

        return Response({
            "message": "Mot de passe réinitialisé avec succès"
        }, status=status.HTTP_200_OK)


def approve_gerant_by_token(request, token):
    """
    GET /api/admin/approve-gerant/<token>/

    Approuve un gérant via le lien dans l'email
    """
    try:
        gerant = Gerant.objects.get(approval_token=token)
    except Gerant.DoesNotExist:
        # Token invalide ou déjà utilisé
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
                .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .error {{ color: #f44336; font-size: 48px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="error">❌</div>
                <h2>Lien invalide ou expiré</h2>
                <p>Ce lien d'approbation n'est plus valide. Il peut avoir déjà été utilisé ou expiré.</p>
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    Veuillez contacter l'administrateur pour plus d'informations.
                </p>
            </div>
        </body>
        </html>
        """, content_type='text/html')

    # Vérifier si déjà traité
    if gerant.statut_approbation != 'en_attente':
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
                .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .warning {{ color: #ff9800; font-size: 48px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="warning">⚠️</div>
                <h2>Action déjà effectuée</h2>
                <p>Ce gérant a déjà été <strong>{gerant.get_statut_approbation_display()}</strong>.</p>
            </div>
        </body>
        </html>
        """, content_type='text/html')

    # Approuver
    gerant.approuver()

    # Invalider le token
    gerant.approval_token = None
    gerant.save()

    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
            .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .success {{ color: #4caf50; font-size: 48px; }}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="success">✅</div>
            <h2>Gérant Approuvé</h2>
            <p><strong>{gerant.utilisateur.full_name}</strong> a été approuvé avec succès.</p>
            <p>Un email de confirmation lui a été envoyé.</p>
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                Vous pouvez fermer cette fenêtre.
            </p>
        </div>
    </body>
    </html>
    """, content_type='text/html')


def reject_gerant_by_token(request, token):
    """
    GET /api/admin/reject-gerant/<token>/

    Rejette un gérant via le lien dans l'email
    """
    try:
        gerant = Gerant.objects.get(approval_token=token)
    except Gerant.DoesNotExist:
        # Token invalide ou déjà utilisé
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
                .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .error {{ color: #f44336; font-size: 48px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="error">❌</div>
                <h2>Lien invalide ou expiré</h2>
                <p>Ce lien de rejet n'est plus valide. Il peut avoir déjà été utilisé ou expiré.</p>
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    Veuillez contacter l'administrateur pour plus d'informations.
                </p>
            </div>
        </body>
        </html>
        """, content_type='text/html')

    # Vérifier si déjà traité
    if gerant.statut_approbation != 'en_attente':
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
                .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .warning {{ color: #ff9800; font-size: 48px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="warning">⚠️</div>
                <h2>Action déjà effectuée</h2>
                <p>Ce gérant a déjà été <strong>{gerant.get_statut_approbation_display()}</strong>.</p>
            </div>
        </body>
        </html>
        """, content_type='text/html')

    # Rejeter avec raison par défaut
    raison = "Document non conforme ou informations incomplètes"
    gerant.rejeter(raison)

    # Invalider le token
    gerant.approval_token = None
    gerant.save()

    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }}
            .box {{ background: white; padding: 40px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .error {{ color: #f44336; font-size: 48px; }}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="error">❌</div>
            <h2>Gérant Rejeté</h2>
            <p>La demande de <strong>{gerant.utilisateur.full_name}</strong> a été rejetée.</p>
            <p>Un email lui a été envoyé avec la raison du rejet.</p>
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                Vous pouvez fermer cette fenêtre.
            </p>
        </div>
    </body>
    </html>
    """, content_type='text/html')


class GerantUpdateFullNameView(generics.UpdateAPIView):
    serializer_class = GerantUpdateFullNameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        # ✅ تأكد أنه gérant
        if not hasattr(user, "gerant_profile"):
            raise PermissionDenied("Vous n'êtes pas un gérant")

        return user


class GerantChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        user = self.request.user

        # ✅ فقط gérant
        if not hasattr(user, "gerant_profile"):
            raise PermissionDenied("Vous n'êtes pas un gérant")

        return user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Mot de passe modifié avec succès"},
            status=status.HTTP_200_OK
        )


class SalleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = SalleSerializer
    permission_classes = [IsGerant]

    def get_queryset(self):
        return Salle.objects.filter(gerant=self.request.user.gerant_profile)

    def perform_create(self, serializer):
        instance = serializer.save(gerant=self.request.user.gerant_profile)
        # ✅ Géocodage automatique à la création
        geocode_and_save_salle(instance)


class DetailSalleViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    serializer_class = SalleSerializer
    permission_classes = [IsGerant]

    lookup_field = 'id'

    def get_queryset(self):
        # Filter to ensure the executing user (gerant) owns the salle
        return Salle.objects.filter(gerant=self.request.user.gerant_profile)

    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)

    def perform_update(self, serializer):
        instance = serializer.save()
        # ✅ Géocodage automatique à la mise à jour
        geocode_and_save_salle(instance)


class AllSalleViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin   # ✅ أضف هذا
):
    serializer_class = SalleSerializer
    queryset = Salle.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 🔥 زيادة عدد المشاهدات
        Salle.objects.filter(pk=instance.pk).update(
            views_count=F('views_count') + 1
        )

        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HistoriqueRechercheView(generics.ListCreateAPIView):
    serializer_class = historiqueSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        client = self.request.user.client_profile
        return historiqueRecherche.objects.filter(clientHistorique=client)

    def perform_create(self, serializer):
        client = self.request.user.client_profile
        serializer.save(clientHistorique=client)


class historiqueRechercheDetail(generics.RetrieveAPIView):
    serialzer_class = historiqueSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]
    lookup_field = 'id'

    def get_queryset(self):
        client = self.request.user.client_profile

        return historiqueRecherche.objects.filter(clientHistorique=self.request.user.client)


class ServiceListView(APIView):
    """GET /api/services/ - Liste tous les services disponibles"""
    permission_classes = [AllowAny]

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalleServiceView(APIView):
    """Gérer les services d'une salle"""
    permission_classes = [IsAuthenticated, IsGerant]

    def get_salle(self, salle_id):
        try:
            return Salle.objects.get(
                id=salle_id,
                gerant=self.request.user.gerant_profile
            )
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

    def get(self, request, salle_id):
        """GET /api/salles/{salle_id}/services/ - Voir les services de la salle"""
        salle = self.get_salle(salle_id)
        services = SalleService.objects.filter(
            salle=salle).select_related('service')
        serializer = SalleServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, salle_id):
        """POST /api/salles/{salle_id}/services/ - Remplacer tous les services"""
        salle = self.get_salle(salle_id)
        serializer = SalleServiceBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_ids = serializer.validated_data['service_ids']

        # Supprimer les anciens
        SalleService.objects.filter(salle=salle).delete()

        # Ajouter les nouveaux
        services_to_create = [
            SalleService(salle=salle, service_id=service_id)
            for service_id in service_ids
        ]
        SalleService.objects.bulk_create(services_to_create)

        # Retourner le résultat
        updated_services = SalleService.objects.filter(
            salle=salle).select_related('service')
        result_serializer = SalleServiceSerializer(updated_services, many=True)

        return Response({
            'message': f'{len(service_ids)} services configurés avec succès',
            'services': result_serializer.data
        }, status=status.HTTP_200_OK)


class SalleServiceAddView(APIView):
    """POST /api/salles/{salle_id}/services/add/ - Ajouter un service"""
    permission_classes = [IsAuthenticated, IsGerant]

    def post(self, request, salle_id):
        try:
            salle = Salle.objects.get(
                id=salle_id,
                gerant=request.user.gerant_profile
            )
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        service_id = request.data.get('service_id')

        if not service_id:
            return Response(
                {'error': 'service_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response(
                {'error': 'Service introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        salle_service, created = SalleService.objects.get_or_create(
            salle=salle,
            service=service
        )

        serializer = SalleServiceSerializer(salle_service)

        return Response({
            'message': 'Service ajouté' if created else 'Service déjà présent',
            'created': created,
            'service': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SalleServiceDeleteView(APIView):
    """DELETE /api/salles/{salle_id}/services/{service_id}/ - Supprimer un service"""
    permission_classes = [IsAuthenticated, IsGerant]

    def delete(self, request, salle_id, service_id):
        try:
            salle = Salle.objects.get(
                id=salle_id,
                gerant=request.user.gerant_profile
            )
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        try:
            salle_service = SalleService.objects.get(
                salle=salle,
                service_id=service_id
            )
            salle_service.delete()

            return Response({
                'message': 'Service supprimé avec succès'
            }, status=status.HTTP_200_OK)

        except SalleService.DoesNotExist:
            return Response({
                'error': 'Ce service n\'est pas associé à cette salle'
            }, status=status.HTTP_404_NOT_FOUND)


class SalleDetailPublicView(generics.RetrieveAPIView):
    """GET /api/salles/{id}/ - Profil public d'une salle avec toutes les données"""
    serializer_class = SallePublicDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    queryset = Salle.objects.all().prefetch_related('services__service')


class AvisView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = AvisSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsClient()]

    def get_queryset(self):
        salle_id = self.kwargs.get("salle_id")
        return Avis.objects.filter(salle__id=salle_id)

    def perform_create(self, serializer):
        client = self.request.user.client_profile
        salle_id = self.kwargs.get("salle_id")
        salle = get_object_or_404(Salle, id=salle_id)
        serializer.save(client=client, salle=salle)

    def delete(self, request, salle_id=None, avis_id=None):
        client = request.user.client_profile
        try:
            avis = Avis.objects.get(
                id=avis_id,
                client=client
            )
            avis.delete()
            return Response({"message": "Comment deleted"}, status=204)
        except Avis.DoesNotExist:
            return Response({"error": "Avis not found or not authorized"}, status=404)


class CritereConcernsViewSet(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, salle_id, criter_id, *args, **kwargs):
        try:
            criter = CritereNotation.objects.get(id=criter_id)
        except CritereNotation.DoesNotExist:
            return Response({"detail": "CritereNotation not found"}, status=404)

        equipements = concerneEquipement.objects.filter(
            SalleEquipement_id=salle_id,
            critere=criter
        )
        services = concerneServices.objects.filter(
            Salleservices__salle_id=salle_id,
            critere=criter
        )

        return Response({
            "equipements": concernEquipmentSerializer(equipements, many=True).data,
            "services": ConcerneServicesSerializer(services, many=True).data
        })


class CriterNotationViewSet(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = criterNotationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGerant]

    def get_queryset(self):
        # Optional: filter by gerant if CritereNotation is linked to gerant
        return CritereNotation.objects.all()

    # GET /api/criter/ or /api/criter/<id>/
    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                obj = CritereNotation.objects.get(id=id)
            except CritereNotation.DoesNotExist:
                return Response({"detail": "CritereNotation not found"}, status=404)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        return self.list(request, *args, **kwargs)

    # POST /api/criter/
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # PUT /api/criter/<id>/
    def put(self, request, id=None, *args, **kwargs):
        if not id:
            return Response({"detail": "ID is required in URL"}, status=400)
        try:
            obj = CritereNotation.objects.get(id=id)
        except CritereNotation.DoesNotExist:
            return Response({"detail": "CritereNotation not found"}, status=404)

        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    # DELETE /api/criter/<id>/
    def delete(self, request, id=None, *args, **kwargs):
        if not id:
            return Response({"detail": "ID is required in URL"}, status=400)
        try:
            obj = CritereNotation.objects.get(id=id)
        except CritereNotation.DoesNotExist:
            return Response({"detail": "CritereNotation not found"}, status=404)

        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=204)


"""
class ConcernViewSet(generics.GenericAPIView,
                     ListModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = concernSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        # Only return concerns for the logged-in client
        return Concerne.objects.filter(client=self.request.user.client_profile)

    def get_object(self):
        salle_id = self.kwargs.get("salle_id")
        return Concerne.objects.filter(
            salle_id=salle_id, client=self.request.user.client_profile
        ).first()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client_profile)

    # PUT/PATCH support
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ConcernEquipmentViewSet(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = concernEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        # List all concerns for the logged-in client
        return concerneEquipement.objects.filter(client=self.request.user.client_profile)

    def get_object(self):
        salle_id = self.kwargs.get("salle_id")
        obj = concerneEquipement.objects.filter(
            SalleEquipement_id=salle_id,
            client=self.request.user.client_profile
        ).first()
        if not obj:
            raise NotFound("No concerneEquipement matches the given query.")
        return obj

    def perform_create(self, serializer):
        salle_id = self.kwargs.get("salle_id")
        salle = SalleEquipement.objects.get(id=salle_id)
        serializer.save(client=self.request.user.client_profile,
                        SalleEquipement=salle)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ConcerneServicesViewSet(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = ConcerneServicesSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        # List all services concerns of the logged-in client
        return concerneServices.objects.filter(client=self.request.user.client_profile)

    def get_object(self):
        service_id = self.kwargs.get("service_id")
        obj = concerneServices.objects.filter(
            Salleservices_id=service_id,
            client=self.request.user.client_profile
        ).first()
        if not obj:
            raise NotFound("No concerneServices matches the given query.")
        return obj

    def perform_create(self, serializer):
        service_id = self.kwargs.get("service_id")
        salle_service = SalleService.objects.get(id=service_id)
        serializer.save(client=self.request.user.client_profile,
                        Salleservices=salle_service)

    # PUT -> update
    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE -> delete
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    # GET -> list
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # POST -> create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class ConcernCourseViewSet(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = ConcerneCourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        # List all concerns for the logged-in client
        return ConcerneCourse.objects.filter(client=self.request.user.client_profile)

    def get_object(self):
        salle_id = self.kwargs.get("salle_id")
        course_id = self.kwargs.get("course_id")
        obj = ConcerneCourse.objects.filter(
            course__id=course_id,
            course__salle__id=salle_id,
            client=self.request.user.client_profile
        ).first()
        if not obj:
            raise NotFound("No ConcerneCourse matches the given query.")
        return obj

    def perform_create(self, serializer):
        salle_id = self.kwargs.get("salle_id")
        course_id = self.kwargs.get("course_id")
        course = Course.objects.get(id=course_id, salle__id=salle_id)
        serializer.save(client=self.request.user.client_profile, course=course)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

"""


class AddConcernView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, salle_id, *args, **kwargs):
        user_client = request.user.client_profile
        salle = get_object_or_404(Salle, id=salle_id)

        # Expecting a list of ratings from the frontend
        # Example: [{"type": "equipment", "target_id": 1, "note": 4}, ...]
        ratings_data = request.data.get("ratings", [])
        # The ID for Cleanliness, Price, etc.
        critere_id = request.data.get("critere")

        if not ratings_data:
            return Response({"detail": "No ratings provided."}, status=400)

        # Check if the user is trying to mix General and Specific in this request
        types = {r.get("type") for r in ratings_data}
        if "general" in types and len(types) > 1:
            raise ValidationError(
                {"detail": "Cannot submit General and Specific ratings together."})

        # --- EXCLUSIVITY LOGIC ---
        if "general" in types:
            # Check if they already have specific ratings in the DB
            has_specific = (
                concerneEquipement.objects.filter(client=user_client, SalleEquipement__salle=salle).exists() or
                concerneServices.objects.filter(client=user_client, Salleservices__salle=salle).exists() or
                ConcerneCourse.objects.filter(
                    client=user_client, course__salle=salle).exists()
            )
            if has_specific:
                raise ValidationError(
                    {"detail": "Delete specific ratings before adding a general one."})

            # Save General
            rating = ratings_data[0]
            Concerne.objects.update_or_create(
                salle=salle, client=user_client, critere_id=critere_id,
                defaults={"note_etoile": rating.get("note")}
            )
        else:
            # Check if they already have a general rating in the DB
            if Concerne.objects.filter(salle=salle, client=user_client).exists():
                raise ValidationError(
                    {"detail": "Delete general rating before adding specific ones."})

            # Save all specific ratings provided
            for r in ratings_data:
                target_id = r.get("target_id")
                note = r.get("note")

                if r.get("type") == "equipment":
                    concerneEquipement.objects.update_or_create(
                        SalleEquipement_id=target_id, client=user_client, critere_id=critere_id,
                        defaults={"note_etoile": note}
                    )
                elif r.get("type") == "service":
                    concerneServices.objects.update_or_create(
                        Salleservices_id=target_id, client=user_client, critere_id=critere_id,
                        defaults={"note_etoile": note}
                    )
                elif r.get("type") == "course":
                    ConcerneCourse.objects.update_or_create(
                        course_id=target_id, client=user_client, critere_id=critere_id,
                        defaults={"note_etoile": note}
                    )

        # --- RECALCULATE GLOBAL AVG ---
        self.update_salle_avg(salle)

        return Response({"detail": "Ratings submitted successfully."}, status=status.HTTP_201_CREATED)

    def update_salle_avg(self, salle):
        # Calculate average including general if specific doesn't exist
        # Or average of specifics if general doesn't exist
        ...  # (Logic to sum up all notes and divide by count)


class SalleConcernsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, salle_id, *args, **kwargs):
        # 1. Query the data
        general_qs = Concerne.objects.filter(salle_id=salle_id)
        services_qs = concerneServices.objects.filter(
            Salleservices__salle_id=salle_id)
        equipments_qs = concerneEquipement.objects.filter(
            SalleEquipement__salle_id=salle_id)
        courses_qs = ConcerneCourse.objects.filter(course__salle_id=salle_id)

        # 2. Calculate average per category
        avg_gen = general_qs.aggregate(Avg('note_etoile'))[
            'note_etoile__avg'] or 0
        avg_serv = services_qs.aggregate(Avg('note_etoile'))[
            'note_etoile__avg'] or 0
        avg_equip = equipments_qs.aggregate(Avg('note_etoile'))[
            'note_etoile__avg'] or 0
        avg_course = courses_qs.aggregate(Avg('note_etoile'))[
            'note_etoile__avg'] or 0

        # 3. Logic: If specifics exist, they define the General Score
        specific_scores = [v for v in [
            avg_serv, avg_equip, avg_course] if v > 0]

        if specific_scores:
            # Average of the specific categories
            final_general_score = sum(specific_scores) / len(specific_scores)
        else:
            # Fallback to the General table if no specific ratings exist
            final_general_score = avg_gen

        return Response({
            # This is your '4.7'
            "overall_rating": round(final_general_score, 1),
            "stats": {
                "services": round(avg_serv, 1),
                "equipment": round(avg_equip, 1),
                "courses": round(avg_course, 1),
            },
            "reviews": {
                "general": concernSerializer(general_qs, many=True).data,
                "services": ConcerneServicesSerializer(services_qs, many=True).data,
                "equipments": concernEquipmentSerializer(equipments_qs, many=True).data,
                "courses": ConcerneCourseSerializer(courses_qs, many=True).data,
            }
        })


class EquipementViewset(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SalleEquipementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        salle_id = self.kwargs.get("salle_id")
        return SalleEquipement.objects.filter(salle__id=salle_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class allEquipementViewset(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return Equipement.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EquipementGerantViewset(generics.GenericAPIView,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = SalleEquipementSerializer
    permission_classes = [permissions.IsAuthenticated, IsGerant]

    def get_queryset(self):
        salle_id = self.kwargs.get("salle_id")
        return SalleEquipement.objects.filter(
            salle__id=salle_id,
            salle__gerant=self.request.user.gerant_profile
        )

    def perform_create(self, serializer):
        salle_id = self.kwargs.get("salle_id")
        salle = Salle.objects.get(
            id=salle_id,
            gerant=self.request.user.gerant_profile
        )
        serializer.save(salle=salle)

    def delete(self, request, salle_id=None, equipement_id=None):
        gerant = request.user.gerant_profile
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        try:
            salle_equipement = SalleEquipement.objects.get(
                salle=salle,
                equipement_id=equipement_id
            )
            salle_equipement.delete()
            return Response({'message': 'Équipement supprimé avec succès'}, status=200)

        except SalleEquipement.DoesNotExist:
            return Response({'error': "Cet équipement n'est pas associé à cette salle"}, status=404)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FilterSalleViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = filterSalleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Salle.objects.all()
        equip_id = self.request.query_params.get("equip_id")
        service_id = self.request.query_params.get("services")
        course_id = self.request.query_params.get("course")
        target_day = self.request.query_params.get("day")   # e.g., 'LUNDI'
        target_time = self.request.query_params.get("time")

        if equip_id:
            queryset = queryset.filter(
                salle_equipements__equipement__id=equip_id
            )

        if service_id:
            queryset = queryset.filter(
                services__service__id=service_id
            )
        if course_id:
            queryset = queryset.filter(courses__id=course_id)

        if target_day and target_time:
            queryset = queryset.filter(
                horaires_ouverture__jourSemaine=target_day.upper(),
                horaires_ouverture__estFerme=False,
                horaires_ouverture__heureOuverture__lte=target_time,
                horaires_ouverture__heureFermeture__gte=target_time
            )

        # MOVED OUTSIDE THE IF BLOCK:
        return queryset.distinct()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FilterOptionsView(APIView):
    """
    GET /api/filters/
    Returns metadata for search filters
    """
    permission_classes = [AllowAny]

    def get(self, request):
        services = Service.objects.all()
        equipment = Equipement.objects.all()

        data = {
            "distances": [
                {"label": "1 km", "value": "1"},
                {"label": "5 km", "value": "5"},
                {"label": "10 km", "value": "10"},
                {"label": "25 km", "value": "25"},
                {"label": "50 km", "value": "50"},
                {"label": "100 km", "value": "100"}
            ],
            "equipment": [eq.name for eq in equipment],
            "services": [ser.get_nom_display() for ser in services],
            "days": [
                {"label": "Lundi", "value": "LUNDI"},
                {"label": "Mardi", "value": "MARDI"},
                {"label": "Mercredi", "value": "MERCREDI"},
                {"label": "Jeudi", "value": "JEUDI"},
                {"label": "Vendredi", "value": "VENDREDI"},
                {"label": "Samedi", "value": "SAMEDI"},
                {"label": "Dimanche", "value": "DIMANCHE"}
            ],
            "times": ["Matin", "Soir", "Ouvert maintenant"],
            "ratings": [
                {"label": "4 étoiles & plus", "value": "4"},
                {"label": "3 étoiles & plus", "value": "3"},
                {"label": "Tous", "value": "0"}
            ]
        }
        return Response(data)


class UnifiedSalleSearchView(generics.ListAPIView):
    """
    GET /api/salles/search/
    Unified search with text, distance, and filters
    """
    serializer_class = SalleSearchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        from django.contrib.gis.geos import Point
        from django.contrib.gis.db.models.functions import Distance
        from django.db.models import Avg, F, Q
        from django.contrib.gis.measure import D
        from django.db.models.functions import Cast
        from django.contrib.gis.db.models import PointField
        from django.db.models import Func
        import datetime

        # Base functon to make a point from lat/long columns
        class MakePoint(Func):
            function = 'ST_MakePoint'
            output_field = PointField()
            arity = 2

        # Get base queryset with average rating
        queryset = Salle.objects.annotate(
            note_moyenne=Avg('avis__note_globale')
        )

        search_query = self.request.query_params.get('search')
        distance_param = self.request.query_params.get('distance')
        equipment_param = self.request.query_params.get('equipment')
        services_param = self.request.query_params.get('services')
        rating_param = self.request.query_params.get('rating')

        lat_param = self.request.query_params.get('lat')
        lng_param = self.request.query_params.get('lng')

        day_param = self.request.query_params.get('day')
        time_param = self.request.query_params.get('time')

        # Text search
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(ville__icontains=search_query) |
                Q(wilaya__icontains=search_query)
            )

        # PostGIS Distance Filter
        if lat_param and lng_param:
            try:
                user_lat = float(lat_param)
                user_lng = float(lng_param)
                user_location = Point(user_lng, user_lat, srid=4326)

                # Annotate with distance
                queryset = queryset.annotate(
                    geom_point=Cast(
                        MakePoint(F('longitude'), F('latitude')),
                        output_field=PointField()
                    )
                ).annotate(
                    distance=Distance('geom_point', user_location)
                )

                # Filter by distance if valid
                if distance_param:
                    dist_km = float(distance_param)
                    queryset = queryset.filter(distance__lte=D(km=dist_km))

                # Sort by distance
                queryset = queryset.order_by('distance')

            except (ValueError, TypeError) as e:
                print(f"PostGIS Error: {e}")
                pass

        # Equipment filter
        if equipment_param:
            queryset = queryset.filter(
                salle_equipements__equipement__name=equipment_param)

        # Services filter
        if services_param:
            queryset = queryset.filter(
                services__service__nom=services_param.lower())

        # Day Filter
        if day_param:
            queryset = queryset.filter(
                horaires_ouverture__jourSemaine=day_param,
                horaires_ouverture__estFerme=False
            )

        # Time Filter
        if time_param:
            import datetime
            now = datetime.datetime.now()

            # Logic: If Day param is present, we filter time on that day.
            # If no Day param, we assume Today (standard behavior) or Apply to ANY day?
            # Standard UX: If I pick "Matin", I expect gyms open in the morning.
            # Usually implies "On the selected day" or "Generally".
            # Let's assume on Selected Day if present, otherwise ignore time or check all?
            # Actually, user said: "Journées ouvert et autre pour matin et soir"

            # If user selects 'Ouvert maintenant', it overrides Day param implicitly or checks current time/day
            if time_param == 'Ouvert maintenant':
                current_time = now.time()
                current_day_eng = now.strftime('%A').upper()
                DAYS_MAP = {
                    'MONDAY': 'LUNDI', 'TUESDAY': 'MARDI', 'WEDNESDAY': 'MERCREDI',
                    'THURSDAY': 'JEUDI', 'FRIDAY': 'VENDREDI', 'SATURDAY': 'SAMEDI',
                    'SUNDAY': 'DIMANCHE'
                }
                current_day = DAYS_MAP.get(current_day_eng, 'LUNDI')

                queryset = queryset.filter(
                    horaires_ouverture__jourSemaine=current_day,
                    horaires_ouverture__heureOuverture__lte=current_time,
                    horaires_ouverture__heureFermeture__gte=current_time,
                    horaires_ouverture__estFerme=False
                )

            elif time_param == 'Matin':
                # Open before 10 AM
                queryset = queryset.filter(
                    horaires_ouverture__heureOuverture__lte=datetime.time(
                        10, 0),
                    horaires_ouverture__estFerme=False
                )

            elif time_param == 'Soir':
                # Open after 18 PM (or closes late)
                queryset = queryset.filter(
                    horaires_ouverture__heureFermeture__gte=datetime.time(
                        18, 0),
                    horaires_ouverture__estFerme=False
                )

            else:
                # Specific time "HH:MM"
                try:
                    target_time = datetime.datetime.strptime(
                        time_param, '%H:%M').time()
                    queryset = queryset.filter(
                        horaires_ouverture__heureOuverture__lte=target_time,
                        horaires_ouverture__heureFermeture__gte=target_time,
                        horaires_ouverture__estFerme=False
                    )
                except ValueError:
                    pass

        # Rating filter
        if rating_param and float(rating_param) > 0:
            queryset = queryset.filter(note_moyenne__gte=float(rating_param))

        return queryset.distinct()


class FormuleAbonnementViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = FormuleAbonnementSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Formule_Abonnement.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FormuleAbonnementGerantViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = FormuleAbonnementSerializer
    permission_classes = [permissions.IsAuthenticated, IsGerant]

    def get_queryset(self):
        salle_id = self.kwargs.get("salle_id")
        return Formule_Abonnement.objects.filter(
            salle__id=salle_id,
            salle__gerant=self.request.user.gerant_profile
        )

    def perform_create(self, serializer):
        salle_id = self.kwargs.get("salle_id")
        salle = Salle.objects.get(
            id=salle_id,
            gerant=self.request.user.gerant_profile
        )
        serializer.save(salle=salle)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FormuleAbonnementDetailViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = FormuleAbonnementSerializer
    permission_classes = [permissions.IsAuthenticated, IsGerant]

    def get_queryset(self):
        salle_id = self.kwargs.get("salle_id")
        return Formule_Abonnement.objects.filter(
            salle__id=salle_id,
            salle__gerant=self.request.user.gerant_profile
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# ============================================
# COURSES VIEWS
# ============================================

class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/salles/{salle_id}/courses/ - Liste des cours
    POST /api/salles/{salle_id}/courses/ - Créer un cours
    """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsGerant]

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        # Vérifier que la salle appartient au gérant
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        return Course.objects.filter(salle=salle)

    def perform_create(self, serializer):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        # Récupérer la salle
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        serializer.save(salle=salle)

    def get_serializer_context(self):
        """Passer la salle au serializer pour validation"""
        context = super().get_serializer_context()
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
            context['salle'] = salle
        except Salle.DoesNotExist:
            pass

        return context


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/salles/{salle_id}/courses/{id}/ - Détails d'un cours
    PUT    /api/salles/{salle_id}/courses/{id}/ - Modifier un cours
    DELETE /api/salles/{salle_id}/courses/{id}/ - Supprimer un cours
    """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsGerant]
    lookup_field = 'id'

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        return Course.objects.filter(
            salle__id=salle_id,
            salle__gerant=gerant
        )

    def get_serializer_context(self):
        """Passer la salle au serializer pour validation"""
        context = super().get_serializer_context()
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
            context['salle'] = salle
        except Salle.DoesNotExist:
            pass

        return context


class ScheduleListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/salles/{salle_id}/schedules/ - Liste des créneaux
    POST /api/salles/{salle_id}/schedules/ - Créer un créneau
    """
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsGerant]

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        # Vérifier que la salle appartient au gérant
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        return Schedule.objects.filter(salle=salle).select_related('course')

    def perform_create(self, serializer):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        # Récupérer la salle
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        serializer.save(salle=salle)

    def get_serializer_context(self):
        """Passer la salle au serializer pour validation"""
        context = super().get_serializer_context()
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
            context['salle'] = salle
        except Salle.DoesNotExist:
            pass

        return context


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/salles/{salle_id}/schedules/{id}/ - Détails d'un créneau
    PUT    /api/salles/{salle_id}/schedules/{id}/ - Modifier un créneau
    DELETE /api/salles/{salle_id}/schedules/{id}/ - Supprimer un créneau
    """
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsGerant]
    lookup_field = 'id'

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        return Schedule.objects.filter(
            salle__id=salle_id,
            salle__gerant=gerant
        ).select_related('course')

    def get_serializer_context(self):
        """Passer la salle au serializer pour validation"""
        context = super().get_serializer_context()
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
            context['salle'] = salle
        except Salle.DoesNotExist:
            pass

        return context

# views.py (AJOUTE CES VIEWS)


# ============================================
# PHOTOS VIEWS (GENERICS VERSION)
# ============================================


class SallePhotosView(generics.ListCreateAPIView):
    """
    GET  /api/salles/{salle_id}/photos/ - Liste des photos
    POST /api/salles/{salle_id}/photos/ - Upload photo
    """
    serializer_class = SallePhotoSerializer
    permission_classes = [IsAuthenticated, IsGerant]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        # Vérifier que la salle appartient au gérant
        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        return SallePhoto.objects.filter(salle=salle)

    def perform_create(self, serializer):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        try:
            salle = Salle.objects.get(id=salle_id, gerant=gerant)
        except Salle.DoesNotExist:
            raise PermissionDenied("Vous n'avez pas accès à cette salle")

        serializer.save(salle=salle)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SallePhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/salles/{salle_id}/photos/{id}/ - Détails photo
    PATCH  /api/salles/{salle_id}/photos/{id}/ - Modifier (ordre, légende)
    DELETE /api/salles/{salle_id}/photos/{id}/ - Supprimer
    """
    serializer_class = SallePhotoSerializer
    permission_classes = [IsAuthenticated, IsGerant]
    parser_classes = [MultiPartParser, FormParser]

    # ✅ SOLUTION : Utiliser lookup_url_kwarg au lieu de lookup_field
    lookup_url_kwarg = 'id'  # ← Le nom du paramètre dans l'URL
    # ← Le champ dans le modèle (par défaut 'pk' = 'id')
    lookup_field = 'pk'

    def get_queryset(self):
        salle_id = self.kwargs.get('salle_id')
        gerant = self.request.user.gerant_profile

        return SallePhoto.objects.filter(
            salle__id=salle_id,
            salle__gerant=gerant
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# ============================================
# 1. API GÉOCODAGE D'ADRESSE
# ============================================

class GeocodeAddressView(generics.GenericAPIView):
    """
    POST /api/geocode/

    Convertit une adresse en coordonnées GPS

    Body: {
        "address": "12 Rue Didouche Mourad, Alger",
        "country": "Algeria"  // optionnel
    }
    """
    permission_classes = [AllowAny]
    serializer_class = GeocodeSerializer

    def post(self, request, *args, **kwargs):
        address = request.data.get('address')
        country = request.data.get('country', 'Algeria')

        if not address:
            return Response({
                'success': False,
                'error': 'Le champ "address" est requis'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Géocoder l'adresse
        result = GeocodingService.geocode_address(address, country)

        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)


# ============================================
# 2. API ITINÉRAIRE VERS UNE SALLE
# ============================================

class SalleDirectionsView(generics.RetrieveAPIView):
    """
    GET /api/salles/{salle_id}/directions/

    Retourne l'URL Google Maps pour l'itinéraire

    Query params:
        - mode: driving / walking / bicycling / transit (défaut: driving)
        - all_modes: true (retourne tous les modes)
    """
    queryset = Salle.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'salle_id'

    def retrieve(self, request, *args, **kwargs):
        # Récupérer la salle via le lookup automatique de Generic
        salle = self.get_object()

        # Vérifier les coordonnées
        if not salle.latitude or not salle.longitude:
            return Response({
                'error': 'Cette salle n\'a pas de coordonnées GPS'
            }, status=status.HTTP_404_NOT_FOUND)

        # Paramètres
        mode = request.query_params.get('mode', 'driving')
        all_modes = request.query_params.get(
            'all_modes', 'false').lower() == 'true'

        origin_lat = request.query_params.get('origin_lat')
        origin_lng = request.query_params.get('origin_lng')

        # Générer URLs
        if all_modes:
            urls = GeocodingService.get_multiple_transport_modes(
                float(salle.latitude),
                float(salle.longitude),
                salle.nom,
                origin_lat=origin_lat,
                origin_lng=origin_lng
            )

            return Response({
                'salle_id': salle.id,
                'salle_nom': salle.nom,
                'destination': {
                    'latitude': float(salle.latitude),
                    'longitude': float(salle.longitude)
                },
                'transport_modes': {
                    'driving': {
                        'label': 'En voiture',
                        'url': urls['driving']
                    },
                    'walking': {
                        'label': 'À pied',
                        'url': urls['walking']
                    },
                    'bicycling': {
                        'label': 'À vélo',
                        'url': urls['bicycling']
                    },
                    'transit': {
                        'label': 'Transports en commun',
                        'url': urls['transit']
                    }
                }
            }, status=status.HTTP_200_OK)

        else:
            google_maps_url = GeocodingService.get_google_maps_directions_url(
                float(salle.latitude),
                float(salle.longitude),
                salle.nom,
                origin_lat=origin_lat,
                origin_lng=origin_lng
            )

            return Response({
                'salle_id': salle.id,
                'salle_nom': salle.nom,
                'destination': {
                    'latitude': float(salle.latitude),
                    'longitude': float(salle.longitude)
                },
                'google_maps_url': google_maps_url,
                'transport_mode': mode
            }, status=status.HTTP_200_OK)


# ============================================
# 3. API RECHERCHE PAR PROXIMITÉ (si tu veux l'ajouter plus tard)
# ============================================

# ============================================
# 4. API HORAIRES D'OUVERTURE
# ============================================

class SalleHoraireView(APIView):
    """
    GET /api/salles/{salle_id}/horaires/ - Liste
    POST /api/salles/{salle_id}/horaires/ - Mise à jour globale
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_salle(self, salle_id):
        try:
            return Salle.objects.get(id=salle_id)
        except Salle.DoesNotExist:
            raise NotFound("Salle introuvable")

    def get(self, request, salle_id):
        salle = self.get_salle(salle_id)
        horaires = HoraireOuverture.objects.filter(
            salle=salle).order_by('id')  # ou jourSemaine si triable
        # Trier manuellement selon l'ordre des jours si nécessaire
        serializer = HoraireOuvertureSerializer(horaires, many=True)
        return Response(serializer.data)

    def put(self, request, salle_id):
        # Vérification permission gérant
        if not request.user.is_authenticated:
            raise PermissionDenied("Connexion requise")

        salle = self.get_salle(salle_id)

        # Vérifier que c'est le gérant
        if not hasattr(request.user, 'gerant_profile') or salle.gerant != request.user.gerant_profile:
            raise PermissionDenied("Vous n'êtes pas le gérant de cette salle")

        data = request.data  # Expecting list of objects
        if not isinstance(data, list):
            return Response({"error": "Une liste est attendue."}, status=status.HTTP_400_BAD_REQUEST)

        # Stratégie: Supprimer existants et recréer (plus simple pour mise à jour globale)
        HoraireOuverture.objects.filter(salle=salle).delete()

        created_horaires = []
        errors = []

        for item in data:
            # Inject salle
            # item['salle'] = salle.id  <-- Serializer expects ID, but we can save directly with model

            serializer = HoraireOuvertureSerializer(data=item)
            if serializer.is_valid():
                # Manually create to link salle instance
                horaire = HoraireOuverture.objects.create(
                    salle=salle,
                    **serializer.validated_data
                )
                created_horaires.append(horaire)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"message": "Certains horaires n'ont pas pu être créés", "errors": errors, "created_count": len(created_horaires)}, status=status.HTTP_207_MULTI_STATUS)

        # Return new list
        return Response(HoraireOuvertureSerializer(created_horaires, many=True).data, status=status.HTTP_200_OK)


class NearbySallesView(generics.ListAPIView):
    """
    GET /api/salles/nearby/

    Trouve les salles proches d'une position

    Query params:
        - latitude: latitude utilisateur (requis)
        - longitude: longitude utilisateur (requis)
        - radius: rayon en km (défaut: 10)
    """
    serializer_class = SalleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filtre les salles par distance
        Note: Pour l'instant, on retourne toutes les salles
        Tu implémenteras le filtre distance plus tard avec PostGIS
        """
        # Récupérer tous les paramètres
        user_lat = self.request.query_params.get('latitude')
        user_lng = self.request.query_params.get('longitude')
        radius = float(self.request.query_params.get('radius', 10))

        if not user_lat or not user_lng:
            return Salle.objects.none()

        # Pour l'instant, retourner toutes les salles avec coordonnées
        # Tu ajouteras le calcul de distance plus tard
        return Salle.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )

    def list(self, request, *args, **kwargs):
        """
        Override list pour ajouter des métadonnées
        """
        user_lat = request.query_params.get('latitude')
        user_lng = request.query_params.get('longitude')

        if not user_lat or not user_lng:
            return Response({
                'error': 'Les paramètres "latitude" et "longitude" sont requis'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': len(serializer.data),
            'user_location': {
                'latitude': float(user_lat),
                'longitude': float(user_lng)
            },
            'results': serializer.data
        }, status=status.HTTP_200_OK)


# ============================================
# 4. MODIFIER SalleViewSet (CRÉATION)
# ============================================

class SalleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet pour gérer les salles d'un gérant
    Utilise les Mixins de DRF pour plus de clarté
    """
    serializer_class = SalleSerializer
    permission_classes = [IsGerant]

    def get_queryset(self):
        """Retourne uniquement les salles du gérant connecté"""
        return Salle.objects.filter(gerant=self.request.user.gerant_profile)

    def perform_create(self, serializer):
        """
        Hook appelé avant la sauvegarde
        Parfait pour ajouter le gérant et géocoder
        """
        # Créer la salle
        salle = serializer.save(gerant=self.request.user.gerant_profile)

        # Géocodage automatique
        print(f"\n{'='*60}")
        print(f"🔍 Géocodage automatique pour: {salle.nom}")
        print(f"📍 Adresse: {salle.rue}, {salle.ville}, {salle.wilaya}")

        result = geocode_and_save_salle(salle)

        if result['success']:
            print(f"✅ SUCCÈS : {result['latitude']}, {result['longitude']}")
        else:
            print(f"❌ ÉCHEC : {result.get('error')}")
        print(f"{'='*60}\n")


# ============================================
# 5. MODIFIER DetailSalleViewSet (MODIFICATION)
# ============================================

class DetailSalleViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,  # Ajout du Retrieve pour GET
    generics.GenericAPIView
):
    """
    ViewSet pour modifier/supprimer/consulter une salle
    Utilise les Mixins pour plus de clarté
    """
    serializer_class = SalleSerializer
    permission_classes = [IsGerant]
    lookup_field = 'id'

    def get_queryset(self):
        """Retourne uniquement les salles du gérant connecté"""
        return Salle.objects.filter(gerant=self.request.user.gerant_profile)

    def get(self, request, *args, **kwargs):
        """GET /api/Detail-my-salle/{id}/ - Détails d'une salle"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """PUT /api/Detail-my-salle/{id}/ - Modifier une salle"""
        instance = self.get_object()

        # Sauvegarder l'ancienne adresse
        old_address = {
            'rue': instance.rue,
            'ville': instance.ville,
            'wilaya': instance.wilaya
        }

        # Mettre à jour avec le mixin
        response = self.update(request, *args, **kwargs)

        # Recharger l'instance
        instance.refresh_from_db()

        # Vérifier si l'adresse a changé
        address_changed = (
            instance.rue != old_address['rue'] or
            instance.ville != old_address['ville'] or
            instance.wilaya != old_address['wilaya']
        )

        # Re-géocoder si nécessaire
        if address_changed:
            print(f"\n🔄 Adresse modifiée, re-géocodage...")
            result = geocode_and_save_salle(instance)

            if result['success']:
                print(f"✅ Re-géocodage réussi")
            else:
                print(f"⚠️ Re-géocodage échoué: {result.get('error')}")

        return response

    def patch(self, request, *args, **kwargs):
        """PATCH /api/Detail-my-salle/{id}/ - Modifier partiellement"""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE /api/Detail-my-salle/{id}/ - Supprimer une salle"""
        return self.destroy(request, *args, **kwargs)

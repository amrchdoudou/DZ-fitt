# app/adapters.py
import sys
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class MyAccountAdapter(DefaultAccountAdapter):
    """Account adapter for regular authentication"""

    def _get_redirect_with_token(self, request, redirect_url):
        from rest_framework.authtoken.models import Token
        sys.stderr.write(f"\n[DIAGNOSTIC] _get_redirect_with_token called for {request.user}\n")
        if request.user.is_authenticated:
            token, _ = Token.objects.get_or_create(user=request.user)
            separator = '&' if '?' in redirect_url else '?'
            redirect_url = f"{redirect_url}{separator}token={token.key}"
            sys.stderr.write(f"[DIAGNOSTIC] Token generated and appended: {token.key[:10]}...\n")
        else:
            sys.stderr.write("[DIAGNOSTIC] User NOT authenticated in redirect helper!\n")
        return redirect_url

    def get_login_redirect_url(self, request):
        redirect_url = self._get_redirect_with_token(request, settings.LOGIN_REDIRECT_URL)
        print(f"🔄 MyAccountAdapter.get_login_redirect_url() → {redirect_url}")
        return redirect_url


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Social account adapter for OAuth"""

    def _get_redirect_with_token(self, request, redirect_url):
        from rest_framework.authtoken.models import Token
        if request.user.is_authenticated:
            token, _ = Token.objects.get_or_create(user=request.user)
            separator = '&' if '?' in redirect_url else '?'
            redirect_url = f"{redirect_url}{separator}token={token.key}"
        return redirect_url

    def get_login_redirect_url(self, request):
        redirect_url = self._get_redirect_with_token(request, settings.LOGIN_REDIRECT_URL)
        print("=" * 80)
        print("🔄 MySocialAccountAdapter.get_login_redirect_url() CALLED")
        print(f"🎯 REDIRECTING TO: {redirect_url}")
        print("=" * 80)
        return redirect_url

    def get_signup_redirect_url(self, request):
        redirect_url = self._get_redirect_with_token(request, settings.LOGIN_REDIRECT_URL)
        print(f"🔄 get_signup_redirect_url() → {redirect_url}")
        return redirect_url

    def get_connect_redirect_url(self, request, socialaccount):
        redirect_url = settings.LOGIN_REDIRECT_URL
        print(f"🔄 get_connect_redirect_url() → {redirect_url}")
        return redirect_url

    def pre_social_login(self, request, sociallogin):
        print(f"👤 pre_social_login: {sociallogin.account.extra_data.get('email', 'unknown')}")

        if sociallogin.is_existing:
            return

        if sociallogin.email_addresses:
            email = sociallogin.email_addresses[0].email
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                print(f"🔗 Connected: {email}")
            except User.DoesNotExist:
                print(f"➕ New user: {email}")

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # User is now activated via models.py Utilisateur.save() override
        
        if not getattr(user, 'type_utilisateur', None):
            user.type_utilisateur = 'client'
            
        # Populate name from social data if missing
        if not getattr(user, 'full_name', None):
            extra_data = sociallogin.account.extra_data
            user.full_name = extra_data.get('name') or f"{extra_data.get('given_name', '')} {extra_data.get('family_name', '')}".strip()
            
        user.save()
        print(f"✅ Social User {user.email} saved and activated.")
        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.type_utilisateur = 'client'
        # Also populate name during initial population
        extra_data = sociallogin.account.extra_data
        user.full_name = extra_data.get('name') or f"{extra_data.get('given_name', '')} {extra_data.get('family_name', '')}".strip()
        return user

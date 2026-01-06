from django.utils import timezone  # ✅ Ajouté
from django.core.mail import send_mail, EmailMultiAlternatives  # ✅ Ajouté
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.mail import send_mail
from django.conf import settings
import secrets
from cloudinary.models import CloudinaryField
# ===============================
# MANAGER USER
# ===============================


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Admin toujours actif
        extra_fields.setdefault('email_verified', True)  # Admin vérifié

        return self.create_user(email, password, **extra_fields)


# ===============================
# USER MODEL (MODIFIÉ)
# ===============================

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = [
        ('client', 'Client'),
        ('gerant', 'Gérant'),
    ]

    # ✅ CHANGEMENT : nom + prenom → full_name
    full_name = models.CharField(
        max_length=255, verbose_name="Nom complet", null=True, blank=True)
    email = models.EmailField(unique=True)
    type_utilisateur = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default='client', verbose_name="Type d'utilisateur")

    # ✅ NOUVEAU : Email vérifié ?
    email_verified = models.BooleanField(default=False)

    dateInscription = models.DateTimeField(auto_now_add=True)

    # ✅ IMPORTANT : is_active par défaut à True pour les clients (et Google Login)
    # On le mettra à False spécifiquement pour les gérants lors de l'inscription
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "type_utilisateur"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def save(self, *args, **kwargs):
        # ✅ Logique d'activation
        if self.type_utilisateur == 'gerant':
            if not self.pk: 
                 self.is_active = False
        else:
            # Pour les clients, on s'assure qu'ils sont toujours actifs
            self.is_active = True
            self.email_verified = True
        
        super().save(*args, **kwargs)


# ===============================
# CLIENT PROFILE
# ===============================

class Client(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="client_profile"
    )

    def __str__(self):
        return f"Client: {self.utilisateur.full_name}"


# ===============================
# GERANT PROFILE (SIMPLIFIÉ)
# ===============================

# models.py


# ... (gardez UtilisateurManager et Utilisateur inchangés) ...

# ===============================
# GERANT PROFILE (CORRIGÉ)
# ===============================


class Gerant(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente d\'approbation'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
    ]

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="gerant_profile"
    )

    nif = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="NIF (Numéro d'Identification Fiscale)",
        null=True,
        blank=True,
    )

    certificat_nif = models.FileField(
        upload_to='certificats_nif/',
        validators=[
            FileExtensionValidator(allowed_extensions=[
                                   'pdf', 'jpg', 'jpeg', 'png'])
        ],
        help_text="Téléchargez votre certificat NIF (PDF, JPG, PNG)",
        null=True,
        blank=True
    )

    statut_approbation = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    date_approbation = models.DateTimeField(null=True, blank=True)
    commentaire_admin = models.TextField(
        null=True,
        blank=True,
        help_text="Raison du rejet (si applicable)"
    )

    approval_token = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Gérant: {self.utilisateur.full_name} (NIF: {self.nif})"

    def generate_approval_token(self):
        """Génère un token sécurisé pour l'approbation"""
        self.approval_token = secrets.token_urlsafe(32)
        self.save()
        return self.approval_token

    def approuver(self, admin_user=None):
        """Approuve le gérant et active son compte"""
        print(f"🔄 Tentative d'approbation de {self.utilisateur.email}...")

        try:
            from django.utils import timezone

            self.statut_approbation = 'approuve'
            self.date_approbation = timezone.now()
            self.save()

            print(f"✅ Statut mis à jour: {self.statut_approbation}")

            # ✅ CORRECTION : Activer l'utilisateur, pas le gérant
            self.utilisateur.is_active = True
            self.utilisateur.save()

            print(f"✅ Compte activé pour {self.utilisateur.email}")

            send_mail(
                subject="✅ Votre compte gérant DZ-Fit a été approuvé !",
                message=f"""
Bonjour {self.utilisateur.full_name},

Bonne nouvelle ! Votre compte gérant (NIF: {self.nif}) a été approuvé par notre équipe.

Vous pouvez maintenant vous connecter et commencer à gérer vos salles de sport sur DZ-Fit.

🔗 Connectez-vous : {getattr(settings, 'FRONTEND_URL', 'https://dzfit.com')}/login

Bienvenue dans la communauté DZ-Fit !

Cordialement,
L'équipe DZ-Fit
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.utilisateur.email],
                fail_silently=False,
            )

            print(f"✅ Email d'approbation envoyé à {self.utilisateur.email}")
            return True

        except Exception as e:
            print(f"❌ ERREUR lors de l'approbation: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def rejeter(self, raison, admin_user=None):
        """Rejette la demande du gérant"""
        print(f"🔄 Tentative de rejet de {self.utilisateur.email}...")

        try:
            from django.utils import timezone

            self.statut_approbation = 'rejete'
            self.commentaire_admin = raison
            self.date_approbation = timezone.now()
            self.save()

            print(f"✅ Statut mis à jour: {self.statut_approbation}")

            contact_email = getattr(
                settings, 'CONTACT_EMAIL', 'contact@dzfit.com')

            send_mail(
                subject="❌ Votre demande de compte gérant DZ-Fit",
                message=f"""
Bonjour {self.utilisateur.full_name},

Nous avons examiné votre demande de compte gérant (NIF: {self.nif}).

Malheureusement, nous ne pouvons pas l'approuver pour la raison suivante :

{raison}

Si vous pensez qu'il s'agit d'une erreur, n'hésitez pas à nous contacter à {contact_email}.

Cordialement,
L'équipe DZ-Fit
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.utilisateur.email],
                fail_silently=False,
            )

            print(f"✅ Email de rejet envoyé à {self.utilisateur.email}")
            return True

        except Exception as e:
            print(f"❌ ERREUR lors du rejet: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    # ✅ CETTE MÉTHODE DOIT ÊTRE ICI, AVEC LA MÊME INDENTATION QUE LES AUTRES
    def send_admin_notification(self):
        """Envoie email à l'admin avec liens d'action"""
        print(f"📧 Envoi notification admin pour {self.utilisateur.email}...")

        try:
            from django.core.mail import EmailMultiAlternatives

            if not self.approval_token:
                self.generate_approval_token()
                print(f"✅ Token généré: {self.approval_token}")

            backend_url = getattr(settings, 'BACKEND_URL',
                                  'http://localhost:8000')
            approve_url = f"{backend_url}/api/admin/approve-gerant/{self.approval_token}/"
            reject_url = f"{backend_url}/api/admin/reject-gerant/{self.approval_token}/"

            print(f"🔗 URL d'approbation: {approve_url}")
            print(f"🔗 URL de rejet: {reject_url}")

            subject = f"🏋️ Nouvelle Demande de Compte Gérant"

            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial; background: #f5f5f5; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #2196f3; color: white; padding: 30px 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; }}
        .info-box {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-left: 4px solid #2196f3; }}
        .buttons {{ text-align: center; margin: 40px 0; }}
        .btn {{ display: inline-block; padding: 15px 40px; margin: 10px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        .btn-approve {{ background: #4caf50; color: white !important; }}
        .btn-reject {{ background: #f44336; color: white !important; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏋️ Nouvelle Demande de Compte Gérant</h1>
        </div>
        <div class="content">
            <p>Bonjour,</p>
            <p>Une nouvelle demande de compte gérant a été soumise sur <strong>DZ-Fit</strong>.</p>
            <div class="info-box">
                <p><strong>👤 Nom :</strong> {self.utilisateur.full_name}</p>
                <p><strong>📧 Email :</strong> {self.utilisateur.email}</p>
                <p><strong>📄 NIF :</strong> {self.nif}</p>
                <p><strong>📅 Date :</strong> {self.utilisateur.dateInscription.strftime('%d/%m/%Y à %H:%M')}</p>
            </div>
            <div class="buttons">
                <a href="{approve_url}" class="btn btn-approve">✅ APPROUVER</a>
                <a href="{reject_url}" class="btn btn-reject">❌ REJETER</a>
            </div>
        </div>
    </div>
</body>
</html>
            """

            text_message = f"""
Nouvelle demande de compte gérant - DZ-Fit

- Nom : {self.utilisateur.full_name}
- Email : {self.utilisateur.email}
- NIF : {self.nif}
- Date : {self.utilisateur.dateInscription.strftime('%d/%m/%Y à %H:%M')}

Approuver : {approve_url}
Rejeter : {reject_url}
            """

            admin_email = getattr(
                settings, 'ADMIN_NOTIFICATION_EMAIL', 'admin@dzfit.com')

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email]
            )

            email.attach_alternative(html_message, "text/html")

            if self.certificat_nif:
                try:
                    email.attach_file(self.certificat_nif.path)
                    print(f"✅ Certificat attaché")
                except Exception as e:
                    print(f"⚠️ Impossible d'attacher: {e}")

            email.send(fail_silently=False)
            print(f"✅ Email admin envoyé avec succès")
            return True

        except Exception as e:
            print(f"❌ ERREUR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


# ===============================
# VERIFICATION EMAIL (MODIFIÉ)
# ===============================

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    # ✅ NOUVEAU : Expiration après 15 minutes
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"{self.email} - {self.code}"


class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.token}"


# ===============================
# SALLE (INCHANGÉ)
# ===============================

class Salle(models.Model):
    gerant = models.ForeignKey(
        Gerant,
        on_delete=models.CASCADE,
        related_name="salles"
    )

    nom = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)

    rue = models.CharField(max_length=150)
    ville = models.CharField(max_length=100)
    wilaya = models.CharField(max_length=100)
    codePostal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100, default="Algérie")

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom


# ===============================
# HISTORIQUE RECHERCHE (INCHANGÉ)
# ===============================

class historiqueRecherche(models.Model):
    critresRecherche = models.JSONField()
    dateRecherche = models.DateTimeField(auto_now_add=True)
    nombreResultats = models.IntegerField()
    clientHistorique = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='historique')

    def __str__(self):
        return f"{self.clientHistorique} , {self.dateRecherche}"


# ===============================
# SERVICE (INCHANGÉ)
# ===============================


class Service(models.Model):
    SERVICE_CHOICES = [
        ('douchessssssSSSSSs', 'DouchesSSSSSSSSS'),
        ('douches', 'Douches'),
        ('wifi', 'Wifi'),
        ('climatisation', 'Climatisation'),
        ('parking', 'Parking'),
    ]

    nom = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_nom_display()


class SalleService(models.Model):
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="services"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="salles"
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('salle', 'service')
        verbose_name = "Service de salle"
        verbose_name_plural = "Services de salle"
        ordering = ['service__nom']

    def __str__(self):
        return f"{self.salle.nom} - {self.service}"


# ===============================
# AVIS (INCHANGÉ)
# ===============================

class Avis(models.Model):
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="avis"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="avis"
    )
    commentaire = models.TextField(null=True, blank=True)

    # Ratings
    note_proprete = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    note_equipement = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    note_personnel = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    note_rapport_qualite_prix = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    note_globale = models.FloatField(default=0)

    date_publication = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate overall rating
        notes = [self.note_proprete, self.note_equipement,
                 self.note_personnel, self.note_rapport_qualite_prix]
        self.note_globale = sum(notes) / len(notes) if len(notes) > 0 else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Avis de {self.client} pour {self.salle}"


class CritereNotation(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom

    def get_concern_equipments(self):
        return concerneEquipement.objects.filter(criter=self)

    def get_concerne_services(self):
        return concerneServices.objects.filter(criter=self)


class Concerne(models.Model):
    critere = models.ForeignKey(
        CritereNotation,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    note_etoile = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('critere', 'salle', 'client')


class concerneServices(models.Model):
    critere = models.ForeignKey(
        CritereNotation,
        on_delete=models.CASCADE,
        related_name="concernes_services"
    )
    Salleservices = models.ForeignKey(
        SalleService,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="concernes_servicess"
    )
    note_etoile = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('critere', 'Salleservices',
                           'client')  # <--- fix here

    def __str__(self):
        return f"{self.critere.nom} - {self.Salleservices.salle.nom} - {self.client.utilisateur.full_name} - {self.note_etoile}"


# ===============================
# EQUIPEMENT (INCHANGÉ)
# ===============================

class Equipement(models.Model):
    name = models.CharField(max_length=100)
    # icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SalleEquipement(models.Model):
    salle = models.ForeignKey(
        Salle, on_delete=models.CASCADE, related_name="salle_equipements")
    equipement = models.ForeignKey(
        Equipement, on_delete=models.CASCADE, related_name="equipement_salles")

    class Meta:
        unique_together = ('salle', 'equipement')  # prevent duplicates

    def __str__(self):
        return f"{self.salle.nom} - {self.equipement.name}"


class concerneEquipement(models.Model):
    critere = models.ForeignKey(
        CritereNotation,
        on_delete=models.CASCADE,
        related_name="concernes_equipements"
    )
    SalleEquipement = models.ForeignKey(
        SalleEquipement,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="concernes_equipements"
    )
    note_etoile = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('critere', 'SalleEquipement', 'client')

    def __str__(self):
        return f"{self.critere.nom} - {self.SalleEquipement.salle.nom} - {self.client.utilisateur.full_name} - {self.note_etoile}"


class Formule_Abonnement(models.Model):
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="formules_abonnement"
    )
    nom = models.CharField(max_length=100)
    number_science = models.IntegerField()
    prix_mensuel = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nom} - {self.salle.nom}"


# openning hours
JOUR_SEMAINE_CHOICES = (
    ('LUNDI', 'Lundi'),
    ('MARDI', 'Mardi'),
    ('MERCREDI', 'Mercredi'),
    ('JEUDI', 'Jeudi'),
    ('VENDREDI', 'Vendredi'),
    ('SAMEDI', 'Samedi'),
    ('DIMANCHE', 'Dimanche'),
)


class HoraireOuverture(models.Model):
    # Foreign Key to link to the Salle (the 'many' side of the relationship)
    salle = models.ForeignKey(
        'Salle',  # Use 'Salle' if both models are in the same file
        on_delete=models.CASCADE,
        related_name='horaires_ouverture'  # A useful related_name for reverse lookups
    )

    # Corresponds to jourSemaine: Enum(LUNDI, MARDI, ...)
    jourSemaine = models.CharField(
        max_length=10,
        choices=JOUR_SEMAINE_CHOICES,
        # It's good practice to ensure the day is unique per salle,
        # otherwise you'll need two records for the same day (e.g., if a place closes midday)
        # If the venue only has one opening time slot per day:
        # unique_together = ('salle', 'jourSemaine')
    )

    # Corresponds to heureOuverture: Time
    heureOuverture = models.TimeField()

    # Corresponds to heureFermeture: Time
    heureFermeture = models.TimeField()

    # Corresponds to estFerme: Boolean
    estFerme = models.BooleanField(default=False)

    class Meta:
        # Ensures that a salle cannot have two opening hour records for the same day
        # unless you specifically need to allow split hours (e.g., closed for lunch).
        # Based on your simple model, this is likely what you want.
        unique_together = ('salle', 'jourSemaine')
        verbose_name = "Horaire d'Ouverture"
        verbose_name_plural = "Horaires d'Ouverture"

    def __str__(self):
        return f"{self.salle.nom} - {self.get_jourSemaine_display()}: {self.heureOuverture.strftime('%H:%M')} - {self.heureFermeture.strftime('%H:%M')}"


class Course(models.Model):
    COURSE_CHOICES = [
        ('yoga', 'Yoga'),
        ('hiit_burn', 'HIIT Burn'),
        ('indoor_cycling', 'Indoor Cycling'),
        ('barbell_basics', 'Barbell Basics'),
        ('crossfit', 'CrossFit'),
        ('pilates', 'Pilates'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('all_levels', 'All Levels'),
    ]

    UNIT_CHOICES = [
        ('min', 'Minutes'),
        ('hour', 'Hours'),
    ]

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    name = models.CharField(max_length=50, choices=COURSE_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)]
    )
    duration_unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='min'
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('salle', 'name', 'level')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_name_display()} - {self.get_level_display()} ({self.salle.nom})"

    @property
    def duration_display(self):
        """Affiche la durée formatée: '2h' ou '45min'"""
        return f"{self.duration_value}{self.duration_unit}"

# Ajoute ça à la fin de models.py (après Course)


class ConcerneCourse(models.Model):
    critere = models.ForeignKey(
        CritereNotation,
        on_delete=models.CASCADE,
        related_name="concernes_courses"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="concernes"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="concernes_courses"
    )
    note_etoile = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('critere', 'course', 'client')

    def __str__(self):
        return f"{self.critere.nom} - {self.course.name} - {self.client.utilisateur.full_name} - {self.note_etoile}"


class Schedule(models.Model):
    DAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    room = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Éviter les conflits : même salle, même jour, même heure, même room
        unique_together = ('salle', 'day', 'start_time', 'room')
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.course.get_name_display()} - {self.get_day_display()} {self.start_time} ({self.salle.nom})"

    @property
    def duration(self):
        """Retourne la durée du cours associé"""
        return self.course.duration_display

# models.py (AJOUTE CE MODÈLE À LA FIN DU FICHIER)


class SallePhoto(models.Model):
    """
    Stocke les photos d'une salle (profil, couverture, galerie)
    """
    PHOTO_TYPE_CHOICES = [
        ('cover', 'Photo de couverture'),      # Bannière en haut
        ('profile', 'Photo de profil'),        # Logo/Avatar
        ('gallery', 'Galerie'),                # Toutes les autres photos
    ]

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,              # Si la salle est supprimée, ses photos aussi
        related_name='photos'                  # On pourra faire: salle.photos.all()
    )

    image = CloudinaryField('image', folder='salles/')

    photo_type = models.CharField(
        max_length=10,
        choices=PHOTO_TYPE_CHOICES,
        default='gallery'
    )

    ordre = models.PositiveIntegerField(
        default=0,
        help_text="Ordre d'affichage dans la galerie (0 = premier)"
    )

    legende = models.CharField(
        max_length=255,
        blank=True,
        help_text="Description de la photo (optionnel)"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', '-uploaded_at']   # Trier par ordre, puis date
        verbose_name = "Photo de salle"
        verbose_name_plural = "Photos de salles"

    def __str__(self):
        return f"{self.salle.nom} - {self.get_photo_type_display()}"

    def save(self, *args, **kwargs):
        """
        S'assurer qu'il n'y a qu'UNE SEULE photo de profil 
        et UNE SEULE photo de couverture par salle
        """
        if self.photo_type in ['cover', 'profile']:
            # Supprimer l'ancienne photo du même type avant d'enregistrer la nouvelle
            SallePhoto.objects.filter(
                salle=self.salle,
                photo_type=self.photo_type
            ).exclude(id=self.id).delete()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Supprimer le fichier image du disque quand on supprime l'objet
        """
        if self.image:
            self.image.delete(save=False)  # Supprimer le fichier physique
        super().delete(*args, **kwargs)

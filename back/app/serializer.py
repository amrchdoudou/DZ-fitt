from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings
import random
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg
from .models import (
    Utilisateur,
    Client,
    Gerant,
    VerificationCode,
    Salle,
    PasswordResetToken,
    historiqueRecherche,
    Service,
    SalleService,
    Avis,
    CritereNotation,
    Concerne,
    Equipement,
    SalleEquipement,
    Formule_Abonnement,
    concerneEquipement,
    concerneServices,
    Course,
    Schedule,
    SallePhoto,
    HoraireOuverture,ConcerneCourse,
)


# ===============================
# INSCRIPTION (MODIFIÉ)
# ===============================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    # Champs spécifiques au gérant
    nif = serializers.CharField(required=False)
    certificat_nif = serializers.FileField(required=False)

    class Meta:
        model = Utilisateur
        fields = [
            'full_name', 'email', 'password', 'type_utilisateur',
            'nif', 'certificat_nif'
        ]

    def validate(self, data):
        type_user = data.get('type_utilisateur')

        if type_user == 'gerant':
            if not data.get('nif'):
                raise serializers.ValidationError({
                    "nif": "Le NIF est obligatoire pour un gérant"
                })
            if not data.get('certificat_nif'):
                raise serializers.ValidationError({
                    "certificat_nif": "Le certificat NIF est obligatoire"
                })

        return data

    def create(self, validated_data):
        # Extraire les données
        password = validated_data.pop("password")
        type_user = validated_data.get("type_utilisateur")

        # Données gérant
        nif = validated_data.pop('nif', None)
        certificat_nif = validated_data.pop('certificat_nif', None)

        # Créer utilisateur INACTIF
        user = Utilisateur.objects.create_user(
            password=password,
            is_active=False,
            email_verified=False,
            **validated_data
        )

        # Générer code de vérification
        code = str(random.randint(1000, 9999))
        VerificationCode.objects.create(
            email=user.email,
            code=code
        )

        # Envoyer email de vérification au user
        send_mail(
            subject="🔐 Vérifiez votre email - DZ-Fit",
            message=f"""
Bonjour {user.full_name},

Bienvenue sur DZ-Fit !

Votre code de vérification est : {code}

Ce code est valable pendant 15 minutes.

Si vous n'avez pas créé de compte, ignorez cet email.

Cordialement,
L'équipe DZ-Fit
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        # Créer profils
        if type_user == "client":
            Client.objects.create(utilisateur=user)

        elif type_user == "gerant":
            # Créer le gérant SANS envoyer l'email admin
            gerant = Gerant.objects.create(
                utilisateur=user,
                nif=nif,
                certificat_nif=certificat_nif,
                statut_approbation='en_attente'
            )

            print("=" * 60)
            print("GERANT CREE (email admin sera envoye apres verification)")
            print(f"Gerant: {user.email}")
            print(f"NIF: {nif}")
            print("=" * 60)

        return user

# ===============================
# VÉRIFICATION EMAIL (MODIFIÉ)
# ===============================


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        code = data.get("code")

        # ✅ Vérifier si le code existe et n'est pas utilisé
        try:
            verification = VerificationCode.objects.get(
                email=email,
                code=code,
                is_used=False
            )
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Code de vérification invalide")

        # ✅ Vérifier si expiré
        if verification.is_expired():
            raise serializers.ValidationError("Ce code a expiré (15 min)")

        # ✅ Récupérer l'utilisateur
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable")

        data['user'] = user
        data['verification'] = verification
        return data


# ===============================
# UTILISATEUR (MODIFIÉ)
# ===============================

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'email', 'full_name',
            'type_utilisateur', 'dateInscription',
            'email_verified', 'is_active'
        ]
        read_only_fields = ['id', 'dateInscription',
                            'email_verified', 'is_active']


# ===============================
# CLIENT
# ===============================

class ClientSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'utilisateur']


# ===============================
# GERANT (MODIFIÉ)
# ===============================

class GerantSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    certificat_nif_url = serializers.SerializerMethodField()

    class Meta:
        model = Gerant
        fields = [
            'id', 'utilisateur', 'nif',
            'certificat_nif_url', 'statut_approbation',
            'date_approbation', 'commentaire_admin'
        ]
        read_only_fields = [
            'statut_approbation', 'date_approbation', 'commentaire_admin'
        ]

    def get_certificat_nif_url(self, obj):
        if obj.certificat_nif:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificat_nif.url)
        return None


class GerantUpdateFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["full_name"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mot de passe actuel incorrect")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas")

        validate_password(data["new_password"])
        return data
# ===============================
# LOGIN (MODIFIÉ)
# ===============================


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # ✅ Validate required fields
        if not email or not password:
            raise serializers.ValidationError(
                "Email and password are required")

        # ✅ Récupérer l'utilisateur manuellement pour éviter que authenticate() échoue si is_active=False
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # ✅ Vérifier le mot de passe manuellement
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        # ✅ Check if email is verified
        if not user.email_verified:
            raise serializers.ValidationError(
                "Please verify your email before logging in. Check your inbox."
            )

        # ✅ Check if account is active
        if not user.is_active:
            if user.type_utilisateur == 'gerant':
                try:
                    gerant = user.gerant_profile
                    if gerant.statut_approbation == 'en_attente':
                        raise serializers.ValidationError(
                            "Your gym owner account is pending approval. "
                            "You will receive an email once approved."
                        )
                    elif gerant.statut_approbation == 'rejete':
                        raise serializers.ValidationError(
                            f"Your request was rejected. Reason: {gerant.commentaire_admin}"
                        )
                except Gerant.DoesNotExist:
                    pass

            raise serializers.ValidationError("This account is deactivated")

        data['user'] = user
        return data
# ===============================
# RESTE INCHANGÉ
# ===============================


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Aucun compte associé à cet email")
        return value


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        if not PasswordResetToken.objects.filter(
            email=email,
            token=code,
            is_used=False,
            is_verified=False
        ).exists():
            raise serializers.ValidationError("Code invalide ou expiré")

        return data


class ResetPasswordSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas")

        if not PasswordResetToken.objects.filter(
            reset_token=data['reset_token'],
            is_used=False,
            is_verified=True
        ).exists():
            raise serializers.ValidationError("Token invalide ou expiré")

        return data


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = "__all__"
        read_only_fields = ["gerant"]


class historiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = historiqueRecherche
        fields = "__all__"
        read_only_fields = ["clientHistorique", "dateRecherche"]


class ServiceSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='get_nom_display', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'nom', 'label']


class SalleServiceSerializer(serializers.ModelSerializer):
    service_info = ServiceSerializer(source='service', read_only=True)

    class Meta:
        model = SalleService
        fields = ['id', 'service', 'service_info', 'date_ajout']
        read_only_fields = ['date_ajout']


class SalleServiceBulkSerializer(serializers.Serializer):
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Liste des IDs de services à activer"
    )

    def validate_service_ids(self, value):
        # Vérifier que tous les IDs existent
        existing_ids = Service.objects.filter(
            id__in=value).values_list('id', flat=True)
        existing_ids = Service.objects.filter(
            id__in=value).values_list('id', flat=True)
        invalid_ids = set(value) - set(existing_ids)

        if invalid_ids:
            raise serializers.ValidationError(
                f"Services invalides : {invalid_ids}"
            )

        return value


class SalleWithServicesSerializer(serializers.ModelSerializer):
    services = SalleServiceSerializer(many=True, read_only=True)
    nombre_services = serializers.SerializerMethodField()

    class Meta:
        model = Salle
        fields = '__all__'

    def get_nombre_services(self, obj):
        return obj.services.count()


class AvisSerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()

    class Meta:
        model = Avis
        fields = [
            'id', 'salle', 'client', 'commentaire', 
            'note_proprete', 'note_equipement', 'note_personnel', 
            'note_rapport_qualite_prix', 'note_globale',
            'date_publication', 'utilisateur'
        ]
        read_only_fields = ["client", "salle", "date_publication", "note_globale", "utilisateur"]

    def get_utilisateur(self, obj):
        return {
            "nom_complet": obj.client.utilisateur.full_name,
            "email": obj.client.utilisateur.email
        }


class criterNotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CritereNotation
        fields = "__all__"


class concernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concerne
        fields = "__all__"


class ConcerneServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = concerneServices
        fields = "__all__"


class concernEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = concerneEquipement
        fields = "__all__"


class ConcerneCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcerneCourse
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = "__all__"


class SalleEquipementSerializer(serializers.ModelSerializer):
    equipement_id = serializers.SerializerMethodField()  # Read-only ID
    equipement_write = serializers.PrimaryKeyRelatedField(
        queryset=Equipement.objects.all(),
        source='equipement',
        write_only=True,
        required=False
    )
    equipement = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SalleEquipement
        fields = ['id', 'equipement', 'equipement_id', 'equipement_write']

    def get_equipement_id(self, obj):
        """Retourne l'ID de l'équipement en lecture seule"""
        return obj.equipement.id if obj.equipement else None


class filterSalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = "__all__"


class FormuleAbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formule_Abonnement
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    duration_display = serializers.ReadOnlyField()
    name_display = serializers.CharField(
        source='get_name_display', read_only=True)
    level_display = serializers.CharField(
        source='get_level_display', read_only=True)
    unit_display = serializers.CharField(
        source='get_duration_unit_display', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'name_display',
            'level', 'level_display',
            'duration_value', 'duration_unit', 'unit_display', 'duration_display',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Vérifie qu'on ne crée pas un doublon"""
        salle = self.context['salle']
        name = data.get('name')
        level = data.get('level')

        # Si on est en UPDATE, exclure l'objet actuel
        if self.instance:
            existing = Course.objects.filter(
                salle=salle,
                name=name,
                level=level
            ).exclude(id=self.instance.id)
        else:
            existing = Course.objects.filter(
                salle=salle,
                name=name,
                level=level
            )

        if existing.exists():
            raise serializers.ValidationError(
                f"Un cours {data.get('name')} de niveau {data.get('level')} existe déjà pour cette salle"
            )

        return data


class ScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(
        source='get_day_display', read_only=True)
    duration = serializers.ReadOnlyField()

    # Infos du cours (en lecture seule)
    course_name = serializers.CharField(
        source='course.get_name_display', read_only=True)
    course_level = serializers.CharField(
        source='course.get_level_display', read_only=True)

    start_time = serializers.TimeField()
    end_time = serializers.TimeField(required=False, allow_null=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'course', 'course_name', 'course_level',
            'day', 'day_display', 'start_time', 'end_time',
            'room', 'coach', 'duration',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validations personnalisées"""
        salle = self.context.get('salle')
        course = data.get('course')
        day = data.get('day')
        start_time = data.get('start_time')
        room = data.get('room')

        # Vérifier que le cours appartient à la même salle
        if course and course.salle != salle:
            raise serializers.ValidationError({
                "course": "Ce cours n'appartient pas à cette salle"
            })

        # Vérifier les conflits de créneaux (même jour, même heure, même salle)
        if self.instance:
            # Mode UPDATE : exclure l'objet actuel
            existing = Schedule.objects.filter(
                salle=salle,
                day=day,
                start_time=start_time,
                room=room
            ).exclude(id=self.instance.id)
        else:
            # Mode CREATE
            existing = Schedule.objects.filter(
                salle=salle,
                day=day,
                start_time=start_time,
                room=room
            )

        if existing.exists():
            raise serializers.ValidationError(
                f"Un créneau existe déjà le {day} à {start_time} dans {room}"
            )

        return data

# serializers.py (AJOUTE CES SERIALIZERS)


class SallePhotoSerializer(serializers.ModelSerializer):
    """
    Serializer pour une photo individuelle
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SallePhoto
        fields = [
            'id',
            'image',           # Le fichier uploadé
            'image_url',       # L'URL complète pour afficher l'image
            'photo_type',      # cover / profile / gallery
            'ordre',           # Position dans la galerie
            'legende',         # Description
            'uploaded_at'      # Date d'upload
        ]
        # ✅ CORRECTION : Retirez 'ordre' et 'legende' de read_only_fields
        read_only_fields = ['id', 'uploaded_at', 'image_url']

    def get_image_url(self, obj):
        """
        Retourne l'URL complète de l'image
        """
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_image(self, value):
        """
        Vérifier que l'image n'est pas trop grosse (max 5MB)
        """
        max_size = 5 * 1024 * 1024  # 5MB en bytes
        if value.size > max_size:
            raise serializers.ValidationError(
                f"L'image est trop grosse ({value.size / 1024 / 1024:.1f}MB). Maximum: 5MB"
            )
        return value


class SalleWithPhotosSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher une salle AVEC toutes ses photos organisées
    """
    photo_profil = serializers.SerializerMethodField()
    photo_cover = serializers.SerializerMethodField()
    galerie = serializers.SerializerMethodField()

    class Meta:
        model = Salle
        fields = '__all__'  # Tous les champs de Salle + les 3 nouveaux

    def get_photo_profil(self, obj):
        """Retourne l'URL de la photo de profil"""
        photo = obj.photos.filter(photo_type='profile').first()
        if photo:
            request = self.context.get('request')
            return request.build_absolute_uri(photo.image.url) if request else None
        return None

    def get_photo_cover(self, obj):
        """Retourne l'URL de la photo de couverture"""
        photo = obj.photos.filter(photo_type='cover').first()
        if photo:
            request = self.context.get('request')
            return request.build_absolute_uri(photo.image.url) if request else None
        return None

    def get_galerie(self, obj):
        """Retourne toutes les photos de la galerie"""
        photos = obj.photos.filter(photo_type='gallery')
        return SallePhotoSerializer(photos, many=True, context=self.context).data


class GeocodeSerializer(serializers.Serializer):
    """
    Serializer simple pour valider les données d'entrée
    de l'API /api/geocode/
    """
    address = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="Adresse à géocoder"
    )
    country = serializers.CharField(
        required=False,
        default="Algeria",
        help_text="Pays (optionnel, par défaut Algérie)"
    )


class HoraireOuvertureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoraireOuverture
        fields = ['id', 'jourSemaine', 'heureOuverture',
                  'heureFermeture', 'estFerme']
        read_only_fields = ['id']


class SalleSearchSerializer(serializers.ModelSerializer):
    """
    Serializer optimized for search results
    """
    logo = serializers.SerializerMethodField()
    note_moyenne = serializers.FloatField(read_only=True)
    distance = serializers.SerializerMethodField()
    prix_moyen = serializers.SerializerMethodField()

    class Meta:
        model = Salle
        fields = [
            'id', 'nom', 'description', 'latitude', 'longitude',
            'logo', 'note_moyenne', 'distance', 'prix_moyen'
        ]

    def get_distance(self, obj):
        if not hasattr(obj, 'distance') or obj.distance is None:
            return None
        
        # Handle PostGIS Distance object which has .km attribute
        if hasattr(obj.distance, 'km'):
            return round(obj.distance.km, 2)
        
        # Handle float/decimal (fallback or previous calculation)
        try:
            return round(float(obj.distance), 2)
        except (ValueError, TypeError):
            return None

    def get_logo(self, obj):
        photo = obj.photos.filter(photo_type='profile').first()
        if photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(photo.image.url)
            return photo.image.url
        return None

    def get_prix_moyen(self, obj):
        # Calculate average price from formulas
        avg = obj.formules_abonnement.aggregate(Avg('prix_mensuel'))['prix_mensuel__avg']
        if avg:
            return f"{int(avg)} DZD"
        return "Non spécifié"


# ===============================
# PUBLIC GYM DETAIL SERIALIZER
# ===============================

class SallePublicDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for public gym detail view with all nested data
    """
    # Services
    services = serializers.SerializerMethodField()
    
    # Equipment
    equipes = serializers.SerializerMethodField()
    
    # Working hours
    horaires = serializers.SerializerMethodField()
    
    # Photos
    logo = serializers.SerializerMethodField()
    photo_couverture = serializers.SerializerMethodField()
    photos_galerie = serializers.SerializerMethodField()
    
    # Reviews/Ratings
    avis = serializers.SerializerMethodField()
    note_moyenne = serializers.SerializerMethodField()
    
    # Courses
    courses = serializers.SerializerMethodField()
    
    # Schedules
    schedules = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Salle
        fields = [
            'id', 'nom', 'description', 'rue', 'ville', 'wilaya', 'codePostal', 'pays',
            'latitude', 'longitude', 'telephone',
            'services', 'equipes', 'horaires',
            'logo', 'photo_couverture', 'photos_galerie',
            'avis', 'note_moyenne', 'courses', 'schedules',
            'views_count'
        ]
    
    def get_services(self, obj):
        """Get all services for this gym"""
        services = obj.services.select_related('service').all()
        return [{'id': s.service.id, 'service_nom': s.service.get_nom_display()} for s in services]
    
    def get_equipes(self, obj):
        """Get all equipment for this gym"""
        equipments = obj.salle_equipements.select_related('equipement').all()
        return [{'id': e.equipement.id, 'equipement_nom': str(e.equipement)} for e in equipments]
    
    def get_horaires(self, obj):
        """Get working hours"""
        hours = obj.horaires_ouverture.all()
        return [{
            'jour': h.jourSemaine,
            'heure_ouverture': h.heureOuverture.strftime('%H:%M') if h.heureOuverture else None,
            'heure_fermeture': h.heureFermeture.strftime('%H:%M') if h.heureFermeture else None,
            'est_ferme': h.estFerme
        } for h in hours]
    
    def get_logo(self, obj):
        """Get profile photo URL"""
        photo = obj.photos.filter(photo_type='profile').first()
        if photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(photo.image.url)
            return photo.image.url
        return None
    
    def get_photo_couverture(self, obj):
        """Get cover photo URL"""
        photo = obj.photos.filter(photo_type='cover').first()
        if photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(photo.image.url)
            return photo.image.url
        return None
    
    def get_photos_galerie(self, obj):
        """Get all gallery photos"""
        photos = obj.photos.filter(photo_type='gallery').order_by('ordre')
        request = self.context.get('request')
        return [{
            'id': p.id,
            'image': request.build_absolute_uri(p.image.url) if request else p.image.url,
            'legende': p.legende
        } for p in photos]
    
    def get_avis(self, obj):
        """Get all reviews"""
        reviews = obj.avis.select_related('client__utilisateur').all()
        return [{
            'id': a.id,
            'utilisateur': a.client.utilisateur.full_name,
            'commentaire': a.commentaire,
            'note_proprete': a.note_proprete,
            'note_equipement': a.note_equipement,
            'note_personnel': a.note_personnel,
            'note_rapport_qualite_prix': a.note_rapport_qualite_prix,
            'note_globale': a.note_globale,
            'date_publication': a.date_publication
        } for a in reviews]
    
    def get_note_moyenne(self, obj):
        """Calculate average rating"""
        avg = obj.avis.aggregate(Avg('note_globale'))['note_globale__avg']
        return round(avg, 1) if avg else None
    
    def get_courses(self, obj):
        """Get all courses"""
        courses = obj.courses.all()
        return [{
            'id': c.id,
            'nom': c.get_name_display(),
            'level': c.get_level_display(),
            'description': c.description,
            'duration': c.duration_display
        } for c in courses]
    
    def get_schedules(self, obj):
        """Get all schedules"""
        schedules = obj.schedules.select_related('course').all()
        return [{
            'id': s.id,
            'day_of_week': s.day,
            'start_time': s.start_time.strftime('%H:%M') if s.start_time else None,
            'end_time': s.end_time.strftime('%H:%M') if s.end_time else None,
            'course_name': s.course.get_name_display() if s.course else None,
            'room': s.room,
            'instructor_name': s.coach
        } for s in schedules]


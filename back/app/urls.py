from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    # Auth
    GeocodeAddressView, RegisterView, SalleDirectionsView, VerifyEmailView, ResendVerificationCodeView,
    LoginView, LogoutView,
    ForgotPasswordView, VerifyResetCodeView, ResetPasswordView,

    # Salle
    SalleViewSet, AllSalleViewSet, DetailSalleViewSet,
    SalleDetailPublicView,

    # Services
    ServiceListView, SalleServiceView,
    SalleServiceAddView, SalleServiceDeleteView,

    # Historique & Avis
    HistoriqueRechercheView, historiqueRechercheDetail,
    AvisView, FilterSalleViewSet,

    # Equipements
    EquipementViewset,
    allEquipementViewset,
    EquipementGerantViewset, GerantUpdateFullNameView, GerantChangePasswordView,

    # Formules Abonnement
    FormuleAbonnementGerantViewSet,
    FormuleAbonnementDetailViewSet,

    # Concern & Critères
    CriterNotationViewSet,
    CritereConcernsViewSet, SalleConcernsView, AddConcernView,

    # Admin actions
    approve_gerant_by_token, reject_gerant_by_token,

    CourseListCreateView,
    CourseDetailView,

    ScheduleListCreateView,
    ScheduleDetailView,

    SallePhotosView,
    SallePhotoDetailView,
    NearbySallesView,
    SalleHoraireView,
    FilterOptionsView,
    UnifiedSalleSearchView, SPARegisterView, GoogleLogin, get_authenticated_user,custom_google_login,
)

# Router pour les ViewSets
router = DefaultRouter()
router.register("my-salles", SalleViewSet, basename="my-salles")
router.register("all-salle", AllSalleViewSet, basename="all-salle")

urlpatterns = [
    path("", include(router.urls)),

    # ============================================
    # OAUTH & AUTHENTICATION API
    # ============================================
    path('auth/registration/', SPARegisterView.as_view(), name='rest_register'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    # ✅ FIXED: Removed 'api/'
    path('user/', get_authenticated_user, name='get_user'),
    path('google-auth/', custom_google_login, name='custom_google_login'),

    # ============================================
    # AUTHENTICATION
    # ============================================
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-code/',
         ResendVerificationCodeView.as_view(), name='resend-code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ============================================
    # PASSWORD RESET
    # ============================================
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(),
         name='verify-reset-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    # ============================================
    # ADMIN ACTIONS
    # ============================================
    path('admin/approve-gerant/<str:token>/',
         approve_gerant_by_token, name='approve-gerant'),
    path('admin/reject-gerant/<str:token>/',
         reject_gerant_by_token, name='reject-gerant'),

    # ============================================
    # SALLES
    # ============================================
    path("Detail-my-salle/<int:id>/",
         DetailSalleViewSet.as_view(), name="Detail-my-salle"),
    path('salles/<int:id>/', SalleDetailPublicView.as_view(),
         name='salle-detail-public'),

    # ============================================
    # SERVICES
    # ============================================
    path('services/', ServiceListView.as_view(), name='services-list'),
    path('salles/<int:salle_id>/services/',
         SalleServiceView.as_view(), name='salle-services'),
    path('salles/<int:salle_id>/services/add/',
         SalleServiceAddView.as_view(), name='salle-services-add'),
    path('salles/<int:salle_id>/services/<int:service_id>/',
         SalleServiceDeleteView.as_view(), name='salle-services-delete'),

    # ============================================
    # EQUIPMENTS
    # ============================================
    path('equipment/', allEquipementViewset.as_view(), name='eqiupes-list'),
    path('salles/<int:salle_id>/equipe/',
         EquipementViewset.as_view(), name='salle-equipes'),
    path('salles/<int:salle_id>/equipe/add/',
         EquipementGerantViewset.as_view(), name='salle-equipe-add'),
    path(
        'salles/<int:salle_id>/equipe/<int:equipement_id>/delete/',
        EquipementGerantViewset.as_view(),
        name='salle-equipe-delete'
    ),

    # ============================================
    # COURSES
    # ============================================
    path('salles/<int:salle_id>/courses/',
         CourseListCreateView.as_view(),
         name='course-list-create'),
    path('salles/<int:salle_id>/courses/<int:id>/',
         CourseDetailView.as_view(),
         name='course-detail'),

    # ============================================
    # FORMULES ABONNEMENT
    # ============================================
    path("salles/<int:salle_id>/formules/",
         FormuleAbonnementGerantViewSet.as_view()),
    path("salles/<int:salle_id>/formules/<int:pk>/",
         FormuleAbonnementDetailViewSet.as_view()),

    # ============================================
    # CRITERES & CONCERNS
    # ============================================
    path("salles/<int:salle_id>/criter/<int:id>/",
         CriterNotationViewSet.as_view()),
    path("salles/<int:salle_id>/criter/",
         CriterNotationViewSet.as_view()),
    path('salles/<int:salle_id>/concern/add/',
         AddConcernView.as_view(), name='add-concern'),
    path('salles/<int:salle_id>/concerns/all/',
         SalleConcernsView.as_view(), name='salle-all-concerns'),
    path(
        'salles/<int:salle_id>/criter/<int:criter_id>/concerns/',
        CritereConcernsViewSet.as_view(),
        name='criter-concerns'
    ),

    # ============================================
    # GERANT PROFILE
    # ============================================
    path(
        "gerant/update-full-name/",
        GerantUpdateFullNameView.as_view(),
        name="gerant-update-full-name"
    ),
    path(
        "gerant/change-password/",
        GerantChangePasswordView.as_view(),
        name="gerant-change-password"
    ),

    # ============================================
    # SCHEDULES
    # ============================================
    path('salles/<int:salle_id>/schedules/',
         ScheduleListCreateView.as_view(),
         name='schedule-list-create'),
    path('salles/<int:salle_id>/schedules/<int:id>/',
         ScheduleDetailView.as_view(),
         name='schedule-detail'),

    # ============================================
    # PHOTOS
    # ============================================
    path('salles/<int:salle_id>/photos/',
         SallePhotosView.as_view(),
         name='salle-photos'),
    path('salles/<int:salle_id>/photos/<int:id>/',
         SallePhotoDetailView.as_view(),
         name='salle-photo-detail'),

    # ============================================
    # GEOCODING & DIRECTIONS
    # ============================================
    path('geocode/',
         GeocodeAddressView.as_view(),
         name='geocode'),
    path('salles/<int:salle_id>/directions/',
         SalleDirectionsView.as_view(),
         name='salle-directions'),

    # ============================================
    # HORAIRES & NEARBY
    # ============================================
    path('salles/<int:salle_id>/horaires/',
         SalleHoraireView.as_view(),
         name='salle-horaires'),
    path('salles/nearby/',
         NearbySallesView.as_view(),
         name='salles-nearby'),

    # ============================================
    # FILTER & SEARCH
    # ============================================
    path('salles/filter/', FilterSalleViewSet.as_view(), name='salle-filter'),
    path('filters/', FilterOptionsView.as_view(), name='filter-options'),
    path('salles/search/', UnifiedSalleSearchView.as_view(), name='salle-search'),

    # ============================================
    # AVIS (REVIEWS)
    # ============================================
    path('salles/<int:salle_id>/avis/', AvisView.as_view(), name='salle-avis'),
    path('salles/<int:salle_id>/avis/<int:avis_id>/',
         AvisView.as_view(), name='salle-avis-detail'),
]

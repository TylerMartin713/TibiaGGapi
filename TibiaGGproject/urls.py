from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from TibiaGGapi.views import (
    register_user,
    login_user,
    get_current_user,
)
from TibiaGGapi.views.huntingplace import HuntingPlaceViewSet
from TibiaGGapi.views.location import LocationViewSet
from TibiaGGapi.views.vocation import VocationViewSet
from TibiaGGapi.views.character import CharacterViewSet
from TibiaGGapi.views.creature import CreatureViewSet
from TibiaGGapi.views.imbue import ImbueViewSet
from TibiaGGapi.views.item import ItemViewSet
from TibiaGGapi.views.favorite import FavoriteViewSet
from TibiaGGapi.views.tibiadata import get_character_info, get_creature_info


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"hunting-places", HuntingPlaceViewSet, basename="hunting-place")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"vocations", VocationViewSet, basename="vocation")
router.register(r"characters", CharacterViewSet, basename="character")
router.register(r"creatures", CreatureViewSet, basename="creature")
router.register(r"imbues", ImbueViewSet, basename="imbue")
router.register(r"items", ItemViewSet, basename="item")
router.register(r"favorites", FavoriteViewSet, basename="favorite")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("current_user", get_current_user),
    path("api/character/<str:name>/", get_character_info),
    path("api/creature/<str:name>/", get_creature_info),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

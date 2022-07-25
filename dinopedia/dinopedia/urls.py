"""dinopedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dinosaurs.views import DinosaurViewSet, PetDinosaurViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
# # drf_yasg
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
# from dinosaurs import views

admin.site.site_header = "Dinosaurs Index"
admin.site.site_title = admin.site.site_header

router = routers.DefaultRouter(trailing_slash=False)

router.register("dinosaurs", DinosaurViewSet, "dinosaurs")
router.register("petdinosaurs", PetDinosaurViewSet, "petdinosaurs")


urlpatterns = [
    # path("dinosaurs/", include("dinosaurs.urls")),
    path("api/", include(router.urls)),


    path(
        "api/dinosaurs/<pk>/images1",
        DinosaurViewSet.as_view({"patch": "retrieve"}),
        name="dinosaur-related",
    ),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# drf_yasg api documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Dinopedia API",
        default_version="v1",
        description="API for the Dinosaurs Index app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nick.ioannou86@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

drf_yasg_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
urlpatterns += drf_yasg_urlpatterns

from rest_framework import decorators, parsers, response, status, viewsets

from dinosaurs.models import Dinosaur
from dinosaurs.serializers import (
    DinosaurSerializer,
    DinosaurImage1Serializer,
    DinosaurImage2Serializer,
)

# from rest_framework.filters import OrderingFilter
# from django_filters import rest_framework as filters


class FilterOperators:
    """
    Definitions of the Field lookups, see:
    https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups
    """

    usual_rels = (
        "exact",
        "lt",
        "gt",
        "gte",
        "lte",
        "in",
    )
    text_rels = ("icontains", "iexact", "contains")


class DinosaurViewSet(viewsets.ModelViewSet):
    """
    API endpoint Dinosaur.
    """

    queryset = Dinosaur.objects.all()
    serializer_class = DinosaurSerializer

    # if you want just for this class remove DEFAULT_FILTER_BACKENDS from the settings
    # and add it here
    # filter_backends = (
    #     # filters.DjangoFilterBackend,
    #     OrderingFilter,
    # )
    #

    filterset_fields = {
        "name": ("exact",) + FilterOperators.text_rels,
        #
        "period__name": ("exact",) + FilterOperators.text_rels,
        "period__start_year": FilterOperators.usual_rels,
        "period__end_year": FilterOperators.usual_rels,
        # more with length, width
        "size__size": ("exact",) + FilterOperators.text_rels,
        "size__height_min": FilterOperators.usual_rels,
        "size__height_max": FilterOperators.usual_rels,
        "size__weight_min": FilterOperators.usual_rels,
        "size__weight_max": FilterOperators.usual_rels,
        #
        "eating_type__eating_type": ("exact",) + FilterOperators.text_rels,
        #
        "description": ("exact",) + FilterOperators.text_rels,
    }
    # ordering: add in the url ?ordering=<field> is ascenging (with -field is descending)
    ordering_fields = [
        "name",
        "size",
        "size__height_min",
        "size__height_max",
        "size__weight_min",
        "size__weight_max",
        "period__start_year",
        "period__end_year",
    ]

    @decorators.action(
        detail=True,
        methods=[" GET, PATCH"],
        serializer_class=DinosaurImage1Serializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def image1(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(
            obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        detail=True,
        methods=["GET, PATCH"],
        serializer_class=DinosaurImage2Serializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def density_heat_map(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(
            obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

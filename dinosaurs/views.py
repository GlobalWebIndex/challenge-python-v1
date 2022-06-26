from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Dinosaur


class DinosaurListView(generic.ListView):
    model = Dinosaur
    paginate_by = 12


class DinosaurDetailView(generic.DetailView):
    model = Dinosaur


class SearchResultsView(generic.ListView):
    model = Dinosaur
    template_name = 'dinosaurs/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Dinosaur.objects.filter(name__icontains=query)


class DinosaurCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Dinosaur
    fields = ['name', 'eating_classification', 'colour', 'period', 'size', 'image_1', 'image_2']
    permission_required = 'dinosaurs.can_edit'


class DinosaurUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Dinosaur
    template_name = 'dinosaurs/dinosaur_form_update.html'
    fields = ['name', 'eating_classification', 'colour', 'period', 'size', 'image_1', 'image_2']
    permission_required = 'dinosaurs.can_edit'


class DinosaurDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Dinosaur
    success_url = reverse_lazy('dinosaur')
    permission_required = 'dinosaurs.can_edit'


def add_favorites(request, dinosaur_id):
    dinosaur = get_object_or_404(Dinosaur, id=dinosaur_id)
    dinosaur.favorites.add(request.user)
    return redirect('favorite-dinosaurs')


class FavoritesDinosaurListView(generic.ListView):
    model = Dinosaur
    paginate_by = 12
    template_name = 'dinosaurs/dinosaur_favorites.html'

    def get_queryset(self):
        user = self.request.user
        return Dinosaur.objects.filter(favorites__username__exact=user)

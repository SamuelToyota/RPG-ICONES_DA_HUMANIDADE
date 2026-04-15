from django.shortcuts import render, get_object_or_404, redirect
from .models import Character
from .forms import CharacterForm


def HomeView(request):
    return render(request, 'core/home.html')


def CharacterListView(request):
    characters = Character.objects.all()
    return render(request, 'core/character_list.html', {'characters': characters})


def CharacterDetailView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'core/character_detail.html', {'character': character})


def CharacterCreateView(request):
    if request.method == "POST":
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('character_list')
    else:
        form = CharacterForm()

    return render(request, 'core/character_form.html', {
        'form': form,
        'edit_mode': False
    })


def CharacterUpdateView(request, pk):
    character = get_object_or_404(Character, pk=pk)

    if request.method == "POST":
        form = CharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            return redirect('character_detail', pk=character.pk)
    else:
        form = CharacterForm(instance=character)

    return render(request, 'core/character_form.html', {
        'form': form,
        'character': character,
        'edit_mode': True
    })


def CharacterDeleteView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    character.delete()
    return redirect('character_list')


def LivroRegrasView(request):
    return render(request, 'core/livro_regras.html')
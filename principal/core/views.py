from django.shortcuts import render, get_object_or_404, redirect
from .models import Character
from .forms import CharacterForm

# Lista todos os personagens na Home
def HomeView(request):
    characters = Character.objects.all()
    return render(request, 'core/home.html', {'characters': characters})

# Exibe os detalhes de um personagem específico
def CharacterDetailView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'core/character_detail.html', {'character': character})

# Cria um novo personagem (com suporte a foto)
def CharacterCreateView(request):
    if request.method == "POST":
        # request.POST pega os textos, request.FILES pega a imagem
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CharacterForm()
    return render(request, 'core/character_form.html', {'form': form, 'edit_mode': False})

# Edita um personagem existente (com suporte a foto)
def CharacterUpdateView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if request.method == "POST":
        # instance=character garante que estamos editando o herói certo e não criando um novo
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
    return redirect('home')
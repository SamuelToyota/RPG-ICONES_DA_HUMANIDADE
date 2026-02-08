from django import forms
from .models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        # Lista atualizada: removemos 'anotacoes' e não incluímos 'trilha'
        # (pois a trilha é automática no model)
        fields = [
            'nome_do_heroi',
            'nome_do_jogador',
            'foto',
            'classe',
            'origem',
            'arma',
            'nivel',
            'vida',
            'esforco',
            'defesa_esquiva',
            'forca',
            'agilidade',
            'inteligencia',
            'resistencia',
            'carisma',
            'momentum',
            'pericias',
            'habilidades',
        ]
        widgets = {
            'pericias': forms.CheckboxSelectMultiple(),
            'habilidades': forms.CheckboxSelectMultiple(),
            # Input de foto otimizado para o design do seu template
            'foto': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicando classes CSS automaticamente para manter o visual Cyberpunk
        for field_name, field in self.fields.items():
            # Checkboxes ganham uma classe de grupo para não quebrarem o layout
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'cyber-checkbox-group'})
            # Inputs de arquivo (Foto) são tratados de forma especial no HTML,
            # mas podemos adicionar uma classe se necessário
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'cyber-file-input'})
            # Todos os outros campos (texto, números, selects)
            else:
                field.widget.attrs.update({
                    'class': 'cyber-input',
                    'placeholder': f'Aguardando entrada: {field.label}'
                })
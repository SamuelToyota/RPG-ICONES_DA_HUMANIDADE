from django.contrib import admin
from django.utils.html import format_html
from .models import Character, Pericia, Habilidade, Trilha
from .models import Indole


@admin.register(Pericia)
class PericiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atributo_base')
    list_filter = ('atributo_base',)
    search_fields = ('nome',)


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Indole)
class IndoleAdmin(admin.ModelAdmin):
    list_display = ('nome','cor',)
    search_fields = ('nome',)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    # O que aparece na lista principal
    list_display = (
        'nome_do_heroi',
        'nome_do_jogador',
        'classe',
        'nivel',
        'vida',
        'esforco',
        'barra_defesa_lista',  # Mostra a barra na lista
    )

    list_filter = ('classe', 'origem')
    search_fields = ('nome_do_heroi', 'nome_do_jogador')
    filter_horizontal = ('pericias', 'habilidades')

    # Campo de leitura para a barra aparecer dentro da edição
    readonly_fields = ('visual_defesa_barra',)

    # Função para a barra na LISTA
    @admin.display(description="Defesa/Esq")
    def barra_defesa_lista(self, obj):
        porcentagem = min((obj.defesa_esquiva / 50) * 100, 100)
        return format_html(
            '<div style="width: 80px; background: #444; height: 10px; border-radius: 5px; overflow: hidden; border: 1px solid #777;">'
            '<div style="width: {}%; background: #9d4edd; height: 100%;"></div>'
            '</div>', porcentagem
        )

    # Função para a barra DENTRO da ficha
    @admin.display(description="Visualização da Defesa")
    def visual_defesa_barra(self, obj):
        porcentagem = min((obj.defesa_esquiva / 50) * 100, 100)
        return format_html(
            '''
            <div style="background: #222; padding: 10px; border-radius: 5px; display: inline-block;">
                <div style="width: 200px; background: #444; height: 20px; border-radius: 10px; overflow: hidden; border: 1px solid #9d4edd;">
                    <div style="width: {}%; background: linear-gradient(90deg, #9d4edd, #c8b6ff); height: 100%;"></div>
                </div>
                <div style="margin-top: 5px; text-align: center; color: #c8b6ff; font-weight: bold;">{} / 50</div>
            </div>
            ''', porcentagem, obj.defesa_esquiva
        )

    # Organização dos campos ao editar
    fieldsets = (
        ('Identidade', {
            'fields': ('nome_do_heroi', 'nome_do_jogador', 'classe', 'origem', 'nivel', 'trilha', 'indole')
        }),
        ('Status Vitais', {
            'fields': (('vida', 'esforco'), ('defesa_esquiva', 'visual_defesa_barra'))
        }),
        ('Atributos', {
            'fields': ('forca', 'agilidade', 'inteligencia', 'resistencia', 'carisma')
        }),
        ('Equipamento e Poderes', {
            'fields': ('arma', 'pericias', 'habilidades')
        }),
    )
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# =========================
# PERÍCIAS
# =========================
class Pericia(models.Model):
    ATRIBUTOS = [
        ('FOR', 'Força'),
        ('AGI', 'Agilidade'),
        ('INT', 'Inteligência'),
        ('RES', 'Resistência'),
        ('CAR', 'Carisma'),
    ]

    nome = models.CharField(max_length=50, unique=True)
    atributo_base = models.CharField(max_length=3, choices=ATRIBUTOS)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome} ({self.get_atributo_base_display()})"


# =========================
# HABILIDADES
# =========================
class Habilidade(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


# =========================
# TRILHAS (Automáticas por Classe)
# =========================
class Trilha(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


# =========================
# ÍNDOLES (Com Cores Dinâmicas)
# =========================
class Indole(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    # Campo de cor para o Passo 2
    cor = models.CharField(
        max_length=7,
        default="#00ff88",
        help_text="Cor em Hexadecimal (ex: #ff4d4d)"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Índole"
        verbose_name_plural = "Índoles"


# =========================
# PERSONAGEM
# =========================
class Character(models.Model):
    CLASSES = [
        ('TIT', 'Titã'),
        ('VEL', 'Velocista'),
        ('MEN', 'Mentalista'),
        ('MUT', 'Mutante'),
    ]

    momentum = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        verbose_name="Carga de Momentum"
    )

    @property
    def nivel_momentum(self):
        if self.momentum >= 8: return "MÁXIMO"
        if self.momentum >= 5: return "ALTO"
        if self.momentum >= 1: return "ATIVO"
        return "INATIVO"

    class Origem(models.TextChoices):
        HUMANO = 'HUM', 'Humano Excepcional'
        EXPERIMENTO = 'EXP', 'Experimento Científico'
        PSIQUICO = 'PSI', 'Psíquico Desperto'
        CIBORGUE = 'CIB', 'Ciborgue'
        MUTANTE = 'MUT', 'Mutação Natural'
        COSMICO = 'COS', 'Energia Cósmica'
        MISTICO = 'MIS', 'Entidade Mística'
        MALDICAO = 'MAL', 'Maldição ou Transformação'
        CLONE = 'CLO', 'Clone ou Criação Artificial'
        ALIENIGENA = 'ALI', 'Alienígena'

    class Armas(models.TextChoices):
        SOCO = 'SOC', 'Soco / Punho (1d4, crítico 20)'
        BASTAO = 'BAS', 'Bastão (1d6, crítico 20)'
        ADA = 'ADA', 'Adaga (1d6, crítico 18)'
        ESPADA = 'ESP', 'Espada (2d8, crítico 19)'
        MACHADO = 'MAC', 'Machado (2d10, crítico 20)'
        MARTELO = 'MAR', 'Martelo (2d12, crítico 20)'
        LEN = 'LEN', 'Lâmina de Energia (3d8, crítico 19)'
        CHI = 'CHI', 'Chicote (1d8, crítico 18)'
        GAR = 'GAR', 'Garras (2d6, crítico 19)'
        LAN = 'LAN', 'Lança (2d8, crítico 20)'
        NUN = 'NUN', 'Nunchaku (2d6, crítico 18)'
        ARC = 'ARC', 'Arco (1d8, crítico 20)'
        BES = 'BES', 'Besta (2d8, crítico 19)'
        PIS = 'PIS', 'Pistola (2d6, crítico 19)'
        REV = 'REV', 'Revólver (2d8, crítico 20)'
        SUB = 'SUB', 'Submetralhadora (2d6, crítico 18)'
        RIF = 'RIF', 'Rifle (2d10, crítico 20)'
        ESC = 'ESC', 'Escopeta (3d8, crítico 20)'
        SNI = 'SNI', 'Rifle de Precisão (3d10, crítico 20)'
        CAN = 'CAN', 'Canhão de Energia (2d10, crítico 20)'
        RAI = 'RAI', 'Raio laser (3d8, crítico 19)'

    nome_do_jogador = models.CharField(max_length=100)
    nome_do_heroi = models.CharField(max_length=100)
    classe = models.CharField(max_length=3, choices=CLASSES)
    origem = models.CharField(max_length=3, choices=Origem.choices)
    arma = models.CharField(max_length=3, choices=Armas.choices)

    trilha = models.ForeignKey(Trilha, on_delete=models.SET_NULL, null=True, blank=True, related_name='personagens')
    indole = models.ForeignKey(Indole, on_delete=models.SET_NULL, null=True, blank=True)

    foto = models.ImageField(upload_to='herois/', null=True, blank=True, verbose_name="Foto do Herói")

    vida = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(100)])
    esforco = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(100)])
    defesa_esquiva = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(50)],
        verbose_name="Defesa / Esquiva"
    )
    nivel = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    forca = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    agilidade = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    inteligencia = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    resistencia = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    carisma = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])

    pericias = models.ManyToManyField(Pericia, blank=True, related_name='personagens')
    habilidades = models.ManyToManyField(Habilidade, blank=True, related_name='personagens')

    def save(self, *args, **kwargs):
        # Mapeamento para buscar os nomes reais das Trilhas e Índoles
        mapeamento_nomes = {
            'TIT': 'Titã',
            'VEL': 'Velocista',
            'MEN': 'Mentalista',
            'MUT': 'Mutante',
        }

        nome_correspondente = mapeamento_nomes.get(self.classe)

        if nome_correspondente:
            # Busca e salva a TRILHA automaticamente
            trilha_obj = Trilha.objects.filter(nome__iexact=nome_correspondente).first()
            self.trilha = trilha_obj

            # Busca e salva a ÍNDOLE automaticamente
            indole_obj = Indole.objects.filter(nome__iexact=nome_correspondente).first()
            self.indole = indole_obj

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_do_heroi} ({self.nome_do_jogador})"
from django.db import models
from django.utils import timezone

# ENTIDADE A: PROFESSOR
class Professor(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    departamento = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)  # Indica se está em exercício
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# ENTIDADE C: ALUNO
class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=50, help_text="Para análises estatísticas")

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

# ENTIDADE B: TURMA
class Turma(models.Model):
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    nome = models.CharField(max_length=255, help_text="Ex: Estatística Aplicada I")
    descricao = models.TextField(blank=True, null=True)
    
    # Relacionamento 1:N - Um professor pode ter várias turmas
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='turmas')
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVA')

    # Relacionamento N:N - Turma tem vários alunos (tabela intermediária 'Matricula' abaixo)
    alunos = models.ManyToManyField(Aluno, through='Matricula', related_name='turmas_matriculadas')

    # Relacionamento 1:1 - Representante da turma (Um aluno só pode ser representante de uma turma)
    representante = models.OneToOneField(
        Aluno, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='representante_de_turma'
    )

    def __str__(self):
        return f"{self.nome} - {self.status}"

# TABELA DE JUNÇÃO (N:N Turma <-> Aluno)
class Matricula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')
    data_matricula = models.DateTimeField(auto_now_add=True)
    presenca_acumulada = models.IntegerField(default=0, help_text="Total de presenças calculada")

    class Meta:
        unique_together = ('turma', 'aluno') # Garante que o aluno não se matricule 2x na mesma turma

    def __str__(self):
        return f"{self.aluno} na {self.turma}"

# ENTIDADE AUXILIAR: PRESENÇA
class Presenca(models.Model):
    STATUS_PRESENCA = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('JUSTIFICADO', 'Justificado'),
    ]

    # Relaciona com a matrícula específica (vínculo aluno-turma)
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='historico_presencas')
    data = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_PRESENCA)

    def __str__(self):
        return f"{self.matricula.aluno.nome} - {self.data} - {self.status}"
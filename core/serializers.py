from rest_framework import serializers
from .models import Professor, Turma, Aluno, Matricula, Presenca

# --- Serializers Públicos (Resumidos) ---
# Usados nas listagens gerais para proteger dados pessoais

class ProfessorPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'departamento'] # Apenas o permitido pelo PDF

class TurmaPublicaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.ReadOnlyField(source='professor.nome')
    class Meta:
        model = Turma
        fields = ['id', 'nome', 'status', 'professor_nome'] # Sem detalhes internos

# --- Serializers Completos (Detalhados) ---
# Usados quando se clica em um item específico ou se é Admin

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__' # Mostra e-mail e cadastro (apenas para detalhe)

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'

# --- Serializers Compostos ---

class TurmaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.ReadOnlyField(source='professor.nome')

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'descricao', 'professor', 'professor_nome', 'data_inicio', 'data_fim', 'status', 'representante']

class MatriculaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    aluno_id = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), source='aluno', write_only=True)

    class Meta:
        model = Matricula
        fields = ['id', 'turma', 'aluno', 'aluno_id', 'data_matricula', 'presenca_acumulada']

# --- Serializer do Dashboard ---
class TurmaDashboardSerializer(serializers.ModelSerializer):
    professor = ProfessorPublicoSerializer(read_only=True)
    lista_alunos = MatriculaSerializer(source='matricula_set', many=True, read_only=True)
    representante = AlunoSerializer(read_only=True)

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'status', 'professor', 'representante', 'lista_alunos']

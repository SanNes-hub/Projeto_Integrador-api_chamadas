from rest_framework import serializers
from .models import Professor, Turma, Aluno, Matricula, Presenca

# --- Serializers Básicos ---

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'

# --- Serializers Compostos (Para respostas mais complexas) ---

class TurmaSerializer(serializers.ModelSerializer):
    # Mostra o nome do professor em vez de apenas o ID ao listar
    professor_nome = serializers.ReadOnlyField(source='professor.nome')

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'descricao', 'professor', 'professor_nome', 'data_inicio', 'data_fim', 'status', 'representante']

class MatriculaSerializer(serializers.ModelSerializer):
    # Traz os detalhes do aluno junto com a matrícula
    aluno = AlunoSerializer(read_only=True)
    aluno_id = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), source='aluno', write_only=True)

    class Meta:
        model = Matricula
        fields = ['id', 'turma', 'aluno', 'aluno_id', 'data_matricula', 'presenca_acumulada']

# --- Serializer Especial para o Dashboard ---
class TurmaDashboardSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    # Traz a lista de matrículas (que contém alunos + presenças)
    lista_alunos = MatriculaSerializer(source='matricula_set', many=True, read_only=True)
    representante = AlunoSerializer(read_only=True)

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'status', 'professor', 'representante', 'lista_alunos']
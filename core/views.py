from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Professor, Turma, Aluno, Matricula, Presenca
from .serializers import (
    ProfessorSerializer, TurmaSerializer, AlunoSerializer, 
    MatriculaSerializer, PresencaSerializer, TurmaDashboardSerializer
)

# Permissão personalizada: Leitura para todos, Escrita apenas para logados
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Rota: GET /api/professores/{id}/turmas/
    @action(detail=True, methods=['get'])
    def turmas(self, request, pk=None):
        professor = self.get_object()
        turmas = Turma.objects.filter(professor=professor)
        serializer = TurmaSerializer(turmas, many=True)
        return Response(serializer.data)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Rota: POST /api/turmas/{id}/atribuir-professor/
    @action(detail=True, methods=['post'])
    def atribuir_professor(self, request, pk=None):
        turma = self.get_object()
        professor_id = request.data.get('professor_id')
        professor = get_object_or_404(Professor, id=professor_id)
        turma.professor = professor
        turma.save()
        return Response({'status': f'Professor {professor.nome} atribuído à turma.'})

    # Rota: GET /api/turmas/{id}/alunos/
    @action(detail=True, methods=['get'])
    def alunos(self, request, pk=None):
        turma = self.get_object()
        matriculas = Matricula.objects.filter(turma=turma)
        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data)

    # Rota: POST /api/turmas/{id}/matricular-aluno/
    @action(detail=True, methods=['post'])
    def matricular_aluno(self, request, pk=None):
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        # Cria a matrícula se não existir
        Matricula.objects.get_or_create(turma=turma, aluno=aluno)
        return Response({'status': f'Aluno {aluno.nome} matriculado com sucesso.'})

    # Rota: PUT /api/turmas/{id}/definir-representante/
    @action(detail=True, methods=['put'])
    def definir_representante(self, request, pk=None):
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        # Regra: Um aluno só pode ser representante de UMA turma
        if hasattr(aluno, 'representante_de_turma'):
            return Response({'error': 'Este aluno já é representante de outra turma.'}, status=400)

        turma.representante = aluno
        turma.save()
        return Response({'status': f'Aluno {aluno.nome} é o novo representante.'})

    # Rota: GET /api/turmas/{id}/dashboard/
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        turma = self.get_object()
        serializer = TurmaDashboardSerializer(turma)
        return Response(serializer.data)

class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas logados podem mexer em presença
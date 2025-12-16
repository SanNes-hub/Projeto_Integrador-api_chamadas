from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Professor, Turma, Aluno, Matricula, Presenca
from .serializers import (
    ProfessorSerializer, ProfessorPublicoSerializer,
    TurmaSerializer, TurmaPublicaSerializer, TurmaDashboardSerializer,
    AlunoSerializer, MatriculaSerializer, PresencaSerializer
)

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfessorPublicoSerializer
        return ProfessorSerializer

    @action(detail=True, methods=['get'])
    def turmas(self, request, pk=None):
        professor = self.get_object()
        turmas = Turma.objects.filter(professor=professor)
        serializer = TurmaPublicaSerializer(turmas, many=True)
        return Response(serializer.data)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated] 

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Se o usuário estiver logado (Admin/Professor), vê TUDO (Ativas, Canceladas, Concluídas)
        if self.request.user.is_authenticated:
            return Turma.objects.all()
        # Se for público (anônimo), vê APENAS as turmas ATIVAS
        return Turma.objects.filter(status='ATIVA')

    def get_serializer_class(self):
        if self.action == 'list':
            return TurmaPublicaSerializer # Listagem pública (Sem representante/datas)
        return TurmaSerializer # Detalhe completo

    @action(detail=True, methods=['post'])
    def atribuir_professor(self, request, pk=None):
        turma = self.get_object()
        professor_id = request.data.get('professor_id')
        professor = get_object_or_404(Professor, id=professor_id)
        turma.professor = professor
        turma.save()
        return Response({'status': f'Professor {professor.nome} atribuído à turma.'})

    @action(detail=True, methods=['get'])
    def alunos(self, request, pk=None):
        turma = self.get_object()
        matriculas = Matricula.objects.filter(turma=turma)
        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def matricular_aluno(self, request, pk=None):
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        aluno = get_object_or_404(Aluno, id=aluno_id)
        Matricula.objects.get_or_create(turma=turma, aluno=aluno)
        return Response({'status': f'Aluno {aluno.nome} matriculado com sucesso.'})

    @action(detail=True, methods=['put'])
    def definir_representante(self, request, pk=None):
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        if hasattr(aluno, 'representante_de_turma'):
            return Response({'error': 'Este aluno já é representante de outra turma.'}, status=400)

        turma.representante = aluno
        turma.save()
        return Response({'status': f'Aluno {aluno.nome} é o novo representante.'})

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        turma = self.get_object()
        serializer = TurmaDashboardSerializer(turma)
        return Response(serializer.data)

class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer
    permission_classes = [permissions.IsAuthenticated]

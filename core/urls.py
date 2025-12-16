from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet, TurmaViewSet, AlunoViewSet, PresencaViewSet

# O Router cria automaticamente as rotas padrão (listagem, criação, edição, exclusão)
router = DefaultRouter()
router.register(r'professores', ProfessorViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'presencas', PresencaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
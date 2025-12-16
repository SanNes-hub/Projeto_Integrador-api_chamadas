from django.contrib import admin
from .models import Professor, Turma, Aluno, Matricula, Presenca

# Isso faz as tabelas aparecerem no painel /admin
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Matricula)
admin.site.register(Presenca)
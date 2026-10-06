from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome 

    class Meta: 
        verbose_name_plural = "Categorias"


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita 📈'),
        ('D', 'Despesa 📉'),
    ]
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    data = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = "Transações"
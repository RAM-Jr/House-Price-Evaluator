from django.db import models

# Create your models here.

class Imovel(models.Model):
    cod_imovel = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    venda_ou_aluguel = models.CharField(max_length=10)
    design = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    tipologia = models.CharField(max_length=5)
    moveis = models.CharField(max_length=1)
    guardaFatos = models.CharField(max_length=1)
    arCondicionado = models.CharField(max_length=1)
    garagem = models.CharField(max_length=1)
    cozinhaAmericana = models.CharField(max_length=1)
    numWC = models.PositiveIntegerField()
    suite = models.CharField(max_length=1)
    vista = models.CharField(max_length=1)
    piscina = models.CharField(max_length=1)
    obras = models.CharField(max_length=1)

    def __str__(self):
        return self.design + " - "+ self.bairro

class Avaliacao(models.Model):
    cod_avaliação = models.AutoField(primary_key=True)
    cod_imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    preco = models.FloatField()

    def __str__(self):
        return f"Avaliação de {self.cod_imovel.design} em {self.data_avaliacao.strftime('%Y-%m-%d')}"

class Tipologia(models.Model):
    id = models.AutoField(primary_key=True)
    tipologia = models.CharField(max_length=5)
    def __str__(self):
        return self.tipologia

class Design(models.Model):
    id = models.AutoField(primary_key=True)
    design = models.CharField(max_length=10)
    def __str__(self):
        return self.design

class Bairro(models.Model):
    id = models.AutoField(primary_key=True)
    bairro = models.CharField(max_length=50)
    def __str__(self):
        return self.bairro

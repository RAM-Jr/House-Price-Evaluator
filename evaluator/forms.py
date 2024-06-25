# forms.py
from django import forms
from .models import Bairro, Tipologia, Design, Imovel
from django.core.validators import MinValueValidator

class CreateImovel(forms.ModelForm):
    venda_ou_aluguel = forms.ChoiceField(choices=[('V', 'Venda'), ('A', 'Aluguel')], required=True)
    design = forms.ChoiceField(required=True)
    bairro = forms.ChoiceField(required=True)
    tipologia = forms.ChoiceField(required=True)
    moveis = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    guardaFatos = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    arCondicionado = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    garagem = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    cozinhaAmericana = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    numWC = forms.ChoiceField(choices=((i,i) for i in range(0, 21)), required=True)
    suite = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    vista = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    piscina = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)
    obras = forms.ChoiceField(choices=[('C', 'Possui'), ('S', 'Não Possui')], required=True)

    class Meta:
        model = Imovel
        fields = ['venda_ou_aluguel', 'design', 'bairro', 'tipologia', 'moveis', 'guardaFatos', 'arCondicionado',
                  'garagem', 'cozinhaAmericana', 'numWC', 'suite', 'vista', 'piscina', 'obras']

    def __init__(self, *args, **kwargs):
        super(CreateImovel, self).__init__(*args, **kwargs)
        self.fields['design'].choices = [(design.design, design.design) for design in Design.objects.all()]
        self.fields['bairro'].choices = [(bairro.bairro, bairro.bairro) for bairro in Bairro.objects.all()]
        self.fields['tipologia'].choices = [(tipologia.tipologia, tipologia.tipologia) for tipologia in Tipologia.objects.all()]

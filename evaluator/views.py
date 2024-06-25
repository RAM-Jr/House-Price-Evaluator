from django.shortcuts import render,redirect
from .models import Imovel,Bairro,Design,Tipologia,Avaliacao
from django.http import HttpResponse
import locale
from . import forms
import pickle
from .house_evaluator_module import Evaluation_model
# from .custom_scaler import CustomScaler
import pandas as pd
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa


def evaluation_form(request):
    if request.method == "POST":
        form = forms.CreateImovel(request.POST)
        if form.is_valid():
            # form.save()
            return redirect('evaluations:result')
    else:
        form = forms.CreateImovel()

    return render(request, 'evaluator/evaluation_form.html', {'form': form})


def evaluation_result(request):
    path = r'C:\Users\Munguambe\Documents\FILE\Trabalho de Licenciatura\House_Evaluator\evaluator\house_evaluation_model.pkl'
    eval_model = Evaluation_model(path)

    imovel=Imovel()

    finalidade = request.POST.get('venda_ou_aluguel')
    design = request.POST.get('design')
    bairro = request.POST.get('bairro')
    tipologia = request.POST.get('tipologia')
    moveis = request.POST.get('moveis')
    guardafatos = request.POST.get('guardaFatos')
    arcondicionado = request.POST.get('arCondicionado')
    garagem = request.POST.get('garagem')
    cozinhaamericana = request.POST.get('cozinhaAmericana')
    numWC = float(request.POST.get('numWC'))
    suite = request.POST.get('suite')
    vista = request.POST.get('vista')
    piscina = request.POST.get('piscina')
    obras = request.POST.get('obras')

    imovel.venda_ou_aluguel = finalidade
    imovel.design = design
    imovel.bairro = bairro
    imovel.tipologia = tipologia
    imovel.moveis = moveis
    imovel.guardaFatos = guardafatos
    imovel.arCondicionado = arcondicionado
    imovel.garagem = garagem
    imovel.cozinhaAmericana = cozinhaamericana
    imovel.numWC = numWC
    imovel.suite = suite
    imovel.vista = vista
    imovel.piscina = piscina
    imovel.obras = obras

    imovel.save()

    input = pd.DataFrame([{
        'Nº': 1, 'Design': design, 'Finalidade': finalidade, 'Bairro': bairro, 'Tipologia': tipologia, 'Moveis': moveis,
        'Guarda-Fatos': guardafatos, 'Ar-Condicionado': arcondicionado, 'Garagem': garagem,
        'Cozinha Americana': cozinhaamericana,
        'Nº WC\'s': numWC, 'Suite': suite, 'Vista': vista, 'Piscina': piscina, 'Obras': obras
    }])

    predicted_price = float(eval_model.get_prediction(input)[0])

    avaliacao = Avaliacao()
    avaliacao.cod_imovel = imovel
    avaliacao.preco = predicted_price
    avaliacao.save()

    # evaluation = Avaliacao.objects.get(cod_imovel=cod_imovel)
    locale.setlocale(locale.LC_ALL, '')

    context = {
        'result': "{:,}".format(predicted_price),
        'finalidade': 'Venda' if finalidade=='V' else 'Aluguel',
        'design': design,
        'bairro': bairro,
        'tipologia': tipologia,
        'moveis':'Possui' if moveis=='C' else 'Não Possui',
        'guardafatos': 'Possui' if guardafatos=='C' else 'Não Possui',
        'arcondicionado': 'Possui' if arcondicionado=='C' else 'Não Possui',
        'garagem': 'Possui' if garagem=='C' else 'Não Possui',
        'cozinhaamericana': 'Possui' if cozinhaamericana=='C' else 'Não Possui',
        'numWC': int(numWC),
        'suite': 'Possui' if suite=='C' else 'Não Possui',
        'vista': 'Possui' if vista=='C' else 'Não Possui',
        'piscina': 'Possui' if piscina=='C' else 'Não Possui',
        'obras': 'Possui' if obras=='C' else 'Não Possui',
    }

    return render(request, 'evaluator/evaluation_result.html', context)

class ExportPDFView(View):
    def post(self, request, *args, **kwargs):
        result = request.POST.get('result')
        finalidade = request.POST.get('finalidade')
        design = request.POST.get('design')
        bairro = request.POST.get('bairro')
        tipologia = request.POST.get('tipologia')
        moveis = request.POST.get('moveis')
        guardafatos = request.POST.get('guardafatos')
        arcondicionado = request.POST.get('arcondicionado')
        garagem = request.POST.get('garagem')
        cozinhaamericana = request.POST.get('cozinhaamericana')
        numWC = request.POST.get('numWC')
        suite = request.POST.get('suite')
        vista = request.POST.get('vista')
        piscina = request.POST.get('piscina')
        obras = request.POST.get('obras')

        context = {
            'result': result,
            'finalidade': finalidade,
            'design': design,
            'bairro': bairro,
            'tipologia': tipologia,
            'moveis': moveis,
            'guardafatos': guardafatos,
            'arcondicionado': arcondicionado,
            'garagem': garagem,
            'cozinhaamericana': cozinhaamericana,
            'numWC': numWC,
            'suite': suite,
            'vista': vista,
            'piscina': piscina,
            'obras': obras,
        }

        # Render template with context
        template_path = 'evaluator/export_template.html'
        template = get_template(template_path)
        rendered_html = template.render(context)

        print(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resultado_avaliação.pdf"'

        # Create PDF
        pisa_status = pisa.CreatePDF(rendered_html, dest=response)
        if pisa_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        return response
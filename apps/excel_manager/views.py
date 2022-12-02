from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import json
from apps.excel_manager.services.excel_summarizer import export_excel_summary
# Create your views here.

class HomeView(TemplateView):
    template_name = 'excel_manager/home.html'


def summarize_files(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        input_path = data.get('inputPath')
        output_path = data.get('outputPath')
        target_values = data.get('targetValues')


        # modify to be a list
        target_values = target_values.split(',')
        target_values = [value.strip() for value in target_values]
        try:
            file_count = export_excel_summary(
                input_path=input_path,
                output_path=output_path,
                targeted_values=target_values
            )
        except ValidationError as e:
            print(e)
            response = JsonResponse(status=400, data={'ValidationError': str(e)})
            return response
        else:
            response = JsonResponse(status=200, data=file_count)
            return response

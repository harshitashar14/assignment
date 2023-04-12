from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import uuid
# Create your views here.
from rest_framework.views import APIView
from .models import Report
from .tasks import generate_csv_report
from .serializers import ReportResponseSerializer

class TriggerReportView(APIView):

    def get(self, request):
        report_obj = Report.objects.create()

        generate_csv_report.delay(report_obj.report_id)

        return JsonResponse({
            'status': 'succeded',
            'code': 200,
            'data': {
                'id': str(report_obj.report_id)
            },
        })


class GetReportView(APIView):

    def get(self, request, report_id):
        report_obj = Report.objects.get(report_id=report_id)

        output_data = ReportResponseSerializer(report_obj , many=False)

        data = output_data.data
        return JsonResponse({
            'status': 'succeeded',
            'code': 200,
            'data': data,
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import report
from .serializers import ReportSerializer

class all_reports(APIView):
    permission_classes = []

    def get(self, request):
        reports = report.objects.all().order_by('-created_at')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportCreateView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

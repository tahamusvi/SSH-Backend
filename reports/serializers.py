from rest_framework import serializers
from .models import report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = report
        fields = ['id', 'name', 'short_reason', 'email', 'message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

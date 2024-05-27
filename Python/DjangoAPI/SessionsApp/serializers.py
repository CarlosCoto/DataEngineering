from rest_framework import serializers
from SessionsApp.models import Sessions

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sessions
        fields=('customer_id','median_visits_before_order','median_session_duration_minutes_before_order')

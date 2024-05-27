from django.db import models

# Create your models here.

class Sessions(models.Model):

    customer_id = models.BigIntegerField(null=True)

    median_visits_before_order = models.BigIntegerField(null=True)

    median_session_duration_minutes_before_order = models.CharField(max_length=500,null=True)



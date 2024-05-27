# Generated by Django 4.2 on 2023-04-26 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=500)),
                ('median_visits_before_order', models.CharField(max_length=500)),
                ('median_session_duration_minutes_before_order', models.CharField(max_length=500)),
            ],
        ),
    ]

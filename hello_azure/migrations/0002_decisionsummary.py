# Generated by Django 4.2.7 on 2024-05-09 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_azure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecisionSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('stock', models.CharField(max_length=10)),
                ('decision', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=20)),
            ],
        ),
    ]

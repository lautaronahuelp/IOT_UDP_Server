# Generated by Django 5.0.6 on 2024-06-23 00:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comando',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('comando', models.TextField()),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

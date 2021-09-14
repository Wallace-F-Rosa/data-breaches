# Generated by Django 3.2.7 on 2021-09-11 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_breaches', '0002_alter_source_data_breach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databreach',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entity', to='data_breaches.entity'),
        ),
        migrations.AlterField(
            model_name='source',
            name='data_breach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='databreach', to='data_breaches.databreach'),
        ),
    ]
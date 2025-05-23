# Generated by Django 5.2 on 2025-05-14 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_thirdpartyadmetrics'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='发票抬头', max_length=255)),
                ('tax_number', models.CharField(help_text='税号', max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, help_text='开票金额', max_digits=10)),
                ('status', models.CharField(choices=[('pending', '待开票'), ('issued', '已开票'), ('rejected', '已驳回')], default='pending', max_length=20)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

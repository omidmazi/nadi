# Generated by Django 3.2.6 on 2022-09-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='authority',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
    ]
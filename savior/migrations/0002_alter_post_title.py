# Generated by Django 4.2.3 on 2023-08-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savior', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=30, verbose_name='제목'),
        ),
    ]
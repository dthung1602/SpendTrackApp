# Generated by Django 2.1.2 on 2018-12-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spendtrackapp', '0002_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(default='Unnamed plan', max_length=50),
            preserve_default=False,
        ),
    ]

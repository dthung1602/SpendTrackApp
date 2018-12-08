# Generated by Django 2.1.2 on 2018-12-05 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spendtrackapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('planned_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('compare', models.CharField(choices=[('>', 'gt'), ('=', 'eq'), ('<', 'lt')], max_length=1)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spendtrackapp.Category')),
            ],
        ),
    ]
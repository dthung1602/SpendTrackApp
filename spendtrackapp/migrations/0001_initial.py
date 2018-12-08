# Generated by Django 2.1.2 on 2018-11-13 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spendtrackapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('content', models.CharField(max_length=250)),
                ('value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('categories', models.ManyToManyField(to='spendtrackapp.Category')),
                ('leaf_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='leaf_category', to='spendtrackapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value_type', models.CharField(choices=[('i', 'integer'), ('f', 'float'), ('s', 'string'), ('b', 'boolean')], max_length=1)),
                ('_value', models.CharField(max_length=500)),
            ],
        ),
    ]
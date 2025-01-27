# Generated by Django 3.1.1 on 2020-09-11 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='first_actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.actor'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='second_actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.actor'),
        ),
    ]

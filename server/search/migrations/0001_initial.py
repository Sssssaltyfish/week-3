# Generated by Django 3.1.1 on 2020-09-11 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('summary', models.TextField()),
                ('cover', models.URLField()),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('first_actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.actor')),
                ('second_actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.actor')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('title', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('cover', models.URLField()),
                ('summary', models.TextField()),
                ('comments', models.TextField()),
                ('actors', models.ManyToManyField(blank=True, to='search.Actor')),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='relations',
            field=models.ManyToManyField(blank=True, through='search.Relationship', to='search.Actor'),
        ),
    ]
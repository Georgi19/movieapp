# Generated by Django 3.2.8 on 2021-11-22 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=2000)),
                ('popularity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('poster_path', models.CharField(max_length=2000, null=True)),
                ('backdrop_path', models.CharField(max_length=2000, null=True)),
                ('vote_avg', models.DecimalField(decimal_places=3, max_digits=10)),
                ('vote_count', models.IntegerField()),
                ('adult', models.BooleanField(default=False)),
                ('release_date', models.CharField(max_length=200)),
                ('overview', models.TextField(default='N/A')),
                ('genres', models.ManyToManyField(to='main.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='NewMovies',
            fields=[
                ('title', models.CharField(max_length=2000)),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewPeople',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, default='default_profile.png', null=True, upload_to='')),
                ('seen_movies', models.ManyToManyField(to='main.Movie')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.IntegerField()),
                ('popularity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('profile_path', models.CharField(max_length=2000, null=True)),
                ('birthday', models.CharField(default='N/A', max_length=200, null=True)),
                ('biography', models.TextField(default='N/A', null=True)),
                ('place_of_birth', models.TextField(default='N/A', max_length=200, null=True)),
                ('known_for_department', models.CharField(default='N/A', max_length=100, null=True)),
                ('movies', models.ManyToManyField(to='main.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='people',
            field=models.ManyToManyField(to='main.Person'),
        ),
    ]

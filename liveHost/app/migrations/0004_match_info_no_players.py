# Generated by Django 5.0.6 on 2024-06-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_player_match_stats_player_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match_info',
            name='no_players',
            field=models.IntegerField(db_default=5),
        ),
    ]

# Generated by Django 2.0.2 on 2018-02-26 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(default='', max_length=60)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(choices=[('PS', 'PokerStars')], default='PS', max_length=3)),
                ('name', models.CharField(max_length=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Country')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entries', models.SmallIntegerField(default=1)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to='traffic.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('room', models.CharField(choices=[('PS', 'PokerStars')], default='PS', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Scanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(choices=[('PS', 'PokerStars')], default='PS', max_length=3)),
                ('name', models.CharField(max_length=15)),
                ('game', models.CharField(choices=[('NL', "NL Hold'em"), ('PLO', 'PL Omaha'), ('PLO8', 'PL Omaha H/L'), ('NLO8', 'NL Omaha H/L')], default='NL', max_length=4)),
                ('limit', models.IntegerField(default=0)),
                ('max_players', models.IntegerField(default=6)),
            ],
            options={
                'ordering': ('room', 'game', 'max_players', 'limit'),
            },
        ),
        migrations.CreateModel(
            name='TableScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_count', models.SmallIntegerField(default=0)),
                ('average_pot', models.FloatField(default=0.0)),
                ('players_per_flop', models.SmallIntegerField(default=0)),
                ('unique_player_count', models.SmallIntegerField(default=0)),
                ('entry_count', models.SmallIntegerField(default=0)),
                ('scan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_scans', to='traffic.Scan')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_scans', to='traffic.Table')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='table',
            unique_together={('room', 'name')},
        ),
        migrations.AddField(
            model_name='scan',
            name='scanner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to='traffic.Scanner'),
        ),
        migrations.AddField(
            model_name='playerscan',
            name='table_scan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='traffic.TableScan'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('room', 'name')},
        ),
    ]

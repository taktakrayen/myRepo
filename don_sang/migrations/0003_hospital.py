from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('don_sang', '0002_don_age_don_disponibilite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('ville', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('capacite', models.PositiveIntegerField(default=0, help_text='Capacité de stockage de poches de sang')),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Hôpital',
                'verbose_name_plural': 'Hôpitaux',
                'ordering': ['nom'],
            },
        ),
    ]

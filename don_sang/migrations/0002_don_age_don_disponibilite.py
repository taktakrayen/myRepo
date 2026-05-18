from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('don_sang', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='don',
            name='age',
            field=models.PositiveIntegerField(default=18, help_text='Âge du donneur'),
        ),
        migrations.AddField(
            model_name='don',
            name='disponibilite',
            field=models.CharField(
                choices=[('disponible', 'Disponible'), ('indisponible', 'Indisponible'), ('bientot', 'Disponible bientôt')],
                default='disponible',
                max_length=20,
            ),
        ),
    ]

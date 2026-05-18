import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('don_sang', '0003_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='don',
            name='hopital',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='dons',
                to='don_sang.hospital',
                verbose_name='Hôpital',
            ),
        ),
    ]

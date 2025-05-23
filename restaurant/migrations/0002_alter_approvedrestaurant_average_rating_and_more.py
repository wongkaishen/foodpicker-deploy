import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='average_rating',
            field=models.FloatField(db_index=True, default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Average Rating'),

        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='cuisine_type',
            field=models.CharField(choices=[('ASIAN', 'Asian'), ('ITALIAN', 'Italian'), ('MEXICAN', 'Mexican'), ('AMERICAN', 'American'), ('INDIAN', 'Indian'), ('MEDITERRANEAN', 'Mediterranean'), ('OTHER', 'Other')], db_index=True, default='OTHER', max_length=50, verbose_name='Cuisine Type'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='delivery_available',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Delivery Available'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='latitude',
            field=models.FloatField(blank=True, db_index=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='longitude',
            field=models.FloatField(blank=True, db_index=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Restaurant Name'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='price_range',
            field=models.CharField(choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Fine Dining')], db_index=True, default='$$', max_length=4, verbose_name='Price Range'),
        ),
        migrations.AlterField(
            model_name='approvedrestaurant',
            name='takeout_available',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Takeout Available'),
        ),

        migrations.AlterField(
            model_name='restaurant',
            name='average_rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Average Rating'),
        ),
    ]

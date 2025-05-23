# Generated by Django 4.2.19 on 2025-03-22 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='dishes/')),
                ('category', models.CharField(choices=[('Salads', 'Salads'), ('Soups', 'Soups'), ('Chicken-Dishes', 'Chicken Dishes'), ('Beef-Dishes', 'Beef Dishes'), ('Seafood-Dishes', 'Seafood Dishes'), ('Vegetable-Dishes', 'Vegetable Dishes'), ('Bits&Bites', 'Bits & Bites'), ('On-The-Side', 'On The Side')], max_length=50)),
                ('spiciness_level', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('has_walnuts', models.BooleanField(default=False)),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.cart')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.dish')),
            ],
        ),
    ]

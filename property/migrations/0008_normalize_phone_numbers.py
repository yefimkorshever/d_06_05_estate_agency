# Generated by Django 2.2.24 on 2022-09-15 14:08

from django.db import migrations
import phonenumbers

# pylint: disable=unused-argument


def normalize_phone_numbers(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')  # noqa: N806
    flats = Flat.objects.all()
    if not flats.exists():
        return
    for flat in flats.iterator():
        number_card = phonenumbers.parse(flat.owners_phonenumber, 'RU')
        if not phonenumbers.is_valid_number(number_card):
            continue

        prefix = f'+{number_card.country_code}'
        flat.owner_pure_phone = f'{prefix}{number_card.national_number}'

        flat.save(update_fields=['owner_pure_phone'])


def revert_normalize_phone_numbers(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')  # noqa: N806
    Flat.objects.all().update(owner_pure_phone='')


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(
            normalize_phone_numbers,
            revert_normalize_phone_numbers
        )
    ]

import faker
from faker.providers.phone_number.ru_RU import Provider as RUPhoneProvider

fake = faker.Faker()
fake.add_provider(RUPhoneProvider)


def get_fake_user(is_active: bool = True, is_superuser: bool = False, is_verified: bool = False):
    return dict(
        username=fake.unique.user_name(),
        email=fake.unique.email(domain='mail.ru'),
        phone_number=fake.unique.phone_number(),
        password=fake.unique.password(),
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

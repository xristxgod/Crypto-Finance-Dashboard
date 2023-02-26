import faker
from faker.providers.phone_number.ru_RU import Provider as RUPhoneProvider

fake = faker.Faker()
fake.add_provider(RUPhoneProvider)


def get_fake_telegram(user_id: int, is_active: bool = True):
    return dict(
        id=fake.unique.random_number(fix_len=False, digits=7),
        username='@' + fake.unique.user_name(),
        is_active=is_active,
        user_id=user_id,
    )

import factory

from drf_starter_template.users.models import User
from drf_starter_template.utils.faker import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    name = factory.LazyAttribute(lambda _: faker.name())
    password = factory.LazyAttribute(
        lambda _: faker.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )
    )
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" not in kwargs:
            kwargs["is_superuser"] = False
        return manager.create_user(**kwargs)


class StaffUserFactory(UserFactory):
    is_staff = True


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True

import factory
from django.utils import timezone

from drf_starter_template.utils.faker import faker


class BaseModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    id = factory.LazyAttribute(lambda _: faker.uuid4())
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    deleted_at = None
    is_deleted = False

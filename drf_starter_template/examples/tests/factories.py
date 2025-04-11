from datetime import timedelta

import factory
from django.utils import timezone

from drf_starter_template.examples.models import Todo
from drf_starter_template.utils.faker import faker


class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    id = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=5))
    description = factory.LazyAttribute(lambda _: faker.paragraph())
    completed = False
    priority = Todo.PRIORITY_MEDIUM
    due_date = factory.LazyAttribute(
        lambda _: timezone.now().date() + timedelta(days=7)
    )


class CompletedTodoFactory(TodoFactory):
    completed = True


class HighPriorityTodoFactory(TodoFactory):
    priority = Todo.PRIORITY_HIGH


class LowPriorityTodoFactory(TodoFactory):
    priority = Todo.PRIORITY_LOW

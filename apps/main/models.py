from django.db import models

from auths.models import CustomUser


class ToDoNote(models.Model):
    """
    Note model.
    """

    STATUS_PATTERN = [
        ("NS", "Нужно сделать"),
        ("ND", "В процессе"), 
        ("D", "Завершено")
    ]

    title = models.CharField(
        max_length=255,
        verbose_name='название',
        null=False
    )
    description = models.TextField(
        verbose_name='описание задачи'
    )
    status = models.CharField(
        max_length=100,
        verbose_name='статус',
        choices=STATUS_PATTERN,
        default="Нужно сделать"
    )
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    datetime_created = models.DateTimeField(
        auto_now=True,
        # default=timezone.now(),
        null=True,
        verbose_name='время создания'
    )

    class Meta:
        ordering = [
            '-id'
        ]
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional, Union, TypeVar

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

NullableDate = TypeVar('NullableDate', Union[str, None], datetime, date)


class Category(models.Model):
    """
    A class represents spending category
    Categories are organized to a forest:
        - Each Entry belongs only to one leaf category and all of its ancestors
        - Each Entry belongs only to one tree
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(
        max_length=25,
        unique=True
    )
    """Name of the category. Must be unique."""

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    """Parent of this category. Root categories has no parent."""

    _children = None

    _ancestors = None

    _ancestors_ids = None

    @property
    def children(self) -> QuerySet:
        """List of children of the category, order by name"""

        if self._children is None:
            self._children = Category.objects.filter(parent=self).order_by("name")
        return self._children

    @property
    def ancestors(self) -> List[Category]:
        """List of all ancestors of the category, order by increasing distance to this category"""

        if self._ancestors is None:
            self._ancestors = []
            category = self
            while category.parent is not None:
                self._ancestors.append(category.parent)
                category = category.parent
        return self._ancestors

    @property
    def ancestors_ids(self) -> List[int]:
        """List of all ancestors' ids"""

        if self._ancestors_ids is None:
            self._ancestors_ids = [cat.id for cat in self.ancestors]
        return self._ancestors_ids

    @property
    def is_leaf(self) -> bool:
        """Whether a category has no children"""

        return len(self.children) == 0

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Override save method to validate category before changes are made in DB"""

        if self.parent is not None and len(self.parent.ancestors) + 2 > settings.MODEL_CATEGORY_HIERARCHY_MAX_DEPTH:
            raise ValueError("MODEL_CATEGORY_HIERARCHY_MAX_DEPTH exceeded")
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def get_leaf_category(cls, category_id: int) -> Optional[Category]:
        """
        Return None if category_id is invalid or the category is not leaf
        Otherwise return the category with matching id
        """

        try:
            category = Category.objects.get(pk=category_id)
            if not category.is_leaf:
                raise ValueError
            return category
        except (ValueError, Category.DoesNotExist):
            return None

    @classmethod
    def get_root_categories(cls) -> QuerySet:
        """Return a list of all root categories in database, order by name"""

        return cls.objects.filter(parent__isnull=True).order_by("name")

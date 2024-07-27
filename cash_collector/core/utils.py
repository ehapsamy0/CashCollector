from django.shortcuts import _get_queryset
from rest_framework import exceptions


def api_get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an Http404 exception if the object
    does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        msg = f"First argument to get_object_or_404() must be a Model, Manager,  or QuerySet, not {klass__name}"  # noqa: E501
        raise ValueError(
            msg,
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as exc:
        raise exceptions.NotFound() from exc  # noqa: RSE102

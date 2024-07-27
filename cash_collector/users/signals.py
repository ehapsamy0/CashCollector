from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


@receiver(pre_save, sender=User)
def validate_manger_user(sender, instance, **kwargs):
    if instance.pk and instance.collectors.exists() and instance.manager is not None:
        from django.core.exceptions import ValidationError

        msg = "users_error_message_to_say_a_user_with_collector_cannot_be_assigned_to_another_manager"  # noqa: E501
        raise ValidationError(msg)

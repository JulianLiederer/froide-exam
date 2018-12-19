from datetime import datetime
from django.utils import timezone

from .models import ExamRequest, Subject, Curriculum
from .utils import REFERENCE_NAMESPACE


def connect_request_object(sender, **kwargs):
    reference = kwargs.get('reference')
    if not reference:
        return
    if not reference.startswith(REFERENCE_NAMESPACE):
        return
    try:
        namespace, curriculum_id, subject_id, year = reference.split(':', 3)
    except ValueError:
        return

    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        return

    try:
        curriculum = Curriculum.objects.get(pk=curriculum_id)
    except Subject.DoesNotExist:
        return

    try:
        year = int(year)
        if not curriculum.is_valid_year(year):
            return
    except ValueError:
        return

    year_date = timezone.make_aware(datetime(year, 1, 1))

    venue, _ = ExamRequest.objects.get_or_create(
        curriculum=curriculum,
        subject=subject,
        year=year_date,
        defaults={
            'timestamp': sender.first_message,
            'foirequest': sender,
        }
    )

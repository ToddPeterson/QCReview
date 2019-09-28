import datetime

from django.utils import timezone

from qc_review.models import QCRun, SuiteRun


def create_qcrun(cl, codeline, attempt=1):
    run = QCRun.objects.create(
        cl=cl,
        codeline=codeline,
        attempt=attempt
    )
    return run


def create_suite(run, name, passed, failed, errors, plat='win64', start=None, end=None):
    if start is None:
        start = timezone.now() + datetime.timedelta(minutes=-15)
    if end is None:
        end = timezone.now()

    suite = run.suiterun_set.create(
        suite_name=name,
        platform=plat,
        num_passed=passed,
        num_failed=failed,
        num_error=errors,
        start_time=start,
        end_time=end
    )
    return suite

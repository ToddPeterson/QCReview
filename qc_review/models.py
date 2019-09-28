from django.db import models


class QCRun(models.Model):
    cl = models.IntegerField('changelist')
    codeline = models.CharField(max_length=20)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    attempt = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.cl}_{self.attempt}'
    
    @property
    def elapsed_time(self):
        try:
            elapsed = self.end_time - self.start_time
        except TypeError:
            elapsed = 0
        return elapsed
    
    @property
    def ordered_suiterun_set(self):
        return self.suiterun_set.order_by('suite_name')
    
    def set_time_values_from_suiteruns(self, save=True):
        if self.start_time is None:
            start_times = [suite.start_time for suite in self.suiterun_set.all()]
            self.start_time = min(start_times)
        if self.end_time is None:
            end_times = [suite.end_time for suite in self.suiterun_set.all()]
            self.end_time = max(end_times)
        if save:
            self.save()
    
    def has_suite(self, suite_name):
        try:
            self.suiterun_set.get(suite_name=suite_name)
            return True
        except SuiteRun.DoesNotExist:
            return False


class SuiteRun(models.Model):
    WINDOWS10 = 'win10'
    WINDOWS7 = 'win7'
    LINUX_RHE71 = 'rhe71'
    PLATFORM_CHOICES = (
        (WINDOWS7, 'Windows 7'),
        (WINDOWS10, 'Windows 10'),
        (LINUX_RHE71, 'Linux RHEL 7.1')
    )

    suite_name = models.CharField(max_length=20)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    num_passed = models.IntegerField(default=0)
    num_error = models.IntegerField(default=0)
    num_failed = models.IntegerField(default=0)
    
    qc_run = models.ForeignKey(QCRun, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.suite_name}::{self.platform}'
    
    @property
    def elapsed_time(self):
        return self.end_time - self.start_time

    @property
    def last_clean_run(self):
        if self.num_failed == 0:
            return self
        suites = self.previous_suiteruns()

        for suite in suites:
            if suite.num_failed == 0:
                return suite
        return None

    @property
    def last_dirty_run(self):
        if self.num_failed != 0:
            return self
        suites = self.previous_suiteruns()

        for suite in suites:
            if suite.num_failed != 0:
                return suite
        return None

    def previous_suiteruns(self, count=None):
        runs = QCRun.objects.filter(
            codeline=self.qc_run.codeline,
            cl__lt=self.qc_run.cl
        ).order_by('-cl')
        runs = [run for run in runs if run.has_suite(self.suite_name)]
        if count:
            runs = runs[:count]
        suites = [run.suiterun_set.get(suite_name=self.suite_name) for run in runs]
        return suites

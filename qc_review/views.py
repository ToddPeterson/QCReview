from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View

from rest_framework.response import Response
from rest_framework.views import APIView

from . import config
from .forms import QCRunSelectForm
from .models import QCRun, SuiteRun


class SummaryView(View):
    def get(self, request):
        codeline = request.GET.get('codeline', config.DEFAULT_CODELINE)
        changelist = request.GET.get('changelist')

        runs = QCRun.objects.filter(codeline=codeline).order_by('-cl')
        cl_nums = [run.cl for run in runs]

        if changelist is None:
            run = runs.first()
        else:
            run = get_object_or_404(QCRun, codeline=codeline, cl=changelist)
    
        form = QCRunSelectForm()

        context = {
            'form': form,
            'run': run
        }
        return render(request, 'qc_review/summary.html', context)

    def post(self, request):
        form = QCRunSelectForm(request.POST)
        if form.is_valid():
            changelist = form.cleaned_data['changelist']
            codeline = form.cleaned_data['codeline']
        else:
            messages.error(request, 'Invalid data')
            return redirect('qc_review:index')

        run = get_object_or_404(QCRun, codeline=codeline, cl=changelist,
            attempt=1  # TODO add this to form
        )

        context = {
            'form': form,
            'run': run
        }
        return render(request, 'qc_review/summary.html', context)


class SuiteDetailView(DetailView):
    model = SuiteRun

    class Highlight:
        def __init__(self, title, message, style, icon):
            self.title = title
            self.message = message
            self.style = style
            self.icon = icon

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        suite = self.object

        #setup highlights
        highlights = []
        if suite.num_failed == 0:
            highlights.append(
                self.Highlight('Clean', '100% passed', 'success', 'fa-thumbs-up')
            )
            dirty_run = suite.last_dirty_run
            if dirty_run is not None:
                highlights.append(
                    self.Highlight('Clean Since', f'{dirty_run.qc_run.start_time.strftime("%d %b, %Y")}', 'info', 'fa-calendar-times')
                )
        else:
            highlights.append(
                self.Highlight('Failures', f'{suite.num_failed} tests failed', 'danger', 'fa-exclamation-circle')
            )
            clean_run = suite.last_clean_run
            if clean_run is not None:
                highlights.append(
                    self.Highlight('Last Clean Run', f'{clean_run.qc_run.cl}', 'info', 'fa-calendar-check')
                )
        
        previous_suites = suite.previous_suiteruns(1)
        if previous_suites:
            previous_suite = previous_suites[0]
            if suite.elapsed_time and previous_suite.elapsed_time:
                elapsed_time_ratio = suite.elapsed_time / previous_suite.elapsed_time
                if elapsed_time_ratio > 1.1:
                    highlights.append(
                        self.Highlight('Elapsed Time', '{:.0%} previous run'.format(elapsed_time_ratio), 'warning', 'fa-stopwatch')
                    )
                elif elapsed_time_ratio < 0.9:
                    highlights.append(
                        self.Highlight('Elapsed Time', '{:.0%} previous run'.format(elapsed_time_ratio), 'info', 'fa-stopwatch')
                    )

        context['highlights'] = highlights

        return context


class SuiteDetailData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # suite_name = 'adamspy'
        suite_id = request.GET.get('id')
        suite = SuiteRun.objects.get(pk=suite_id)
        suite_name = suite.suite_name

        all_runs = QCRun.objects.filter(codeline='ADAMSDEV').order_by('cl')
        runs = [run for run in all_runs if run.has_suite(suite_name)][5:]
        suites = [run.suiterun_set.get(suite_name=suite_name) for run in runs]

        elapsed_labels = [f'{run.cl}_{run.attempt}' for run in runs]
        elapsed_data = [suite.elapsed_time for suite in suites]

        hist_labels = elapsed_labels
        hist_pass_data = [suite.num_passed for suite in suites]
        hist_fail_data = [suite.num_failed for suite in suites]

        pf_labels = ["Passed", "Failed", "Error"]
        pf_data = [suite.num_passed, suite.num_failed, suite.num_error]

        data = {
            "elapsed_labels": elapsed_labels,
            "elapsed_data": elapsed_data,
            "hist_labels": hist_labels,
            "hist_pass_data": hist_pass_data,
            "hist_fail_data": hist_fail_data,
            "pf_labels": pf_labels,
            "pf_data": pf_data,
        }
        return Response(data)


class QCRunDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        runs = QCRun.objects.order_by('-cl').all()

        if request.GET.get('codeline'):
            runs = runs.filter(codeline=request.GET['codeline'])

        run_ids = [run.id for run in runs]
        cl_nums = [run.cl for run in runs]
        data = {
            "run_ids": run_ids,
            "cl_nums": cl_nums
        }
        return Response(data)

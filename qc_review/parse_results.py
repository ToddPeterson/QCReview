import os
import glob
import datetime

from django.utils.timezone import make_aware

from . import config
from .models import QCRun, SuiteRun

def main():
    codelines = [
        'ADAMSDEV',
        'ADAMSDEV2'
    ]

    platform = 'win64_win10'

    for codeline in codelines:
        base_dir = os.path.join(config.QA_DATA_DIR, codeline, 'qa', 'cloud', platform)
        if not os.path.exists(base_dir):
            raise Exception(f'{base_dir} does not exist')
        cl_dirs = [dir for dir in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, dir))]
        for cl_dir in cl_dirs:
            changelist, attempt = cl_dir.split('_')
            try:
                QCRun.objects.get(codeline=codeline, cl=changelist, attempt=attempt)
            except QCRun.DoesNotExist:
                parse_run(codeline, changelist, attempt)


def parse_run(codeline, changelist, attempt, platform='win64_win10'):
    print(f'Started parsing {codeline} {changelist}_{attempt}')

    base_dir = os.path.join(config.QA_DATA_DIR, codeline, 'qa', 'cloud', platform, f'{changelist}_{attempt}')
    if not os.path.exists(base_dir):
        raise Exception(f'{base_dir} does not exist')

    try:
        run = QCRun.objects.get(codeline=codeline, cl=changelist, attempt=attempt)
    except QCRun.DoesNotExist:
        run = QCRun(codeline=codeline, cl=changelist, attempt=attempt)

    run.save()

    testrun_dirs = glob.glob(base_dir + '/C2RG*/testrun')
    for testruns in testrun_dirs:
        for suite_dir in os.listdir(testruns):
            if not os.path.isdir(os.path.join(testruns, suite_dir)):
                continue
            suite_name = suite_dir
            suite_home = os.path.join(
                testruns,
                suite_dir,
                f'{codeline}_CL{changelist}',
                platform.split('_')[0],
                'prod'
            )

            regsum_paths = []
            regsum_path = os.path.join(suite_home, 'REGSUM.log')

            if os.path.exists(regsum_path):
                regsum_paths.append((suite_name, regsum_path))
            else:
                for subsuite_dir in os.listdir(suite_home):
                    if not os.path.isdir(os.path.join(suite_home, subsuite_dir)):
                        continue
                    regsum_path = os.path.join(suite_home, subsuite_dir, 'REGSUM.log')
                    subsuite_name = f'{suite_name}_{subsuite_dir}'
                    regsum_paths.append((subsuite_name, regsum_path))

            for name, path in regsum_paths:
                regsum_data = parse_regsum(path)
                create_suiterun(run, name, regsum_data)
                print(f'Parsed suite data for {name}')
    
    run.set_time_values_from_suiteruns()


def parse_regsum(regsum_path):
    keep_data_labels = [
        'Started',
        'Finished',
        'Codeline',
        'Changelist',
        'Host',
        'Errors',
        'Regressions',
        'Failures',
        'Comparisons',
        'Platform'
    ]

    # print(f'{regsum_path} exists: {os.path.exists(regsum_path)}')

    regsum_data = {}
    with open(regsum_path, 'r') as regsum:
        for line in regsum.readlines():
            for label in keep_data_labels:
                if f'{label}:' in line:
                    regsum_data[label] = line.split(':', 1)[1].strip()
    
    if 'Started' in regsum_data:
        datetime_string = regsum_data['Started']
        datetime_string = datetime_string.split(' on ')[0].strip()
        datetime_string = format_datetime(datetime_string)
        regsum_data['Started'] = datetime_string
    if 'Finished' in regsum_data:
        datetime_string = regsum_data['Finished']
        datetime_string = datetime_string.split(' on ')[0].strip()
        datetime_string = format_datetime(datetime_string)
        regsum_data['Finished'] = datetime_string
    if 'Comparisons' in regsum_data:
        comparisons = regsum_data['Comparisons']
        comparisons = comparisons.split()[0]
        regsum_data['Comparisons'] = comparisons
    if 'Platform' in regsum_data:
        plat = regsum_data['Platform']
        plat = plat.split()[0]
        if '_' in plat:
            plat = plat.split('_')[1]
        regsum_data['Platform'] = plat

    # print(regsum_data)
    return regsum_data


def create_suiterun(run, suite_name, data):
    num_passed = int(data['Comparisons']) - int(data['Regressions'])
    if 'Errors' in data:
        errors = int(data['Errors'])
        num_passed -= errors
    else:
        errors = 0
    run.suiterun_set.create(
        suite_name=suite_name,
        platform=data['Platform'],
        start_time=data['Started'],
        end_time=data['Finished'],
        num_passed=num_passed,
        num_failed=data['Regressions'],
        num_error=errors
    )


def format_datetime(datetime_string):
    """Convert datetime_string from regsum to a timezone aware datetime object
    MM/DD/YYYY HH:MM:SS -> datetime
    """
    try:
        naive_datetime = datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M')
    except ValueError:
        naive_datetime = datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S')

    aware_datetime = make_aware(naive_datetime)

    return aware_datetime


if __name__ == '__main__':
    codeline = 'ADAMSDEV'
    changelist = '673885_1'
    platform = 'win64_win10'
    main(codeline, changelist, platform)

DEFAULT_CODELINE = 'ADAMSDEV'

# Used by QCRun. Shortened version must be <= 3 characters.
CODELINE_CHOICES = (
    ('ADAMSDEV', 'AD'),
    ('ADAMSDEV2', 'AD2'),
    ('CDEDEV', 'CDE'),
    ('VPGDEV', 'VD'),
    ('VPGDEV2', 'VD2')
)

CODELINE_LIST = [item[0] for item in CODELINE_CHOICES]

QA_DATA_DIR = r"\\na\devl\breqadata\Adams"


import sys
from pathlib import Path

import pandas as pd
import pytest

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))


@pytest.fixture
def raw_csv_portfolio(request):
    return project_dir / 'tests' / 'csv' / request.param


@pytest.fixture
def raw_csv_allocation(request):
    return project_dir / 'tests' / 'csv' / request.param


@pytest.fixture
def df_expected_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)


@pytest.fixture
def df_working_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)

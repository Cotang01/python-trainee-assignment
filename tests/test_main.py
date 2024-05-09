from logging import getLogger
from aiohttp import ClientResponseError
import pytest
from matrix_traversal.main import get_matrix, parse_matrix, \
    traverse_matrix_cntrclckwse, eject_data_from_url

pytest_plugins = (
    'pytest_asyncio',
)

# Parameters for test_parse_matrix_correct
parse_matrix_success_test_cases = [(
    '+-----+-----+-----+-----+\n'
    '|  10 |  20 |  30 |  40 |\n'
    '+-----+-----+-----+-----+\n'
    '|  50 |  60 |  70 |  80 |\n'
    '+-----+-----+-----+-----+\n'
    '|  90 | 100 | 110 | 120 |\n'
    '+-----+-----+-----+-----+\n'
    '| 130 | 140 | 150 | 160 |\n'
    '+-----+-----+-----+-----+\n',
    [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160]
    ]),
    (
        '| 10 | 20 |\n'
        '| 30 | 40 |',

        [
            [10, 20],
            [30, 40]
        ]
    )]

# Parameters for test_parse_matrix_failure
parse_matrix_failure_test_cases = [
    '+----+----+----+----+\n'
    '  10   20   30   40 \n'
    '+----+----+----+----+\n'
    '  50   60   70   80 \n'
    '+----+----+----+----+\n'
    '  90  100  110  120 \n'
    '+----+----+----+----+\n'
    ' 130  140  150  160 \n'
    '+----+----+----+----+\n',

    ' 10  20 \n'
    ' 30  40 '
]

# Parameters for test_traverse_matrix_cntrclckwse
traverse_matrix_cntrclckwse_test_cases = [(
    [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160]
    ],
    [
        10, 50, 90, 130,
        140, 150, 160, 120,
        80, 40, 30, 20,
        60, 100, 110, 70
    ])
]


@pytest.fixture
def url_with_matrix():
    return 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'


@pytest.fixture
def logger():
    yield getLogger(__name__)


@pytest.mark.asyncio
async def test_eject_data_from_url_success(url_with_matrix):
    assert await eject_data_from_url(url_with_matrix) == \
           '+-----+-----+-----+-----+\n' \
           '|  10 |  20 |  30 |  40 |\n' \
           '+-----+-----+-----+-----+\n' \
           '|  50 |  60 |  70 |  80 |\n' \
           '+-----+-----+-----+-----+\n' \
           '|  90 | 100 | 110 | 120 |\n' \
           '+-----+-----+-----+-----+\n' \
           '| 130 | 140 | 150 | 160 |\n' \
           '+-----+-----+-----+-----+\n'


@pytest.mark.asyncio
async def test_eject_data_from_url_5xx_error():
    with pytest.raises(ClientResponseError):
        await eject_data_from_url('https://httpstat.us/500')


@pytest.mark.asyncio
async def test_eject_data_from_url_4xx_error():
    with pytest.raises(ClientResponseError):
        await eject_data_from_url('https://httpstat.us/404')


@pytest.mark.asyncio
@pytest.mark.parametrize('text, result', parse_matrix_success_test_cases)
async def test_parse_matrix_success(text, result):
    assert await parse_matrix(text) == result


@pytest.mark.asyncio
@pytest.mark.parametrize('text', parse_matrix_failure_test_cases)
async def test_parse_matrix_success(text):
    with pytest.raises(ValueError):
        assert await parse_matrix(text)


@pytest.mark.asyncio
@pytest.mark.parametrize('matrix, expected', traverse_matrix_cntrclckwse_test_cases)
async def test_traverse_matrix_cntrclckwse_success(matrix, expected):
    assert await traverse_matrix_cntrclckwse(matrix) == expected


@pytest.mark.asyncio
async def test_get_matrix_success(url_with_matrix, logger):
    assert await get_matrix(url_with_matrix, logger) == \
           [
               10, 50, 90, 130,
               140, 150, 160, 120,
               80, 40, 30, 20,
               60, 100, 110, 70
           ]

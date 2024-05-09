from typing import List
import asyncio
import aiohttp
from logging import getLogger, Logger

"""Matrix traverse constants"""
directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
dir_count: int = 4

"""Request constants"""
TIMEOUT_SECONDS = 15


async def get_matrix(url: str, logger_=None) -> List[int]:
    """This function gets text that contains matrix from URL and returns
    traversal list of matrix numbers in counterclockwise direction starting
    from top left corner."""
    if logger_ is None or not isinstance(logger_, Logger):
        logger_ = getLogger(__name__)
    try:
        source_content = await eject_data_from_url(url)
        matrix = await parse_matrix(source_content)
        return await traverse_matrix_cntrclckwse(matrix)
    except (aiohttp.ClientResponseError,
            aiohttp.ClientTimeout,
            aiohttp.ServerTimeoutError,
            ValueError,
            TypeError) as e:
        logger_.error(f'{e}')
    except AssertionError:
        logger_.error(f'Transfer protocol of "{url}" is invalid.')


async def eject_data_from_url(url: str) -> str:
    """Function that makes async GET method to url source and returns
    plain text from response."""
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
                if text is None:
                    raise ValueError(f'Ejected data from "{url}" is empty.')
                return text
    except (aiohttp.ClientResponseError,
            aiohttp.ClientTimeout,
            aiohttp.ServerTimeoutError):
        raise


async def parse_matrix(matrix_text: str) -> List[List[int]]:
    """Function that parses text content and returns matrix to work with."""
    res = []
    buf = []
    for el in matrix_text.split('|'):
        if el.strip().isdigit():
            buf.append(int(el))
        else:
            if buf:
                res.append(buf)
            buf = []
    if not res:
        raise ValueError(f'Could not parse matrix from text: "{matrix_text}".')
    return res


async def traverse_matrix_cntrclckwse(matrix: List[List[int]]) \
        -> List[int]:
    # Time: O(m * n) Space: O(m * n)
    """Function that traverses matrix in counterclockwise direction starting
    from top left corner and returns traverse result as list with ints."""
    res = []
    m = len(matrix)
    n = len(matrix[0])
    m_buf = m - 1
    n_buf = n - 1
    dir_ptr = 0  # Pointer for starting direction in directions
    border_dif = abs(m - n)
    cur_pos = (0, 0)  # Traverse starting point before incrementing
    coord_len = 2
    steps_lengths = [m_buf, n_buf, m_buf]
    """ ^ Lengths of each straight way before direction change.
    For counterclockwise direction we need to do:
    1. m - 1 steps down
    2. n - 1 steps right
    3. m - 1 steps up
    and then we need decremented by 1 both m and n values until any of m or n
    becomes less than size difference between m and n (border dif) and each 
    of values are gonna be our next path lengths before direction changes.
    This works with square-shaped and rectangle-shaped matrix."""

    while m_buf >= border_dif and n_buf >= border_dif:
        n_buf -= 1
        m_buf -= 1
        if n_buf >= border_dif:
            steps_lengths.append(n_buf)
        if m_buf >= border_dif:
            steps_lengths.append(m_buf)

    res.append(matrix[cur_pos[0]][cur_pos[1]])
    for length in steps_lengths:
        for _ in range(length):
            cur_pos = tuple(cur_pos[i] + directions[dir_ptr][i]
                            for i in range(coord_len))
            res.append(matrix[cur_pos[0]][cur_pos[1]])
        dir_ptr = (dir_ptr + 1) % dir_count

    return res


if __name__ == '__main__':
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('matrix_traversal_debug.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    url_ = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
    # url_ = 'https://httpstat.us/404'
    res = asyncio.run(get_matrix(url_, logger))
    print(res)
    logger.info(f'Got "{res}" from "{url_}"')

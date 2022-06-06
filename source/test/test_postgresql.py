from unittest.mock import patch

from source.core import postgres


def test_update():
    expected = 'Update query has finished.'

    with patch('psycopg2.connect') as mock_connect:
        mock_con_cm = mock_connect.return_value
        mock_con = mock_con_cm.__enter__.return_value
        mock_cur = mock_con.cursor.return_value
        mock_cur.fetchall.return_value = expected

        result = postgres.update_table('table_name', 'column_name')
        assert expected == result

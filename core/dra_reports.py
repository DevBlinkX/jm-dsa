from django.utils import timezone
import xlsxwriter
from xlsxwriter.worksheet import (Worksheet, cell_number_tuple, cell_string_tuple)
from typing import Optional
import io
import logging
import datetime
logger = logging.getLogger(__name__)



def get_column_width(worksheet: Worksheet, column: int) -> Optional[int]:
    """Get the max column width in a `Worksheet` column."""
    strings = getattr(worksheet, '_ts_all_strings', None)
    if strings is None:
        strings = worksheet._ts_all_strings = sorted(
            worksheet.str_table.string_table,
            key=worksheet.str_table.string_table.__getitem__)
    lengths = set()
    for row_id, colums_dict in worksheet.table.items():  # type: int, dict
        data = colums_dict.get(column)
        if not data:
            continue
        if type(data) is cell_string_tuple:
            iter_length = len(strings[data.string])
            if not iter_length:
                continue
            lengths.add(iter_length)
            continue
        if type(data) is cell_number_tuple:
            iter_length = len(str(data.number))
            if not iter_length:
                continue
            lengths.add(iter_length)
    if not lengths:
        return None
    return max(lengths)


def set_column_autowidth(worksheet: Worksheet, column: int):
    """
    Set the width automatically on a column in the `Worksheet`.
    !!! Make sure you run this function AFTER having all cells filled in
    the worksheet!
    """
    try:
        maxwidth = get_column_width(worksheet=worksheet, column=column)
        if maxwidth is None:
            return
        worksheet.set_column(first_col=column, last_col=column, width=maxwidth)
    except Exception as e:
        return


def set_col_width(worksheet: Worksheet, col_width=None):
    try:
        if col_width:
            for k, v in col_width.items():
                worksheet.set_column(first_col=k, last_col=k, width=v)
    except Exception as e:
        return


def added_user_section(worksheet_s: Worksheet, user, row, cell_center, header):
    try:
        on_time = datetime.datetime.now().strftime("%c")
        worksheet_s.write(row, 0, 'Downloaded By', header)
        worksheet_s.write(row, 1,  user.name, cell_center)
        row += 1
        worksheet_s.write(row, 0, 'On', header)
        worksheet_s.write(row, 1,  on_time, cell_center)
        row += 2
        return row
    except Exception as e:
        logger.exception(e)
        return row

def get_workbook(worksheet_name="custom_report", in_memory=True):
    output = io.BytesIO()
    if not in_memory:
        output = f"{worksheet_name}.xlsx"

    workbook = xlsxwriter.Workbook(output, {'in_memory': in_memory})
    worksheet_s = workbook.add_worksheet(worksheet_name)

    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })

    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1,
        'bold': True
    })

    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1,
        'text_wrap': True
    })

    cell_left = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'border': 1
    })

    return output, workbook, worksheet_s, title, header, cell_center, cell_left


def get_report_data(reports_data, in_memory=True, **kwargs):
    sheet_name = kwargs.get('sheet_name')
    output, workbook, worksheet_s, title, header, cell_center, cell_left = get_workbook(worksheet_name=sheet_name, in_memory=in_memory)
    worksheet_s.write(0, 0, reports_data.get('y_header', 'S. NO.'), header)
    row = 0
    user = kwargs.get('user')
    on_time = datetime.datetime.now().strftime("%c")

    # user name
    if user:
        row = added_user_section(worksheet_s, user, row, cell_center, header)
        row += 2

    xid = 0
    col = 0

    for x in reports_data.get('headers'):
        worksheet_s.write(row, xid, x, header)
        xid += 1

    for val  in reports_data.get('data'):
        row += 1
        col = 0
        # worksheet_s.write_number(row, col, row, header)
        for k in reports_data.get('headers'):
            worksheet_s.write(row, col, val.get(k, 'NA'), cell_center)
            col = col+1

    for i in range(0,col):
        set_column_autowidth(worksheet_s, i)
    set_col_width(worksheet_s, {0:20})

    workbook.close()
    if in_memory:
        output.seek(0)
    return output

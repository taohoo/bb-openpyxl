# -*- coding: utf-8 -*-
"""
@author: hubo
@project: bb-py
@file: insert.py
@time: 2023/12/22 14:13
@desc:
关于公式和宏，应该python代码代替复杂的公式和宏。目前支持当个sheet页内的公式迁移，跨sheet页的公式迁移会出错，可以通过公式名称管理一定程度上解决跨sheet页的公式问题
从excel使用角度：
    插入或者删除行或者列的时候，受影响的有公式、合并的单元格、列宽、行高、数据格式、数据验证、图表、宏代码
    其中宏代码不考虑。
    已经处理：公式、合并的单元格、列宽、行高
    待验证：数据格式、数据验证、图表、宏代码
从代码角度：
    已经处理：merged_cells
    未处理完整：row_dimensions，column_dimensions
    待处理：col_breaks, row_breaks, data_validations
    待验证： scenarios
    暂不处理：宏，defined_names，跨sheet页
"""
from ._insert import (_un_merge_cells_before_insert, _re_merge_cells_when_after_insert,
                      _get_all_columns_width, _get_all_rows_height, _reset_all_columns_width, _reset_all_rows_height,
                      _re_set_all_formulas, _warning_unsupported_formula)


def insert_rows(worksheet, idx, amount=1):
    """
    插入一行，同时保持原来的合并单元格，公式，行高
    :param worksheet: worksheet
    :param idx: 同Worksheet.insert_rows
    :param amount:同Worksheet.insert_rows
    :return:
    """
    unmerged_ranges = _un_merge_cells_before_insert(worksheet, row_idx=idx, amount=amount)
    heights = _get_all_rows_height(worksheet)
    if amount > 0:
        worksheet.insert_rows(idx, amount=amount)
    else:
        worksheet.delete_rows(idx, amount=-amount)
    _re_set_all_formulas(worksheet, row_idx=idx, amount=amount)
    _warning_unsupported_formula(worksheet.parent)
    _reset_all_rows_height(worksheet, heights, idx, amount=amount)
    _re_merge_cells_when_after_insert(worksheet, unmerged_ranges, row_idx=idx, amount=amount)


def insert_cols(worksheet, idx, amount=1):
    """
    插入一列，同时保持原来的合并单元格，公式，列宽
    :param worksheet:
    :param idx:同Worksheet.insert_rows
    :param amount:同Worksheet.insert_rows
    :return:
    """
    unmerged_ranges = _un_merge_cells_before_insert(worksheet, col_idx=idx, amount=amount)
    widths = _get_all_columns_width(worksheet)
    if amount > 0:  # 插入列
        worksheet.insert_cols(idx, amount=amount)
    else:   # 删除列
        worksheet.delete_cols(idx, amount=-amount)
    _re_set_all_formulas(worksheet, col_idx=idx, amount=amount)
    _warning_unsupported_formula(worksheet.parent)
    _reset_all_columns_width(worksheet, widths, idx, amount=amount)
    _re_merge_cells_when_after_insert(worksheet, unmerged_ranges, col_idx=idx, amount=amount)

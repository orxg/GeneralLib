#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-18 14:37:17
# @Author  : Li Hao (howardlee_h@outlook.com)
# @Link    : https://github.com/SAmmer0
# @Version : $Id$

'''
由基础数据计算而来的衍生因子

__version__ = 1.0.0
修改日期：2017-07-27
修改内容：
    初始化
'''
import pdb
import datatoolkits
import dateshandle
import numpy as np
import pandas as pd
from .utils import Factor, check_indexorder, check_duplicate_factorname, convert_data
from .query import query

# --------------------------------------------------------------------------------------------------
# 常量和功能函数
NAME = 'derivativefactors'


def get_factor_dict():
    res = dict()
    for f in factor_list:
        res[f.name] = {'rel_path': NAME + '\\' + f.name, 'factor': f}
    return res


# --------------------------------------------------------------------------------------------------
# 价值类因子
# EP_TTM
def get_ep(universe, start_time, end_time):
    '''
    EP为净利润与总市值的比
    '''
    ni_data = query('NI_TTM', (start_time, end_time))
    tmktv_data = query('TOTAL_MKTVALUE', (start_time, end_time))
    ep = ni_data / tmktv_data
    ep = ep.loc[:, sorted(universe)]
    assert check_indexorder(ep), 'Error, data order is mixed!'
    return ep


ep_ttm = Factor('EP_TTM', get_ep, pd.to_datetime('2017-07-27'),
                dependency=['NI_TTM', 'TOTAL_MKTVALUE'], desc='净利润/总市值计算得到')

# BP_TTM


def get_bp(universe, start_time, end_time):
    '''
    BP为归属母公司权益/总市值
    '''
    bv_data = query('EQUITY', (start_time, end_time))
    tmktv_data = query('TOTAL_MKTVALUE', (start_time, end_time))
    bp = bv_data / tmktv_data
    bp = bp.loc[:, sorted(universe)]
    assert check_indexorder(bp), 'Error, data order is mixed!'
    return bp


bp = Factor('BP', get_bp, pd.to_datetime('2017-07-27'),
            dependency=['EQUITY', 'TOTAL_MKTVALUE'], desc='最新的归属母公司权益/总市值')

# SP_TTM


def get_sp(universe, start_time, end_time):
    '''
    SP为营业收入与总市值的比
    '''
    sale_data = query('OPREV_TTM', (start_time, end_time))
    tmktv_data = query('TOTAL_MKTVALUE', (start_time, end_time))
    sp = sale_data / tmktv_data
    sp = sp.loc[:, sorted(universe)]
    assert check_indexorder(sp), 'Error, data order is mixed!'
    return sp


sp_ttm = Factor('SP_TTM', get_sp, pd.to_datetime('2017-07-27'),
                dependency=['OPREV_TTM', 'TOTAL_MKTVALUE'], desc='营业收入/总市值')

# CFP_TTM


def get_cfp(universe, start_time, end_time):
    '''
    CFP为经营活动产生的现金流量净额/总市值
    '''
    cf_data = query('OPNETCF_TTM', (start_time, end_time))
    tmktv_data = query('TOTAL_MKTVALUE', (start_time, end_time))
    cfp = cf_data / tmktv_data
    cfp = cfp.loc[:, sorted(universe)]
    assert check_indexorder(cfp), 'Error, data order is mixed!'
    return cfp


cfp_ttm = Factor('CFP_TTM', get_cfp, pd.to_datetime('2017-07-27'),
                 dependency=['OPNETCF_TTM', 'TOTAL_MKTVALUE'], desc='经营活动中现金流净额/总市值')

# SALE2EV


def get_sale2ev(universe, start_time, end_time):
    '''
    SALE2EV = 营业收入/(总市值+非流动负债合计-货币资金)
    '''
    sale_data = query('OPREV_TTM', (start_time, end_time), fillna=0)
    tmktv_data = query('TOTAL_MKTVALUE', (start_time, end_time), fillna=0)
    ncdebt_data = query('TNCL', (start_time, end_time), fillna=0)
    cash_data = query('CASH', (start_time, end_time), fillna=0)
    data = sale_data / (tmktv_data + ncdebt_data - cash_data)
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data


sale2ev = Factor('SALE2EV', get_sale2ev, pd.to_datetime('2017-07-27'),
                 dependency=['OPREV_TTM', 'TOTAL_MKTVALUE', 'TNCL', 'CASH'],
                 desc='营业收入/(总市值+非流动负债合计-货币资金)')
# --------------------------------------------------------------------------------------------------
# 成长类因子
# 单季度营业收入同比增长


def get_oprev_yoy(universe, start_time, end_time):
    '''
    OPREV_YOY = (本季度营业收入-上年同季度营业收入)/abs(上年同季度营业收入)
    '''
    oprev_lq = query('OPREV_1S', (start_time, end_time))
    oprev_lyq = query('OPREV_5S', (start_time, end_time))
    data = (oprev_lq - oprev_lyq) / np.abs(oprev_lyq) - 1
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data


oprev_yoy = Factor('OPREV_YOY', get_oprev_yoy, pd.to_datetime('2017-07-27'),
                   dependency=['OPREV_1S', 'OPREV_5S'],
                   desc='(本季度营业收入-上年同季度营业收入)/abs(上年同季度营业收入)')
# 单季度净利润同比增长


def get_ni_yoy(universe, start_time, end_time):
    '''
    NI_YOY = (本季度净利润-上年同季度净利润)/abs(上年同季度净利润)
    '''
    ni_lq = query('NI_1S', (start_time, end_time))
    ni_lyq = query('NI_5S', (start_time, end_time))
    data = (ni_lq - ni_lyq) / np.abs(ni_lyq) - 1
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data


ni_yoy = Factor('NI_YOY', get_ni_yoy, pd.to_datetime('2017-07-27'),
                dependency=['NI_1S', 'NI_5S'],
                desc='(本季度净利润-上年同季度净利润)/abs(上年同季度净利润)')

# 过去5年增长率


def get_p5ygrowth(factor_type):
    '''
    母函数，用于生成计算过去五年平均增长率的函数

    Parameter
    ---------
    factor_type: str
        因子类型，目前只支持['NI', 'OPREV']

    Notes
    -----
    采用将对应数值对时间做回归（时间由远到近依次为1到5），然后除以平均值的绝对值
    '''
    def calc_growth(df):
        # 假设数据按照升序排列，即由上到下依次为1-5
        t = np.arange(5, 0, -1)
        df_mean = df.mean()
        df_demean = df - df_mean
        res = np.dot(t, df_demean.values) / 10
        res = pd.Series(res, index=df.columns)
        res = res / np.abs(df_mean)
        return res

    def _inner(universe, start_time, end_time):
        datas = list()
        for i in range(1, 6):
            tmp_data = query(factor_type + '_%dY' % i, (start_time, end_time))
            datas.append(tmp_data)
        data = convert_data(datas, range(1, 6))  # 1（最近年度）-5（最远年度）依次表示到现在的时间间隔越来越远
        data = data.sort_index()
        by_date = data.groupby(level=0)
        data = by_date.apply(calc_growth)
        data = data.loc[:, sorted(universe)]
        assert check_indexorder(data), 'Error, data order is mixed!'
        return data
    return _inner


# 净利润过去5年增长率
ni_5yg = Factor('NI_5YG', get_p5ygrowth('NI'), pd.to_datetime('2017-07-28'),
                dependency=['NI_%dY' % i for i in range(1, 6)])
# 营业收入过去5年增长率
oprev_5yg = Factor('OPREV_5YG', get_p5ygrowth('OPREV'), pd.to_datetime('2017-07-28'),
                   dependency=['OPREV_%dY' % i for i in range(1, 6)])

# --------------------------------------------------------------------------------------------------
# 质量类因子
# ROE


def get_roe(universe, start_time, end_time):
    '''
    ROE = 净利润TTM / 归属母公司权益
    '''
    ni_data = query('NI_TTM', (start_time, end_time))
    equity_data = query('EQUITY', (start_time, end_time))
    data = ni_data / equity_data
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data


roe = Factor('ROE', get_roe, pd.to_datetime('2017-07-28'),
             dependency=['NI_TTM', 'EQUITY'], desc='净利润TTM/归属母公司权益')
# ROA


def get_roa(universe, start_time, end_time):
    '''
    ROA = 净利润TTM / 总资产
    '''
    ni_data = query('NI_TTM', (start_time, end_time))
    ta_data = query('TA', (start_time, end_time))
    data = ni_data / ta_data
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data


roa = Factor('ROA', get_roa, pd.to_datetime('2017-07-28'),
             dependency=['NI_TTM', 'TA'], desc='净利润TTM/总资产')

# 营业利润率


def get_grossmargin(universe, start_time, end_time):
    '''
    营业利润率 = (营业收入-营业成本-销售费用-管理费用-财务费用) / abs(营业收入)
    '''
    oprev = query('OPREV_TTM', (start_time, end_time))
    opcost = query('OPCOST_TTM', (start_time, end_time))
    opsale = query('OPEXP_TTM', (start_time, end_time))
    adminexp = query('ADMINEXP_TTM', (start_time, end_time))
    fiexp = query('FIEXP_TTM', (start_time, end_time))
    data = (oprev - opcost - opsale - adminexp - fiexp) / np.abs(oprev)
    data = data.loc[:, sorted(universe)]
    assert check_indexorder(data), 'Error, data order is mixed!'
    return data

gross_margin = Factor('GROSS_MARGIN', get_grossmargin, pd.to_datetime('2017-07-28'),
                      dependency=['OPREV_TTM', 'OPCOST_TTM', 'OPEXP_TTM', 'ADMINEXP_TTM',
                                  'FIEXP_TTM'],
                      desc='营业利润率 = (营业收入-营业成本-销售费用-管理费用-财务费用) / abs(营业收入)')
# --------------------------------------------------------------------------------------------------

factor_list = [ep_ttm, bp, sp_ttm, cfp_ttm, sale2ev, oprev_yoy, ni_yoy, ni_5yg, oprev_5yg,
               roe, roa, gross_margin]
check_duplicate_factorname(factor_list, __name__)

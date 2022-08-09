import time
import traceback
from datetime import date, datetime
from os import name

import requests
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import *
from requests.adapters import HTTPAdapter

'''
这里的代码是用来爬取数据并提取出所需要的字段数据，因隐私原因，仅供参考学习。这个模块是被main引用的哟！
'''

# 登录状态
def 检查登录状态(name):
    url = 'http://api.smart-insight-service.com:40423/case_data_batch?a=paginate&query=&page_count=6&_=1638612090870'
    headers = {
        'Accept':
        'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9',
        'Authorization':
        '',
        'Connection':
        'keep-alive',
        'Host':
        'api.smart-insight-service.com:40423',
        'Origin':
        'http://saas.smart-insight-service.com:40423',
        'Referer':
        'http://saas.smart-insight-service.com:40423/case/case_search/detail.html',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    while True:
        try:
            with open('账号信息.txt', encoding='utf-8') as f:
                au = f.readline()
                di = eval(au)
                # print(au)
        except:
            di = {}
            au = input('无此账号，正在注册，请按F12，找到身份识别信息复制过来', type=TEXT, placeholder='这个身份识别信息有点复杂', help_text='不懂的问管理员哦', required=True)
            di[name] = au
            di = str(di)
            with open('账号信息.txt', 'w', encoding='utf-8') as f:
                f.write(di)

        headers['Authorization'] = di.get(name)

        try:
            req = requests.get(url=url, headers=headers)
            r = req.json()
            # put_text('正在检查登录状态.....')
            返回状态 = r.get('msg')
            put_text(返回状态)
        except:
            put_text('获取失败,请检查网址或网络!')

        if 返回状态 == '请求成功':
            break
        else:
            au = input('无此账号或账号登录状态已失效，请选择所属团队，按F12找到身份识别信息并复制过来', type=TEXT, placeholder='每次退出登录或者关闭浏览器都需要重新添加的', help_text='不懂的问管理员哦', required=True)
            di[name] = au
            di = str(di)
            with open('账号信息.txt', 'w', encoding='utf-8') as f:
                f.write(di)
    return headers

def 更改登录团队():
    账号 = input('请重新输入你的系统帐号登录😊', type=TEXT, placeholder='是系统的账号哟😀', help_text='切换到所需要的团队', required=True)
    
    with open('账号信息.txt', encoding='utf-8') as f:
        au = f.readline()
        di = eval(au)

    au = input('请选择所属团队，按F12找到身份识别信息并复制过来', type=TEXT, placeholder='重新输入所属团队的身份标识', help_text='', required=True)
    di[账号] = au
    di = str(di)
    with open('账号信息.txt', 'w', encoding='utf-8') as f:
        f.write(di)

    检查登录状态(账号)

# 获取网址
def 身份证号查询网址(身份证号, 案件数=10, 页数=1):
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=paginate&cur_page={页数}&page_count={案件数}&id_no={身份证号}&_=1632296854055'
    return url

def 案件号查询网址(案件号):
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=paginate&no={案件号}&_=1635560354271'
    return url

def 批次号查询网址(批次号, 案件数=10, 页数=1):
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=paginate&cur_page={页数}&page_count={案件数}&batch_no={批次号}&_=1637329954374'
    return url

def 批次号回传查询网址(批次号, 回传状态, 案件数=10, 页数=1):
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=paginate&cur_page={页数}&page_count={案件数}&batch_no={批次号}&send_status={回传状态}&_=1635821545417'
    return url

def 列表页理算结果查询网址(案件号):
    url = f'http://api.smart-insight-service.com:40423/case_adjuster_result?a=duty_result_detail&case_no={案件号}&_=1632296854056'
    return url

def 列表页理算结果详情页面查询网址(案件id):
    url = f'http://api.smart-insight-service.com:40423/case_adjuster_result?a=detail&result_id=0&case_id={案件id}&_=1641733395628'
    return url

def 案件详情查询网址(案件id):
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=detail&medical_id=0&case_id={案件id}&_=1638670784300'
    return url

def 案件详情页领款人与受益人网址(案件id):
    url = f'http://api.smart-insight-service.com:40423/case_beneficiary_payee?a=detail&medical_id={案件id}'
    return url

def 案件详情页申请人网址(案件id):
    url = f'http://api.smart-insight-service.com:40423/case_beneficiary_payee?a=detail_applicant&medical_id={案件id}'
    return url

def 案件详情退单查询网址(票据类型, 案件id, 票据id):
    # type=1是城镇居民门诊，2是城镇职工门诊，=3是住院，=5是门特；stub_id对应网址iteam_id
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=get_drug_fee_note&type={票据类型}&case_id={案件id}&iteam_id={票据id}&_=1638276609808'
    return url

def 案件详情保期查询网址(保期查询号, 保单号):
    # 案件详情页获取信息内容
    url = f'http://api.smart-insight-service.com:40423/case_medical?a=detail_duty&assurer_id={保期查询号}&insurance_no={保单号}'
    return url

# 提取内容
def 提取案件列表数量(x):
    if x:
        当前页数 = x.get('cur_page')
        案件数量 = x.get('count')
        当前页最大显示页数 = x.get('end_page')
        总页数 = x.get('pages')

        data = {'当前页数': 当前页数, '案件数量': 案件数量, '当前页最大显示页数': 当前页最大显示页数, '总页数': 总页数}
    else:
        data = {}
        put_text('没有列表数量信息')
    return data

def 提取案件列表个案详情(x):
    if x:
        姓名 = x.get('name')
        批次号 = x.get('batch_no')
        案件号 = x.get('no')
        身份证号 = x.get('id_no')
        上传时间 = x.get('case_data').get('upload_time')
        回传时间 = x.get('case_data').get('send_time')
        案件状态 = x.get('case_status')    # 案件的各种状态,可检查核查状态
        案件id = x.get('case_id')
        审核员 = x.get('user').get('nickname')
        理算状态 = x.get('adjuster_name')
        理算标识 = x.get('adjuster_status')
        身份证号 = x.get('id_no')
        核查状态 = x.get('check_name')  # 和核查校验是一个
        核查校验 = x.get('is_check')

        data = {
            '姓名': 姓名,
            '批次号': 批次号,
            '案件号': 案件号,
            '身份证号': 身份证号,
            '上传时间': 上传时间,
            '回传时间': 回传时间,
            '案件状态': 案件状态,
            '案件id': 案件id,
            '审核员': 审核员,
            '核查状态': 核查状态,
            '理算状态': 理算状态,
            '理算标识': 理算标识,
            '身份证号': 身份证号,
            '核查校验': 核查校验
        }
    else:
        data = {}
        print('没有案件列表信息')
    return data

def 提取列案件表页理算结果(x):
    人寿给付责任编码 = {
        '门诊': ['1081103301', '1121101402', '1121103402'],
        '住院': ['1121101403', '1121101405', '1121103403', '1121101404', '1081102301'],
        '门特': ['1121101407']
        }
        
    if x:
        住院标识 = 0
        门诊标识 = 0
        门特标识 = 0
        
        门诊个人赔案号 = ''
        门诊保单号 = ''
        门诊事件号 = ''
        门诊申请金额 = 0
        门诊回传金额 = 0
        门诊责任编码 = ''
        门诊给付责任编码 = ''
        住院个人赔案号 = ''
        住院保单号 = ''
        住院事件号 = ''
        住院申请金额 = 0
        住院回传金额 = 0
        住院责任编码 = ''
        住院给付责任编码 = ''
        门特个人赔案号 = ''
        门特保单号 = ''
        门特事件号 = ''
        门特申请金额 = 0
        门特回传金额 = 0
        门特责任编码 = ''
        门特给付责任编码 = ''
        申请总额 = ''
        回传总额 = ''

        for i in x:
            for j in 人寿给付责任编码:
                if i.get('pay_duty_code') in 人寿给付责任编码[j]:

                    if '门诊' == j:
                        if 门诊标识 == 0:
                            门诊个人赔案号 = i.get('event_no')
                            门诊保单号 = i.get('insurance_no')
                            门诊事件号 = i.get('compensation_no')
                            门诊申请金额 = float(i.get('bill_money', 0))
                            门诊回传金额 = float(i.get('insurance_pay', 0))
                            门诊责任编码 = i.get('duty_code')
                            门诊给付责任编码 = i.get('pay_duty_code')
                            门诊标识 = 1
                        else:
                            门诊申请金额 += float(i.get('bill_money', 0))
                            门诊回传金额 += float(i.get('insurance_pay', 0))
                            
                    elif '住院' == j:
                        if 住院标识 == 0:
                            住院个人赔案号 = i.get('event_no')
                            住院保单号 = i.get('insurance_no')
                            住院事件号 = i.get('compensation_no')
                            住院申请金额 = float(i.get('bill_money', 0))
                            住院回传金额 = float(i.get('insurance_pay', 0))
                            住院责任编码 = i.get('duty_code')
                            住院给付责任编码 = i.get('pay_duty_code')
                            住院标识 = 1
                        else:
                            住院申请金额 += float(i.get('bill_money', 0))
                            住院回传金额 += float(i.get('insurance_pay', 0))

                    elif '门特' == j:
                        if 门特标识 == 0:
                            门特个人赔案号 = i.get('event_no')
                            门特保单号 = i.get('insurance_no')
                            门特事件号 = i.get('compensation_no')
                            门特申请金额 = float(i.get('bill_money', 0))
                            门特回传金额 = float(i.get('insurance_pay', 0))
                            门特责任编码 = i.get('duty_code')
                            门特给付责任编码 = i.get('pay_duty_code')
                            门特标识 = 1
                        else:
                            门特申请金额 += float(i.get('bill_money', 0))
                            门特回传金额 += float(i.get('insurance_pay', 0))
                            

        住院申请总额 = round((住院申请金额+门特申请金额), 2)
        住院回传总额 = round((住院回传金额+门特回传金额), 2)

        申请总额 = round((门诊申请金额+住院申请总额), 2)
        回传总额 = round((门诊回传金额+住院回传总额), 2)

        date = {
            '门诊个人赔案号': 门诊个人赔案号,
            '门诊保单号': 门诊保单号,
            '门诊事件号': 门诊事件号,
            '门诊申请金额': 门诊申请金额,
            '门诊回传金额': 门诊回传金额,
            '门诊责任编码': 门诊责任编码,
            '门诊给付责任编码': 门诊给付责任编码,
            '住院个人赔案号': 住院个人赔案号,
            '住院保单号': 住院保单号,
            '住院事件号': 住院事件号,
            '住院申请金额': 住院申请金额,
            '住院回传金额': 住院回传金额,
            '住院责任编码': 住院责任编码,
            '住院给付责任编码': 住院给付责任编码,
            '门特个人赔案号': 门特个人赔案号,
            '门特保单号': 门特保单号,
            '门特事件号': 门特事件号,
            '门特申请金额': 门特申请金额,
            '门特回传金额': 门特回传金额,
            '门特责任编码': 门特责任编码,
            '门特给付责任编码': 门特给付责任编码,
            '住院申请总额': 住院申请总额,
            '住院回传总额': 住院回传总额,
            '申请总额': 申请总额,
            '回传总额': 回传总额
        }

    else:
        date = {}
        print('没有理算信息')

    return date

def 提取案件详情基础信息(x):
    if x:
        姓名 = x.get('name')
        证件类型 = x.get('id_type_name')
        身份证号 = x.get('id_no')
        性别 = x.get('gender_name')
        联系电话 = x.get('phone')
        职业 = x.get('career').get('text')
        社保号 = x.get('ssn')
        银行名 = x.get('bank')
        银行帐号 = x.get('bank_no')
        保单银行名 = x.get('assurer_bank')
        保单银行账号 = x.get('assurer_bank_no')
        保单数 = x.get('insurance_list')
        保单号 = x.get('insurance_no')
        保期查询号 = x.get('assurer_id')
        保单方案 = x.get('solution')
        生效时间 = x.get('effect_time')
        特殊人员标识 = x.get('special_personnel')
        医保类型 = x.get('type_name')
        问题件 = x.get('error_flag_name')
        问题件简述 = x.get('error_remark')
        批次号 = x.get('batch_no')
        案件号 = x.get('no')
        申请金额 = float(x.get('apply', 0))
        备注 = x.get('remark')
        if x.get('assurer'):
            投保单位 = x.get('assurer').get('company').get('name')
            出生日期 = x.get('assurer').get('birth_time')
            年龄 = 2021 - int(身份证号[6:10]) + 1
            国籍 = x.get('assurer').get('country')
        else:
            投保单位 = '无'
            出生日期 = '无'
            年龄 = '无'
            国籍 = '无'

        data = {
            '姓名': 姓名,
            '证件类型': 证件类型,
            '身份证号': 身份证号,
            '性别': 性别,
            '联系电话': 联系电话,
            '职业': 职业,
            '社保号': 社保号,
            '银行名': 银行名,
            '银行帐号': 银行帐号,
            '保单银行名': 保单银行名,
            '保单银行账号': 保单银行账号,
            '保单数': 保单数,
            '保单号': 保单号,
            '保期查询号': 保期查询号,
            '保单方案': 保单方案,
            '生效时间': 生效时间,
            '特殊人员标识': 特殊人员标识,
            '医保类型': 医保类型,
            '问题件': 问题件,
            '问题件简述': 问题件简述,
            '批次号': 批次号,
            '案件号': 案件号,
            '申请金额': 申请金额,
            '备注': 备注,
            '投保单位': 投保单位,
            '出生日期': 出生日期,
            '年龄': 年龄,
            '国籍': 国籍
        }

    else:
        data = {}
        print('没有基础信息')
    return data

def 提取保期信息(x):
    # 以列表形式[{}]传入参数，筛重之后再以字典形式返回
    if x:
        # dic用来筛重保单方案
        datas = {}
        for i in x:
            方案名称 = i.get('sol_name')
            责任名称 = i.get('duty_name')
            责任始期 = time.strftime("%Y-%m-%d", time.localtime(i.get('duty_begin_time')))
            责任止期 = time.strftime("%Y-%m-%d", time.localtime(i.get('duty_end_time')))
            给付责任名称 = i.get('pay_duty_name')
            给付责任始期 = time.strftime("%Y-%m-%d", time.localtime(i.get('pay_duty_begin_time')))
            给付责任止期 = time.strftime("%Y-%m-%d", time.localtime(i.get('pay_duty_end_time')))

            datas[方案名称] = {
                '责任名称': 责任名称,
                '责任始期': 责任始期,
                '责任止期': 责任止期,
                '给付责任名称': 给付责任名称,
                '给付责任始期': 给付责任始期,
                '给付责任止期': 给付责任止期
            }
    else:
        datas = {}
        put_text('没有保期信息')
    
    return datas

def 提取案件详情城镇门诊信息(x):
    if x:
        姓名 = x.get('name')
        票据号 = x.get('sn')
        叹号下标 = x.get('signet')
        账单类型 = x.get('bill_type').get('name')
        医院名称 = x.get('hospital').get('name')
        疾病名称 = x.get('disease').get('name')
        门诊大额支付 = float(x.get('clinic_charge', 0))
        退休补充支付 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))
        合计校验 = x.get('total_self_charge_check')
        票据时间 = x.get('occur_time')
        票根 = x.get('attach').get('name')
        案件id = x.get('case_id')
        票据id = x.get('stub_id')
        退单状态 = x.get('back_type') # 1退单，0不退单
        票据类型 = 2

        # 检查标红
        if 合计校验:
            字段标红 = '否'
        else:
            字段标红 = '是'

        data = {
            '姓名': 姓名,
            '票据号': 票据号,
            '叹号下标': 叹号下标,
            '账单类型': 账单类型,
            '医院名称': 医院名称,
            '疾病名称': 疾病名称,
            '门诊大额支付': 门诊大额支付,
            '退休补充支付': 退休补充支付,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计,
            '票据时间': 票据时间,
            '票根': 票根,
            '案件id': 案件id,
            '票据id': 票据id,
            '退单状态': 退单状态,
            '票据类型': 票据类型,
            '字段标红': 字段标红
        }

    else:
        data = {}
        put_text('没有城镇门诊信息')
    return data

def 提取案件详情居民门诊信息(x):
    if x:
        姓名 = x.get('name')
        票据号 = x.get('sn')
        叹号下标 = x.get('signet')
        账单类型 = x.get('bill_type').get('name')
        医院名称 = x.get('hospital').get('name')
        疾病名称 = x.get('disease').get('name')
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))
        合计校验 = x.get('total_self_charge_check')
        票据时间 = x.get('occur_time')
        票根 = x.get('attach').get('name')
        案件id = x.get('case_id')
        票据id = x.get('stub_id')
        退单状态 = x.get('back_type') # 1退单，0不退单
        票据类型 = 1
        # 检查标红
        if 合计校验:
            字段标红 = '否'
        else:
            字段标红 = '是'

        data = {
            '姓名': 姓名,
            '票据号': 票据号,
            '叹号下标': 叹号下标,
            '账单类型': 账单类型,
            '医院名称': 医院名称,
            '疾病名称': 疾病名称,
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计,
            '票据时间': 票据时间,
            '票根': 票根,
            '案件id': 案件id,
            '票据id': 票据id,
            '退单状态': 退单状态,
            '票据类型': 票据类型,
            '字段标红': 字段标红
        }

    else:
        data = {}
        print('没有居民门诊信息')
    return data

def 提取案件详情城镇门诊合计信息(x):
    if x:
        门诊大额支付 = float(x.get('clinic_charge', 0))
        退休补充支付 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))

        data = {
            '门诊大额支付': 门诊大额支付,
            '退休补充支付': 退休补充支付,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计}
    else:
        data = {}
        print('没有门诊合计信息')
    return data

def 提取案件详情居民门诊合计信息(x):
    if x:
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))

        data = {
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计}
    else:
        data = {}
        print('没有门诊合计信息')
    return data

def 提取案件详情住院信息(x):
    if x:
        姓名 = x.get('name')
        票据号 = x.get('sn')
        叹号下标 = x.get('signet')
        账单类型 = x.get('bill_type').get('name')
        医院名称 = x.get('hospital').get('name')
        疾病名称 = x.get('disease').get('name')
        医疗保险范围内金额 = float(x.get('insurance_charge', 0))
        医疗保险基金支付金额 = float(x.get('sum_insurance_charge', 0))
        统筹基金 = float(x.get('whole_charge', 0))
        退休补充医疗保险 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))
        合计校验 = x.get('total_self_charge_check')
        入院时间 = x.get('in_time')
        出院时间 = x.get('out_time')
        票根 = x.get('attach').get('name')
        案件id = x.get('case_id')
        票据id = x.get('stub_id')
        退单状态 = x.get('back_type') # 1退单，0不退单
        票据类型 = 3
        # 检查标红
        if 合计校验:
            字段标红 = '否'
        else:
            字段标红 = '是'

        data = {
            '姓名': 姓名,
            '票据号': 票据号,
            '叹号下标': 叹号下标,
            '账单类型': 账单类型,
            '医院名称': 医院名称,
            '疾病名称': 疾病名称,
            '医疗保险范围内金额': 医疗保险范围内金额,
            '医疗保险基金支付金额': 医疗保险基金支付金额,
            '统筹基金': 统筹基金,
            '退休补充医疗保险': 退休补充医疗保险,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '个人支付': 个人支付,
            '合计': 合计,
            '入院时间': 入院时间,
            '出院时间': 出院时间,
            '票根': 票根,
            '案件id': 案件id,
            '票据id': 票据id,
            '退单状态': 退单状态,
            '票据类型': 票据类型,
            '字段标红': 字段标红
        }

    else:
        data = {}
        print('没有住院信息')
    return data

def 提取案件详情住院合计信息(x):
    if x:
        医疗保险范围内金额 = float(x.get('insurance_charge', 0))
        医疗保险基金支付金额 = float(x.get('sum_insurance_charge', 0))
        统筹基金 = float(x.get('whole_charge', 0))
        退休补充医疗保险 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))

        data = {
            '医疗保险范围内金额': 医疗保险范围内金额,
            '医疗保险基金支付金额': 医疗保险基金支付金额,
            '统筹基金': 统筹基金,
            '退休补充医疗保险': 退休补充医疗保险,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '个人支付': 个人支付,
            '合计': 合计
        }
    else:
        data = {}
        print('没有住院合计信息')
    return data

def 提取案件详情门特信息(x):
    if x:
        姓名 = x.get('name')
        票据号 = x.get('sn')
        叹号下标 = x.get('signet')
        账单类型 = x.get('bill_type').get('name')
        医院名称 = x.get('hospital').get('name')
        疾病名称 = x.get('disease').get('name')
        统筹基金支付 = float(x.get('whole_charge', 0))
        住院大额支付 = float(x.get('clinic_charge', 0))
        退休补充支付 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))
        合计校验 = x.get('total_self_charge_check')
        票据时间 = x.get('occur_time')
        票根 = x.get('attach').get('name')
        案件id = x.get('case_id')
        票据id = x.get('stub_id')
        退单状态 = x.get('back_type') # 1退单，0不退单
        票据类型 = 5
        # 检查标红
        if 合计校验:
            字段标红 = '否'
        else:
            字段标红 = '是'

        data = {
            '姓名': 姓名,
            '票据号': 票据号,
            '叹号下标': 叹号下标,
            '账单类型': 账单类型,
            '医院名称': 医院名称,
            '疾病名称': 疾病名称,
            '统筹基金支付': 统筹基金支付,
            '住院大额支付': 住院大额支付,
            '退休补充支付': 退休补充支付,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计,
            '票据时间': 票据时间,
            '票根': 票根,
            '案件id': 案件id,
            '票据id': 票据id,
            '退单状态': 退单状态,
            '票据类型': 票据类型,
            '字段标红': 字段标红
        }
    else:
        data = {}
        print('没有门特信息')
    return data

def 提取案件详情门特合计信息(x):
    if x:
        统筹基金支付 = float(x.get('whole_charge', 0))
        住院大额支付 = float(x.get('clinic_charge', 0))
        退休补充支付 = float(x.get('retire_charge', 0))
        残军补助支付 = float(x.get('army_charge', 0))
        单位补充险支付 = float(x.get('staff_charge', 0))
        本次医保范围内金额 = float(x.get('charge', 0))
        累计医保内范围金额 = float(x.get('total_charge', 0))
        自付一 = float(x.get('self_charge_1', 0))
        起付金额 = float(x.get('self_charge_1_min', 0))
        超封顶金额 = float(x.get('self_charge_1_max', 0))
        自付二 = float(x.get('self_charge_2', 0))
        自费 = float(x.get('self_charge', 0))
        基金支付 = float(x.get('fund_pay', 0))
        个人支付 = float(x.get('person_pay', 0))
        合计 = float(x.get('total_self_charge', 0))

        data = {
            '统筹基金支付': 统筹基金支付,
            '住院大额支付': 住院大额支付,
            '退休补充支付': 退休补充支付,
            '残军补助支付': 残军补助支付,
            '单位补充险支付': 单位补充险支付,
            '本次医保范围内金额': 本次医保范围内金额,
            '累计医保内范围金额': 累计医保内范围金额,
            '自付一': 自付一,
            '起付金额': 起付金额,
            '超封顶金额': 超封顶金额,
            '自付二': 自付二,
            '自费': 自费,
            '基金支付': 基金支付,
            '个人支付': 个人支付,
            '合计': 合计
        }
    else:
        data = {}
        print('没有门特合计信息')
    return data

def 提取领款人信息(x):
    if x:
        姓名 = x.get('name')
        性别 = x.get('gender_name')
        出生日期 = x.get('birth_name')
        证件类型 = x.get('id_type_name')
        证件号码 = x.get('id_no')
        证件签发日期 = x.get('id_begin_time_name')
        证件失效日期 = x.get('id_end_time_name')
        证件为长期 = x.get('id_long_time')  # 0否 1是
        国籍 = x.get('country_code_name')
        领款人与受益人关系 = x.get('beneficiary_relation_name')

        data = {
            '姓名': 姓名,
            '性别': 性别,
            '出生日期': 出生日期,
            '证件类型': 证件类型,
            '证件号码': 证件号码,
            '证件签发日期': 证件签发日期,
            '证件失效日期': 证件失效日期,
            '证件为长期': 证件为长期,
            '国籍': 国籍,
            '领款人与受益人关系': 领款人与受益人关系
        }
    else:
        data = {}
        print('没有领款人信息')
    return data

def 提取受益人信息(x):
    if x:
        姓名 = x.get('name')
        性别 = x.get('gender_name')
        出生日期 = x.get('birth_name')
        证件类型 = x.get('id_type_name')
        证件号码 = x.get('id_no')
        证件签发日期 = x.get('id_begin_time_name')
        证件失效日期 = x.get('id_end_time_name')
        证件为长期 = x.get('id_long_time')  # 0否 1是
        国籍 = x.get('country_code_name')
        受益人与被保险人关系 = x.get('beneficiary_relation_name')

        data = {
            '姓名': 姓名,
            '性别': 性别,
            '出生日期': 出生日期,
            '证件类型': 证件类型,
            '证件号码': 证件号码,
            '证件签发日期': 证件签发日期,
            '证件失效日期': 证件失效日期,
            '证件为长期': 证件为长期,
            '国籍': 国籍,
            '受益人与被保险人关系': 受益人与被保险人关系
        }
    else:
        data = {}
        print('没有受益人信息')
    return data

def 提取退单内容(x):
    if x:
        x1 = x['total_drug'][0]['note'][0]
        退单原因 = x1['name']
        问题描述 = x1['descript']
        退单类型 = x1['back_type']  # 1是整张退单，2是部分退单

        data = {
            '退单原因': 退单原因,
            '问题描述': 问题描述,
            '退单类型': 退单类型
        }
    else:
        data = {}
        put_text('没有退单原因')
    return data

def 获取案件信息(url, headers):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        req = s.get(url=url, headers=headers, timeout=200)
        r = req.json()
        a = r.get('msg')
        if a == '请求成功':
            datas = r.get('data')  # 案件列表要分离2次，案件详情分离1次。

        else:
            datas = a
            print(a)
        
        # else:
        #     print(datetime.now())
        #     print(a)
        #     # put_text(a)
        #     datas = {}
            
    except Exception as e:
        # 输出错误提示
        print(datetime.now())
        exstr = traceback.format_exc()
        print(f'exstr = {exstr}')
        print(f'e = {e}')
        datas = {}

    return datas

if __name__ == '__main__':
    headers = 检查登录状态('输入账号')

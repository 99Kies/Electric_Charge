# coding : utf-8

import requests
from pyquery import PyQuery as pq
import re
import time


def login_post(userid,userpassword,money,area,house):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        s = requests.session()
        r = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/')
        doc = pq(r.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        items = doc.find('#Table3 > tbody > tr > td').items()

        yanzhen = ''

        for item in items:
            aim = item.find('img').attr('src')
            if aim is not None:
                pic = re.findall('.*(\d).*', aim)
                yanzhen = yanzhen + pic[0]

        login_data = {
            '__LASTFOCUS':'',
            '__VIEWSTATE':value_1,
            'UserLogin:txtUser': userid,
            'UserLogin:txtPwd':userpassword,
            'UserLogin:ddlPerson': '卡户',
            'UserLogin:txtSure': yanzhen,
            'UserLogin:ImageButton1.x': '37',
            'UserLogin:ImageButton1.y': '10',
            '_EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__EVENTVALIDATION': value_2
        }

        r_login = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Default.aspx',data=login_data)
        r_login = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/Cardholder.aspx',headers=headers)
        yu_e = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/AccBalance.aspx')
        doc = pq(yu_e.text)
        MyMoney = doc.find('#lblOne0').text()
        print('当前余额为：%s' % MyMoney)
        are_you_sure()
        if eval(money) > eval(MyMoney[1:]):
            print('心里还有点数吗,就剩 %s,这么不买个飞机.' % (MyMoney))
            return None
        r_post = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelp.aspx', headers=headers)
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')

        post_data = {
            '__EVENTTARGET':'rbItem',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE':value_1,
            '__smartNavPostBack':'true',
            'rbList':'rbList',
            'rbItem':'rbItem',
            'rdoAll':'rdoAll',
            'DropDownList1':'2015',
            'DropDownList2':'01',
            '__EVENTVALIDATION':value_2
        }
        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelp.aspx',data=post_data)
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        list_post_data = {
            '__EVENTTARGET':'lsItem',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE':value_1,
            'rbItem':'rbItem',
            'lsItem':'999',
            'rdoAll':'rdoAll',
            'DropDownList1':'2015',
            'DropDownList2':'01',
            '__EVENTVALIDATION':value_2,
            '__smartNavPostBack':'true'
        }
        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelp.aspx',data=list_post_data)
        r_post = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpElec.aspx')
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        first_data = {
            '__EVENTTARGET':'lsArea',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE':value_1,
            'lsArea':area,
            '__EVENTVALIDATION': value_2,
        }
        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpElec.aspx',data=first_data)
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        home = '0' + house[0]
        second_data = {
            '__EVENTTARGET':'lsHouse',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE': value_1,
            'lsArea':area,
            'lsHouse':home,
            '__EVENTVALIDATION':value_2,
        }
        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpElec.aspx',data=second_data)
        r_post.encoding = r_post.apparent_encoding
        msg = '<option value="(.*?)">%s照明</option>' % house
        room = re.findall(msg,r_post.text)[0]
        # print(room)
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        thrid_data = {
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE':value_1,
            'lsArea':area, # 宿舍楼
            'lsHouse':home, # 楼层
            'lsRoom':room,
            '__EVENTVALIDATION':value_2,
            'btnOK.x':'24',
            'btnOK.y':'16',
        }
        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpElec.aspx',data=thrid_data)
        r_post = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpPay.aspx')
        doc = pq(r_post.text)
        value_1 = doc.find('#__VIEWSTATE').attr('value')
        value_2 = doc.find('#__EVENTVALIDATION').attr('value')
        Electric = doc.find('#lblItem').text()
        Electric = re.search('缴费项目：常工用电缴费 当前剩余电量：(.*?)度', Electric)[1]
        final_data = {
            '__VIEWSTATE':value_1,
            'txtMon':money,
            'txtPwd':userpassword,
            '__EVENTVALIDATION':value_2,
            'btnOK.x':'13',
            'btnOK.y':'17',
        }

        r_post = s.post('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/SelfHelpPay.aspx',data=final_data)
        r_post.encoding = r_post.apparent_encoding
        if '缴费成功' in r_post.text:
            print('缴费成功')
            yu_e = s.get('http://dcard.zjhu.edu.cn/Zytk32Portal/Cardholder/AccBalance.aspx')
            doc = pq(yu_e.text)
            MyMoney = doc.find('#lblOne0').text()
            print('成功缴费：%s\t余额还剩：%s\t还剩%s度电' % (money, MyMoney, Electric))
            time.sleep(5)
        else:
            print('Error')
    except:
        login_post(userid, userpassword, money, area, house)


def are_you_sure():
    yes = ['yes','y']
    no = ['no','n']
    Is = input('are you sure, 你就整这些??? [yes/no]:  ')
    if Is in yes:
        # login_post(userid, userpassword, money, area, house)
        # return None
        pass
    elif Is in no:
        print('好的老弟, 多挣点钱养我')
        time.sleep(5)
        return None

if __name__ == '__main__':

    userid = input('学号:  ')
    userpassword = input('密码:  ')
    area = input('哪栋:  ')
    house = input('哪间寝室:  ')
    money = input('给你寝室整多少的:  ')
    # are_you_sure(userid,userpassword,money,area,house)
    login_post(userid,userpassword,money,area,house)
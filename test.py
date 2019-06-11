import requests
from bs4 import BeautifulSoup

#email model
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

#time model
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job():
    page = requests.get('http://ssdut.dlut.edu.cn/index/bkstz.htm')
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'lxml')
    dataList = []
    for ul in soup.find_all(attrs={'style': 'width:650px;'}):
        found_title = ul.a['title']
        found_website_temp = ul.a['href']
        found_date_temp = ul.span.string

        # 2018-03-07
        found_date = found_date_temp.strip().lstrip().rstrip(',')
        found_website = found_website_temp.replace('..', 'http://ssdut.dlut.edu.cn')

        dic = {'title': found_title, 'website': found_website, 'date': found_date}
        dataList.append(dic)
        # print dic

    # loading email model
    host_server = 'smtp.qq.com'
    sender_qq = 'dlutzhy@qq.com'
    pwd = ''

    sender_qq_mail = 'dlutzhy@qq.com'
    receiver = 'dlutzhy@qq.com'

    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq , pwd)


    todayTime = time.strftime('%Y-%m-%d')
    print todayTime
    for dic in dataList:
        if dic['date'] == todayTime:
            newPage = requests.get(dic['website'])
            newPage.encoding = 'utf-8'
            newSoup = BeautifulSoup(newPage.text, 'lxml')
            #next pages
            for url in newSoup.find_all(attrs={'id': 'vsb_content'}):
                print url

                mail_content = dic['website']
                mail_title = dic['title']


                msg = MIMEText(mail_content, 'plain', 'utf-8')
                msg['Subject'] = Header(mail_title, 'utf-8')
                msg['From'] = sender_qq_mail
                msg['To'] = receiver
                msg['Accept-Language'] = 'zh-CN'
                msg['Accept-Charset'] = 'utf-8'
                smtp.sendmail(sender_qq_mail, receiver, msg.as_string())

    smtp.quit()
#end job
scheduler = BlockingScheduler()
scheduler.add_job(job,'cron',day_of_week='0-6',hour=22,minute=50)
scheduler.start()


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send(content='', type='plain'):

    user = 'xxxx'
    pwd = 'xxxx'
    to = ['xxxx']
    if content == '':
        content = '<h3>公子，票已经抢到，请速速去支付</h3>'

    msg = MIMEMultipart()
    msg['Subject'] = Header('火车票订单', 'utf-8')
    msg['From'] = Header(user)
    doc = MIMEText(content, type, 'utf-8')
    msg.attach(doc)

    s = smtplib.SMTP('smtp.sina.com')
    s.set_debuglevel(1)              #调试使用
    s.starttls()                     #建议使用
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    s.close()


def buildHTML(data):
    rows = ''
    for row in data:
        rows = '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(row[0], row[1], row[2], row[3], row[4], row[5])

    html = '''
            <table border="1" style="border-collapse: collapse;width: 600px;text-align: center;color: darkorchid;">
    		<thead>
    			<tr>
    				<td>序号</td>
    				<td>车次信息</td>
    				<td>席位信息</td>
    				<td>旅客信息</td>
    				<td>票款金额</td>
    				<td>车票状态</td>
    			</tr>
    		</thead>
    		<tbody>
    		%s
    		</tbody>
    	</table>
        ''' % rows
    return html


if __name__ == "__main__":
    pass
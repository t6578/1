import requests
from lxml import etree
import xlwt
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
qiyulist=[] #存储区域信息
while True:
    quyu = input('请输入你要查询的区域，一次输入一个，输入q推出，目前有藏龙岛，黄家湖，文化大道，纸坊，庙山，其他：') #输入区域
    if quyu == '藏龙岛':
        url = 'https://wh.lianjia.com/ershoufang/canglongdao/'
        qiyulist.append(url)
    elif quyu == '黄家湖':
        url = 'https://wh.lianjia.com/ershoufang/huangjiahu/'
        qiyulist.append(url)
    elif quyu == '文化大道':
        url = 'https://wh.lianjia.com/ershoufang/wenhualu/'
        qiyulist.append(url)
    elif quyu == '纸坊':
        url = 'https://wh.lianjia.com/ershoufang/zhifang/'
        qiyulist.append(url)
    elif quyu == '庙山':
        url = 'https://wh.lianjia.com/ershoufang/miaoshan/'
        qiyulist.append(url)
    elif quyu == '其他':
        url = 'https://wh.lianjia.com/ershoufang/jiangxiaqita'
        qiyulist.append(url)
    elif quyu == 'q':
        break
    else:
        print('输入错误，程序退出，请重新执行')
        exit()
print(qiyulist)
page = int(input('请输入要爬取的页数：')) #爬取页数
listurl= [] #存储所有区域的url
all_url = [] #存储所有区域页数的url
for i in range(1, page+1):
    for url in qiyulist:
        url = url + 'pg' + str(i)
        all_url.append(url)
for a in all_url:
    response=requests.get(a,headers=headers)
    html=etree.HTML(response.text)
    url=html.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a/@href')
    listurl.extend(url)
print(listurl) #打印所有url
book = xlwt.Workbook(encoding='utf-8',style_compression=0) #创建excel
sheet = book.add_sheet('链家二手房',cell_overwrite_ok=True) #创建sheet
sheet.write(0,0,'标题')
sheet.write(0,1,'价格')
sheet.write(0,2,'单价')
sheet.write(0,3,'户型')
sheet.write(0,4,'朝向')
sheet.write(0,5,'总面积')
sheet.write(0,6,'小区名称')
sheet.write(0,7,'所在区域')
sheet.write(0,8,'装修情况')
sheet.write(0,9,'梯户比例')
sheet.write(0,10,'抵押信息')
sheet.write(0,11,'房屋年限')
data=[] #存储所有行信息

#爬取信息
for b in listurl:
    try:
        response=requests.get(b,headers=headers) #请求url
        h=etree.HTML(response.text) #解析
        title=h.xpath("/html/body/div[3]/div/div/div[1]/h1/@title")[0]
        price=h.xpath("/html/body/div[5]/div[2]/div[3]/div/span[1]/text()")[0]+"万"
        unitprice=h.xpath("/html/body/div[5]/div[2]/div[3]/div/div[1]/div[1]/span/text()")[0]+"元/平米"
        huxing=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[1]/text()")[0]
        chaoxiang=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[3]/text()")[0]
        mianji=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[3]/text()")[0]
        xqmc=h.xpath("/html/body/div[5]/div[2]/div[5]/div[1]/a[1]/text()")[0]
        qy1=h.xpath("/html/body/div[5]/div[2]/div[5]/div[2]/span[2]/a/text()")[0]
        qy2 = h.xpath("/html/body/div[5]/div[2]/div[5]/div[2]/span[2]/a/text()")[1]
        qy3 = h.xpath("/html/body/div[5]/div[2]/div[5]/div[2]/span[2]/text()")[1]
        szqy=qy1+qy2+qy3
        zxqk=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[9]/text()")[0]
        thbl=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[11]/text()")[0]
        dyxx=h.xpath("//html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()")[0].strip()
        fwnx=h.xpath("/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()")[0]
        print(title,price,unitprice,huxing,chaoxiang,mianji,xqmc,szqy,zxqk,thbl,dyxx,fwnx)
        data.append([title,price,unitprice,huxing,chaoxiang,mianji,xqmc,szqy,zxqk,thbl,dyxx,fwnx])
    except Exception as e:
        print(e)
        continue
#写入excel
for i in range(0,len(data)):
    for j in range(0,len(data[i])):
        sheet.write(i+1,j,data[i][j])
book.save('链家二手房.xls') #保存excel

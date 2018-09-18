import sqlite3
import xlwt
def select_data(table):
    conn=sqlite3.connect('hillstone_covert_tool.db')
    c=conn.cursor()
    sql='select * from '+table
    c.execute(sql)
    values=c.fetchall()
    conn.commit()
    conn.close()
    return values

def select_address(addr):
    conn=sqlite3.connect('hillstone_covert_tool.db')
    c=conn.cursor()
    sql='select * from address where addr_name="'+addr+'"'
    c.execute(sql)
    values=c.fetchall()
    conn.commit()
    conn.close() 
    return values

def addrlist(values):
    if values:
        if values[0][2]=='host':
            v=values[0][3].split(',')
        elif values[0][2]=='subnet':
            v=[values[0][3].replace(',','/'),]
        elif values[0][2]=='range':
            v=[values[0][3].replace(',','-'),]
        elif values[0][2]=='group':
            obj=values[0][3].split(',')
            v=[]
            for ip in obj:
                iplist=select_address(ip)
                if iplist[0][2]=='host':
                    v+=iplist[0][3].split(',')
                elif iplist[0][2]=='subnet':
                    v+=[iplist[0][3].replace(',','/'),]
                elif iplist[0][2]=='range':
                    v+=[iplist[0][3].replace(',','-'),]                

    else:
        v=[]
    return v
#
v=select_data('policy')


wbk = xlwt.Workbook()
sheet = wbk.add_sheet('policy_ip')
i=0
for row in v:
    srcaddr=select_address(str(row[6]))
    dstaddr=select_address(str(row[7]))
    src=addrlist(srcaddr)
    dst=addrlist(dstaddr)
  
    #print(src)
    #print(addr)
    if dst:
        for dstip in dst:
            if src:
                for srcip in src:
                    print(row[6]+' ('+srcip+') -->'+row[7]+'('+dstip+')'+row[8])
                    sheet.write(i,0,row[0])
                    sheet.write(i,1,row[4])
                    sheet.write(i,2,row[5])
                    sheet.write(i,3,row[6])
                    sheet.write(i,4,srcip)
                    sheet.write(i,5,row[7])
                    sheet.write(i,6,dstip)
                    sheet.write(i,7,row[8])
                    sheet.write(i,8,row[3])
                    i+=1
            else:
                print(row[6]+' -->'+row[7]+'('+dstip+')'+row[8])
                sheet.write(i,0,row[0])
                sheet.write(i,1,row[4])
                sheet.write(i,2,row[5])
                sheet.write(i,3,row[6])
                sheet.write(i,4,row[6])
                sheet.write(i,5,row[7])
                sheet.write(i,6,dstip)
                sheet.write(i,7,row[8])
                sheet.write(i,8,row[3])
                i+=1
    else:
            if src:
                for srcip in src:
                    print(row[6]+' ('+srcip+') -->'+row[7]+row[8])
                    sheet.write(i,0,row[0])
                    sheet.write(i,1,row[4])
                    sheet.write(i,2,row[5])
                    sheet.write(i,3,row[6])
                    sheet.write(i,4,srcip)
                    sheet.write(i,5,row[7])
                    sheet.write(i,6,row[7])
                    sheet.write(i,7,row[8])
                    sheet.write(i,8,row[3])
                    i+=1
            else:
                print(row[6]+' -->'+row[7]+row[8])
                sheet.write(i,0,row[0])
                sheet.write(i,1,row[4])
                sheet.write(i,2,row[5])
                sheet.write(i,3,row[6])
                sheet.write(i,4,row[6])
                sheet.write(i,5,row[7])
                sheet.write(i,6,row[7])
                sheet.write(i,7,row[8])
                sheet.write(i,8,row[3])
                i+=1
 

wbk.save('iptable.xls')
        




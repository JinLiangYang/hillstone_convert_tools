import sqlite3
import os
import datetime
###########################数据库部分函数 #######################################
class db():
    def __init__(self):
        pass    
    def newdb(self):
        if os.path.exists(os.getcwd() + 'hillstone_covert_tool.db'):  # 判断当前源文件的文件夹下是否存在，
            os.remove(os.getcwd() + 'hillstone_covert_tool.db')  # 如果存在就删除这个数据库，
        conn=sqlite3.connect('hillstone_covert_tool.db')
        c = conn.cursor()
        #创建服务表
        c.execute('create table IF NOT EXISTS service('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'serv_name char(100),'\
                'type char(50),'\
                'srcport_start char(50),'\
                'srcport_end char(50),'\
                'dstport_start char(50),'\
                'dstport_end char(50),'\
                'description text,'\
                'token char(100))')
        #创建地址表
        c.execute('create table IF NOT EXISTS address('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'addr_name char(100),'\
                'type char(50),'\
                'addr_member text,'\
                'description varchar(255),'\
                'token char(100))')
        
        #创建预定义服务对应关系表
        c.execute('create table IF NOT EXISTS predef_service('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'vendor varchar(100),'\
                'vendor_predef_serv varchar(100),'\
                'hs_predef_serv varchar(100),'\
                'description text,'\
                'token char(100))')
        #创建snat表
        c.execute('create table IF NOT EXISTS snat('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'ruleid varchar(100),'\
                'src_addr text,'\
                'dst_addr text,'\
                'service varchar(100),'\
                'eif varchar(100),'\
                'trans_to varchar(100),'\
                'pat varchar(100),'\
                'sticky varchar(100),'\
                'log varchar(100),'\
                'status varchar(100),'\
                'description text,'\
                'token varchar(100))')
        #创建dnat表
        c.execute('create table IF NOT EXISTS dnat('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'ruleid varchar(100),'\
                'in_if varchar(100),'\
                'src_addr text,'\
                'dst_addr text,'\
                'service varchar(100),'\
                'trans_to varchar(100),'\
                'port varchar(100),'\
                'log varchar(100),'\
                'status varchar(100),'\
                'description text,'\
                'token varchar(100))')
        #创建策略表
        c.execute('create table IF NOT EXISTS policy('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'ruleid varchar(100),'\
                'status varchar(100),'\
                'action varchar(100),'\
                'src_zone varchar(100),'\
                'dst_zone varchar(100),'\
                'src_addr text,'\
                'dst_addr text,'\
                'service varchar(100),'\
                'schedule varchar(100),'\
                'log varchar(100),'\
                'description text,'\
                'token varchar(100))')
        #创建发包工具表
        c.execute('create table IF NOT EXISTS packet('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'src_zone varchar(100),'\
                'dst_zone varchar(100),'\
                'src_ip varchar(100),'\
                'dst_ip varchar(100),'\
                'proto varchar(100),'\
                'port varchar(100),'\
                'description text,'\
                'token varchar(100))')
        #创建token表
        c.execute('create table IF NOT EXISTS token('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'token varchar(100))')
                #创建token表
        c.execute('create table IF NOT EXISTS dstroute('\
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                'dstnet varchar(100),'\
                'gateway varchar(50),'\
                'metric varchar(10),'\
                'interface varchar(100),'\
                'description varchar(100),'\
                'token varchar(100))')
        conn.commit()
        conn.close()
    #插入数据到数据库
    def insert_data(self,type,data):
        conn=sqlite3.connect('hillstone_covert_tool.db')
        c = conn.cursor()
        if type=='service':
            sql='insert into service(serv_name,type,srcport_start,srcport_end,dstport_start,dstport_end,description,token)  values(?,?,?,?,?,?,?,?);'
        elif type=='address':
            sql='insert into address(addr_name,type,addr_member,description,token)  values(?,?,?,?,?);'
        elif type=='snat':
            sql='insert into snat(ruleid,src_addr,dst_addr,service,eif,trans_to,pat,sticky,log,status,description,token) values(?,?,?,?,?,?,?,?,?,?,?,?)'
        elif type=='dnat':
            sql='insert into dnat(ruleid,in_if,src_addr,dst_addr,service,trans_to,port,log,status,description,token)  values(?,?,?,?,?,?,?,?,?,?,?)'
        elif type=='policy':
            sql='insert into policy(ruleid,src_zone,dst_zone,src_addr,dst_addr,service,action,log,schedule,status,description,token)  values(?,?,?,?,?,?,?,?,?,?,?,?)'
        elif type=='token':
            sql='insert into token(token) values(?);'
        elif type=='dstroute':
            sql='insert into dstroute(dstnet,gateway,metric,interface,description,token) values(?,?,?,?,?,?);'
        c.execute(sql,data)
        conn.commit()
        conn.close()
    #读取数据库内容
    def select_data(self,table,token):
        conn=sqlite3.connect('hillstone_covert_tool.db')
        c=conn.cursor()
        sql='select * from '+table+' where token='+token
        c.execute(sql)
        values=c.fetchall()
        conn.commit()
        conn.close()
        return values

    def select_address(self,addr,token):
        conn=sqlite3.connect('hillstone_covert_tool.db')
        c=conn.cursor()
        sql='select * from address where token='+token+' and addr_name='+addr
        c.execute(sql)
        values=c.fetchall()
        conn.commit()
        conn.close()
        return values
        
        

from db import *
import traceback
class Hillstone_config(db):
    def __init__(self):
        db.__init__(self)#实例化父类db

#########################生成配置###################################
    def create_hsconfig(self,token):
        self.m_textCtrl3.AppendText('开始生成配置....')
        self.hs_address(token)
        self.hs_service(token)
        self.hs_snat(token)
        self.hs_dnat(token)
        self.hs_policy(token)
        self.hs_dstroute(token)
        self.output.Enable()
        self.m_textCtrl3.AppendText('配置转换完成！')
    #生成山石地址配置
    def hs_address(self,token):
        try:
            values=self.select_data('address',token)
            for row in values:
                address='address '+row[1]+'\n'
                memberlist=row[3].split(',')
                memberip=''
                if row[2] in 'host':                
                    for ip in memberlist:
                        memberip+=' ip '+ip+'/32\n'
                elif row[2] in 'group':
                    for ip in memberlist:
                        memberip+=' member '+ip+'\n'                              
                if row[2] in 'subnet':                
                        memberip+=' ip '+memberlist[0]+' '+memberlist[1]+'\n'
                if row[2] in 'range':                
                        memberip+=' range '+memberlist[0]+' '+memberlist[1]+'\n'                    
                self.m_textCtrl2.AppendText(address+memberip+'exit\n')
        except:
            self.m_textCtrl3.AppendText('配置生成失败：'+row[1]+'\n')
            traceback.print_exc(file=open('address.log','w+'))#输出异常信息到文件               
    #生成山石服务配置       
    def hs_service(self,token):
        v=self.select_data('service',token)
        for row in v:
            if row[2] in 'group':
                servicename='servgroup '+row[1]+'\n'
                member=''
                memberlist=row[5].split(',')
                for s in memberlist:
                    member+=' member '+s+'\n'
                service=servicename+member+'exit\n'
            else:
                #判断是否有源端口
                if row[3]:
                    srcport=' src-port '+row[3]+' '+row[4]
                elif row[4]:
                    srcport=' src-port '+row[3]+' '+row[4]
                else:
                    srcport=''
                service='service '+row[1]+'\n '+row[2]+' dst-port '+row[5]+' '+row[6]+srcport+'\nexit\n'
            self.m_textCtrl2.AppendText(service)
    #生成山石snat配置
    def hs_snat(self,token):
        v=self.select_data('snat',token)
        for row in v:
            src_addr,src_addrname=self.hs_nat_address(row,'src')
            dst_addr,dst_addrname=self.hs_nat_address(row,'dst')
            if row[5]:
                eif=' eif '+row[5]
            else:
                eif=''
        
            snat='ip vrouter trust-vr\nsnatrule id '+row[1]+' from '+src_addrname+' to '+dst_addrname+' service '+row[4]+ eif+' trans_to address-book '+row[6]+' mode '+row[7]+' '+row[10]+'\nexit\n'  
            self.m_textCtrl2.AppendText(src_addr)
            self.m_textCtrl2.AppendText(dst_addr) 
            self.m_textCtrl2.AppendText(snat)    
    #创建nat对应的地址簿
    def hs_nat_address(self,row,type):
        if type=='src':
            n=2
        elif type=='dst':
            n=3
        addrlist=row[n].split(',')
        if len(addrlist)>1:           
            address='address nat_'+type+'_'+row[1]+'\n'
            addrname='nat_'+type+'_'+row[1]
            for addr in addrlist:
                address+=' member'+addr+'\n'
            address+='exit\n'
        else:
            address=''
            addrname=addrlist[0]
        return address,addrname
    
    #生成山石dnat配置
    def hs_dnat(self,token):
        v=self.select_data('dnat',token)
        for row in v:
            src_addr,src_addrname=self.hs_nat_address(row,'src')
            dst_addr,dst_addrname=self.hs_nat_address(row,'dst')
            if row[2]:
                inif=' eif '+row[2]
            else:
                inif=''
            if row[7]:
                port=' port '+row[7]
            else:
                port=''
            snat='ip vrouter trust-vr\ndnatrule id '+row[1]+' from '+src_addrname+' to '+dst_addrname+' service '+row[4]+ inif+' trans_to '+row[6]+' '+port+' '+row[9]+'\nexit\n'  
            self.m_textCtrl2.AppendText(src_addr)
            self.m_textCtrl2.AppendText(dst_addr) 
            self.m_textCtrl2.AppendText(snat)
            
     #生成山石策略配置，目前暂未做dnat对应策略的目标地址替换       
    def hs_policy(self,token):
        v=self.select_data('policy',token)
        for row in v:
            if row[2]:
                status=row[2]+'\n'
            else:
                status='' 
            rule='rule id '+row[1]+'\n '+status+' action '+row[3]+'\n src-zone '+row[4]+'\n dst-zone '+row[5]+'\n'           
            srclist=row[6].split(',')
            for src in srclist:
                rule+=' src-addr '+src+'\n'
            dstlist=row[7].split(',')
            for dst in dstlist:
                rule+=' dst-addr '+dst+'\n'
            serlist=row[8].split(',')
            for ser in serlist:
                rule+=' service '+ser+'\n'
            rule+='exit\n'
            self.m_textCtrl2.AppendText(rule)
    #生成山石的静态路由
    def hs_dstroute(self,token):
        v=self.select_data('dstroute',token)
        for row in v:
            dstroute='ip vroute trust-vr\n ip route '+row[1]+' '+row[4]+' '+row[2]+' '+row[3]+'\nexit\n'
            self.m_textCtrl2.AppendText(dstroute)


                    
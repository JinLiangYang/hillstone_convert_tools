# -*- coding: utf-8 -*- 
import traceback
import re
from db import * #继承数据库连接类的方法
#创建类
class Get_config(db):
    def __init__(self):
        db.__init__(self)#实例化父类db
  #主函数  
    def configtodb(self,source_config,vendor,token):
        source_config_list=source_config.split('\n')
        i=0
        self.m_textCtrl3.AppendText( '开始提取配置内容......\n')
        if vendor==0:
            self.m_textCtrl3.AppendText( '请选择需要转换配置的厂商\n')
            exit()
        while i<len(source_config_list):
            if vendor==5:
#############################天融信配置识别#################################################################################
                #根据正则进行匹配地址对象
                if re.match('^ID \d{3,5} define [b-z].{3,5} add name',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取地址对象......\n')
                    self.get_address(source_config_list[i],token)
                #提取地址组
                if re.match('^ID \d{3,5} define group_address add name',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取地址组......\n')
                    self.get_address(source_config_list[i],token)
                #提取服务和服务组
                if re.match('^ID \d{3,5} define .{0,6}service add name',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取服务对象......\n') 
                    self.get_service(source_config_list[i],token)
                if re.match('^ID \d{4,5} firewall policy',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取策略......\n') 
                    self.get_policy(source_config_list[i],token)                
                if re.match('^ID \d{3,5} nat policy add',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取NAT......\n') 
                    self.get_nat(source_config_list[i],token)
                if re.match('^network route add dst',source_config_list[i]):
                    #self.m_textCtrl3.AppendText( '正在提取NAT......\n') 
                    self.get_dstroute(source_config_list[i],token)
                #if re.match('^ object network \w{4,6} .{1,20}\r\n(  host address \S{1,100}\r\n)+',topseclist[i]):
                    #print(topseclist[i])
####################################H3C 配置识别#######################################################################
            if vendor==2:
                #提取地址
                if re.match('^object-group ip address',source_config_list[i]):
                    i=self.h3cv7_address(source_config_list,i,token)
                #提取服务
                if re.match('^object-group service',source_config_list[i]):
                    i=self.h3cv7_service(source_config_list,i,token)
                #提取静态路由
                if re.match('^ ip route-static',source_config_list[i]):
                    self.h3c_dstroute(source_config_list[i],token)                    
                    
            if vendor==3:                    
                if re.match('^ object network \w{4,6}',source_config_list[i]):
                    i=self.h3c_address(source_config_list,i,token)
                #提取服务
                if re.match('^ object service',source_config_list[i]):
                    i=self.h3c_service(source_config_list,i,token)
                #提取静态路由
                if re.match('^ ip route-static',source_config_list[i]):
                    self.h3c_dstroute(source_config_list[i],token)
                
####################################asa配置识别##########################################################################
            if vendor==1:
                if re.match('^object\S{0,6} network \S{1,100}',source_config_list[i]):
                    i=self.asa_address(source_config_list,i,token)
                if re.match('object-group service',source_config_list[i]):
                    i=self.asa_service(source_config_list,i,token)
                if re.match('access-list \S{1,100} extended', source_config_list[i]):
                    self.asa_policy(source_config_list[i],token)
###








####
#



 ##################################netsccreen配置识别##############################################################################           
            if vendor==6:
                #分类配置内容
                # if ('set service ' in source_config_list[i]):  # 转换服务
                #     i = transservice(source_config_list[i],i,token)
                # elif ('set' in words and 'interface' in words and 'dip' in words):  # 转换dip地址薄
                #     if (words[words.index('dip') + 1].isnumeric()):
                #         stra = words[words.index('dip')] + words[words.index('dip') + 1]
                #         strb = 'address ' + stra + '\n'
                #         strb = strb + ' range ' + words[words.index('dip') + 2] + ' ' + words[
                #             words.index('dip') + 3] + '\nexit\n'
                #         # print(stra)
                #         # break
                #         ed.writelines(strb)
                #     else:
                #         None
                #     i = i + 1
                # elif ('set' in words and 'interface' in words and 'mip' in words):  # 转换mip，包含snat和dnat
                #     # stra='MIP('+words[words.index('mip')+1]+')'
                #     stra = words[words.index('mip') + 1] + '/32'
                #     strb = 'address ' + stra + '\n'
                #     strb = strb + ' ip ' + words[words.index('mip') + 1] + '/32\nexit\n'
                #     # print(stra)
                #     # break
                #     ed.writelines(strb)  # strb中是mip地址薄
                #     strc = 'nat\nsnatrule from ' + words[words.index('mip') + 3] + '/32 to any service any eif ' + \
                #            words[words.index('mip') - 1] + ' trans-to address-book ' + stra + ' mode static\n'
                #     strc = strc + 'dnatrule from any to ' + stra + ' service any trans-to ' + words[
                #         words.index('mip') + 3] + '/32\nexit\n'
                #     strc = strc.replace('"', '')  # 将其中的双引号删除
                #     ed.writelines(strc)
                #     i = i + 1
                # elif ('set' in words and 'address' in words):  # 转换地址薄和地址组
                #     transaddrandgr(list)
                # elif ('set' in words and 'service' in words and 'group' in words):
                #     transservgr(list)
                #     # 转换服务组

                if ('set policy id ' in source_config_list[i]) and (' nat ' in source_config_list[i]):  # 转换带nat的安全策略
                    i = self.netscren_policy_nat(source_config_list, i,token)

                elif ('set policy id ' in source_config_list[i]):  # 转换安全策略
                    i = self.netscren_policy(source_config_list,i,token)
                # elif ('set' in words and 'scheduler' in words):
                #     transschedu(list)
                # pass
            
            i+=1
                
        self.m_textCtrl3.AppendText( '配置提取完成！\n')
        self.totran.Enable()#释放按钮



###################################netsccreen配置提取函数##########################################################
    def netscren_service(self):
        # 现在列表中第一个元素是access-list,第4个元素是permit,第5个元素是tcp/ip/udp/icmp，第6个元素是host/object-group（src-ip/src-addr）,第8个元素是host/object-group（dst-ip/dst-addr），
        # prewritin1='rule\n'
        # prewritin1=prewritin1+' action '+list[3]+'\n'
        # ---------------------------------------开始判断第5个元素------------------------------------------------------------------------
        global i
        stra = ''
        strdstport = ''
        strdstportstar = ''
        strdstportend = ''
        strsrcport = ''
        strsrcportstar = ''
        strsrcportend = ''
        words = list[i].split()  # 将第i+1行分割成一个个元素放在列表words中，list[i]是一个字符串(文件中的一行)
        # print(i+1)
        k = i
        y = 0
        #
        while (i > 0):  # 当+在当前行，且protocol在下一行时，就停止运行while中的语句
            k = k + 1
            words = list[k].split()  # 取下一行到words中，
            if ('+' not in words):
                y = 1
            if (y == 1):
                break
        # 此时list[k]中含有protocol或是最后一行，
        # print(k)
        words = list[i].split()
        m = words.index('service')  # 获得’‘索引值
        strservice = words[m + 1]  # 获得service名称
        stra = 'service ' + strservice + '\n'
        if ('tcp' in words):
            strprotocol = 'tcp'
        elif ('udp' in words):
            strprotocol = 'udp'
        else:
            ed.writelines(list[i])
            i = i + 1
            return 0
        if ('src-port' in words):
            n = words.index('src-port')
            strsrcport = words[n + 1]
            # print(strsrcport)
            tmplist = strsrcport.split('-')
            strsrcportstar = tmplist[0]
            strsrcportend = tmplist[1]
            strdstport = words[n + 3]
            tmplist = strdstport.split('-')
            strdstportstar = tmplist[0]
            strdstportend = tmplist[1]
        else:
            print('58')
        stra = 'service ' + strservice + '\n'
        stra = stra + ' ' + strprotocol + ' dst-port ' + strdstportstar + ' ' + strdstportend + ' src-port ' + strsrcportstar + ' ' + strsrcportend + '\n'

        i = i + 1
        while (i < k):
            words = list[i].split()  # 下一行
            if ('tcp' in words):
                strprotocol = 'tcp'
            elif ('udp' in words):
                strprotocol = 'udp'
            if ('src-port' in words):
                n = words.index('src-port')
                strsrcport = words[n + 1]
                tmplist = strsrcport.split('-')
                strsrcportstar = tmplist[0]
                strsrcportend = tmplist[1]
                strdstport = words[n + 3]
                tmplist = strdstport.split('-')
                strdstportstar = tmplist[0]
                strdstportend = tmplist[1]
                stra = stra + ' ' + strprotocol + ' dst-port ' + strdstportstar + ' ' + strdstportend + ' src-port ' + strsrcportstar + ' ' + strsrcportend + '\n'
            else:
                print('49')
            i = i + 1
        # print(i)
        stra = stra + 'exit\n'
        ed.writelines(stra)
        return 0



    def netscren_policy_nat(self,a_string,j,token):			#转换策略				#list是words,

        #现在列表中第一个元素是access-list,第4个元素是permit,第5个元素是tcp/ip/udp/icmp，第6个元素是host/object-group（src-ip/src-addr）,第8个元素是host/object-group（dst-ip/dst-addr），
        #prewritin1='rule\n'
        #prewritin1=prewritin1+' action '+list[3]+'\n'
        #---------------------------------------开始判断第5个元素------------------------------------------------------------------------

        words = a_string[j].split()        #将第i行分割成一个个元素放在列表words中，list[i]是一个字符串(文件中的一行)
        k = j + 1
        m = words.index('id')  # 获得’id‘索引值
        ruleid = words[m + 1]  # 策略id是多少
        p = words.index('from')  # 获得’from‘索引值
        src_zone = words[p + 1]  # 策略源域
        dst_zone = words[p + 3]  # 策略目的域
        src_addr = words[p + 4]  # 策略源地址
        dst_addr = words[p + 5]  # 策略目的地址
        service = words[p + 6]  # 策略的服务  # 将ICMP-ANY等，替换为ICMP
        # for l in range(len(servlista)):
        #     if (service == servlista[l]):
        #         service = servlistb[l]
        # servlist = []
        # servlist.append(service)

        log = ''
        schedule = ''
        status = ''
        description = ''

        while (not('exit' in words)):
            words = a_string[j].split()
            if ('src' in words and 'dip-id' in words and 'dst' in words):
                # set policy id 1025 from "Untrust" to "Trust"  "046-网络贷款-广州优迈测试" "046-网络贷款-总行测试_VO" "S_HTTP/HTTPS/FTP" nat src dip-id 16 dst ip 22.188.12.104 permit schedule "20140825-1125" log

                q = words.index('dst')  # 获得’dst‘索引值
                strdstip = words[q + 2]  # 获得内网服务器ip
                action = words[q + 3]  # 策略的动作
                r = words.index('src')  # 获得’src‘索引值
                strdipid = words[r + 2]  # 获得’dip-id‘号
                if ('schedule' in words):
                    n = words.index('schedule')
                    schedule = words[n + 1]

                if ('name' in words):
                    n = words.index('name')
                    description = words[n + 1]

                # policy_tuple = ruleid,src_zone,dst_zone,src_addr,dst_addr,service,action,log,schedule,status,description,token
                # self.insert_data('policy',policy_tuple)

                j += 1
                words = a_string[j].split()
                while (not('exit' in words)):  ################################################################
                    words = a_string[j].split()
                    if ('policy' in words and 'disable' in words):
                        status = 'disable'
                    elif ('src-address' in words):
                        t = words.index('src-address')
                        src_addr +=  ',' + words[t + 1]
                        # policy_tuple = ruleid, '', '', src_addr, '', '', '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('dst-address' in words):
                        t = words.index('dst-address')
                        dst_addr += ',' + words[t + 1]
                        # policy_tuple = ruleid, '', '', '', dst_addr, '', '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('service' in words):
                        t = words.index('service')
                        service += ',' + words[t + 1]
                        # 将ICMP-ANY等，替换为ICMP
                        # for l in range(len(servlista)):
                        #     if (strservi == servlista[l]):
                        #         strservi = servlistb[l]
                        # servlist.append(strservi)
                        # policy_tuple = ruleid, '', '', '', '', service, '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('session-init' in words):
                        log = 'YES'

                    j += 1

                policy_tuple = ruleid,src_zone,dst_zone,src_addr,dst_addr,service,action,log,schedule,status,description,token
                self.insert_data('policy', policy_tuple)

            elif ('src' in words and 'dst' in words):
                # set policy id 1099 from "Untrust" to "Trust"  "044-省烟草结算-烟草服务器" "T-中行SIT测试机_VOUT" "TCP:5138/PING" nat src dst ip 22.136.66.112 permit schedule "20150909-1231" log
                q = words.index('dst')  # 获得’dst‘索引值
                strdstip = words[q + 2]  # 获得内网服务器ip
                action = words[q + 3]  # 策略的动作
                r = words.index('src')  # 获得’src‘索引值
                # strdipid = words[r + 2]  # 获得’dip-id‘号
                if ('schedule' in words):
                    n = words.index('schedule')
                    schedule = words[n + 1]
                if ('name' in words):
                    n = words.index('name')
                    description = words[n + 1]
                policy_tuple = ruleid, src_zone, dst_zone, src_addr, dst_addr, service, action, log, schedule, status, description, token
                self.insert_data('policy', policy_tuple)

                j += 1
                words = a_string[j].split()
                while (not('exit' in words)):  ################################################################
                    words = a_string[j].split()
                    if ('policy' in words and 'disable' in words):
                        status = 'disable'
                    elif ('src-address' in words):
                        t = words.index('src-address')
                        src_addr = words[t + 1]
                        policy_tuple = ruleid, '', '', src_addr, '', '', '', '', '', '', '', ''
                        self.insert_data('policy', policy_tuple)
                    elif ('dst-address' in words):
                        t = words.index('dst-address')
                        dst_addr = words[t + 1]
                        policy_tuple = ruleid, '', '', '', dst_addr, '', '', '', '', '', '', ''
                        self.insert_data('policy', policy_tuple)
                        # print(strnat)
                    elif ('service' in words):
                        t = words.index('service')
                        service = words[t + 1]
                        # for l in range(len(servlista)):
                        #     if (strservi == servlista[l]):
                        #         strservi = servlistb[l]
                        # servlist.append(strservi)
                        policy_tuple = ruleid, '', '', '', '', service, '', '', '', '', '', ''
                        self.insert_data('policy', policy_tuple)
                    elif ('session-init' in words):
                        log = 'YES'

                    j += 1

                policy_tuple = ruleid, '', '', '', '', '', '', log, '', status, '', token
                self.insert_data('policy', policy_tuple)
                # stra=stra+'exit\n'

            elif ('dst' in words):
                #nat dst ip 9.72.48.133 permit
                q = words.index('dst')  # 获得’dst‘索引值
                strdstip = words[q + 2]  # 获得内网ip
                stract = words[q + 3]  # 策略的动作
                if ('schedule' in words):
                    n = words.index('schedule')
                    strsche = words[n + 1]
                    stra = '\n\nrule id ' + strid + '\n src-zone ' + strsrcz + '\n dst-zone ' + strdstz + '\n src-addr ' + strsrc + '\n dst-addr ' + strdst + '\n service ' + strservi + '\n action ' + stract + '\n schedule ' + strsche + '\n'
                else:
                    stra = '\n\nrule id ' + strid + '\n src-zone ' + strsrcz + '\n dst-zone ' + strdstz + '\n src-addr ' + strsrc + '\n dst-addr ' + strdst + '\n service ' + strservi + ' \n action ' + stract + '\n'
                if ('name' in words):
                    n = words.index('name')
                    descrip = words[n + 1]
                    stra += ' description ' + descrip + '\nexit\n'
                else:
                    stra += 'exit\n'
                i = i + 1
                words = list[i].split()

                while (not('exit' in words)):  ################################################################
                    if ('policy' in words and 'disable' in words):
                        stra = stra + 'rule id ' + strid + '\n'
                        stra = stra + ' disable\nexit\n'
                    elif ('src-address' in words):
                        t = words.index('src-address')
                        strsrc = words[t + 1]
                        stra = stra + '\nrule id ' + strid + '\n src-addr ' + strsrc + '\nexit\n'
                        strnat += 'address ' + srcaddr_name + '\n'
                        strnat += ' member ' + strsrc + '\n' + \
                                  'exit\n'
                    elif ('dst-address' in words):
                        t = words.index('dst-address')
                        strdst = words[t + 1]
                        stra = stra + '\nrule id ' + strid + '\n dst-addr ' + strdst + '\nexit\n'
                        strnat += 'address ' + dstaddr_name + '\n' + \
                                  ' member ' + strdst + '\n' + \
                                  'exit\n'
                        # print(strnat)
                    elif ('service' in words):
                        t = words.index('service')
                        strservi = words[t + 1]
                        # for l in range(len(servlista)):
                        #     if (strservi == servlista[l]):
                        #         strservi = servlistb[l]
                        # servlist.append(strservi)
                        stra = stra + '\nrule id ' + strid + '\n service ' + strservi + '\nexit\n'
                    elif ('session-init' in words):
                        stra = stra + '\nrule id ' + strid + '\n log session-start\nexit\n'
                    i = i + 1
                    words = list[i].split()


            elif ('src' in words and 'dip-id' in words):
#nat     src dip-id 158 permit schedule "TO20181231" log
                q = words.index('dip-id')  # 获得’dip-id‘索引值
                strdipid = words[q + 1]  # 获得dip号
                action = words[q + 2]  # 策略的动作
                if ('schedule' in words):
                    n = words.index('schedule')
                    schedule = words[n + 1]
                if ('name' in words):
                    n = words.index('name')
                    description = words[n + 1]

                # policy_tuple = ruleid, src_zone, dst_zone, src_addr, dst_addr, service, action, log, schedule, status, description, token
                # self.insert_data('policy', policy_tuple)

                j += 1
                words = a_string[j].split()
                while (not('exit' in words)):  ################################################################
                    words = a_string[j].split()
                    if ('policy' in words and 'disable' in words):
                        status = 'disable'
                    elif ('src-address' in words):
                        t = words.index('src-address')
                        src_addr += ',' + words[t + 1]
                        # policy_tuple = ruleid, '', '', src_addr, '', '', '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('dst-address' in words):
                        t = words.index('dst-address')
                        dst_addr += ',' + words[t + 1]
                        # policy_tuple = ruleid, '', '', '', dst_addr, '', '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('service' in words):
                        t = words.index('service')
                        service += ',' + words[t + 1]
                        # 将ICMP-ANY等，替换为ICMP
                        # for l in range(len(servlista)):
                        #     if (strservi == servlista[l]):
                        #         strservi = servlistb[l]
                        # servlist.append(strservi)
                        # policy_tuple = ruleid, '', '', '', '', service, '', '', '', '', '', ''
                        # self.insert_data('policy', policy_tuple)

                    elif ('session-init' in words):
                        log = 'YES'
                    j += 1

                policy_tuple = ruleid, src_zone, dst_zone, src_addr, dst_addr, service, action, log, schedule, status, description, token
                self.insert_data('policy', policy_tuple)

            elif ('src' in words):
                # set policy id 606 from "DMZ" to "Trust"  "018-大/小额支付系统-测试机1" "018-大小额支付-总行演练测试机" "TCP:1414-1415/PING" nat src permit log

                q = words.index('src')  # 获得’src‘索引值
                stract = words[q + 1]  # 策略的动作
                if ('schedule' in words):
                    n = words.index('schedule')
                    strsche = words[n + 1]
                    stra = '\n\nrule id ' + strid + '\n src-zone ' + strsrcz + '\n dst-zone ' + strdstz + '\n src-addr ' + strsrc + '\n dst-addr ' + strdst + '\n service ' + strservi + '\n action ' + stract + '\n schedule ' + strsche + '\n'
                else:
                    stra = '\n\nrule id ' + strid + '\n src-zone ' + strsrcz + '\n dst-zone ' + strdstz + '\n src-addr ' + strsrc + '\n dst-addr ' + strdst + '\n service ' + strservi + ' \n action ' + stract + '\n'
                if ('name' in words):
                    n = words.index('name')
                    descrip = words[n + 1]
                    stra += ' description ' + descrip + '\nexit\n'
                else:
                    stra += 'exit\n'
                i = i + 1
                words = list[i].split()
                while (not('exit' in words)):  ################################################################
                    if ('policy' in words and 'disable' in words):
                        stra = stra + 'rule id ' + strid + '\n'
                        stra = stra + ' disable\nexit\n'
                    elif ('src-address' in words):
                        t = words.index('src-address')
                        strsrc = words[t + 1]
                        strnat += 'address ' + srcaddr_name + '\n'
                        strnat += ' member ' + strsrc + '\n' + \
                                  'exit\n'
                    elif ('dst-address' in words):
                        t = words.index('dst-address')
                        strdst = words[t + 1]
                        stra = stra + '\nrule id ' + strid + '\n dst-addr ' + strdst + '\nexit\n'
                        strnat += 'address ' + dstaddr_name + '\n' + \
                                  ' member ' + strdst + '\n' + \
                                  'exit\n'
                        # print(stra)
                    elif ('service' in words):
                        t = words.index('service')
                        strservi = words[t + 1]
                        for l in range(len(servlista)):
                            if (strservi == servlista[l]):
                                strservi = servlistb[l]
                        servlist.append(strservi)

                        stra = stra + '\nrule id ' + strid + '\n service ' + strservi + '\nexit\n'

                    elif ('session-init' in words):
                        stra = stra + '\nrule id ' + strid + '\n log session-start\nexit\n'
                    i = i + 1
                    words = list[i].split()
                # stra=stra+'exit\n'
                if len(servlist)>1:
                    servgroup_name = 'servg-' + strid
                    servgroup = 'servgroup ' + servgroup_name + '\n'
                    for service in servlist:
                        servgroup += ' service ' + service + '\n'
                    servgroup += 'exit\n'

                    strnat += servgroup
                    strnat += 'nat\n snatrule id ' + strid + ' from ' + srcaddr_name + ' to ' + dstaddr_name + ' service ' + servgroup_name + ' eif ethernet0/2' + ' trans-to eif-ip mode dynamicport sticky\nexit\n'
                else:
                    strnat += 'nat\n snatrule id ' + strid + ' from ' + srcaddr_name + ' to ' + dstaddr_name + ' service ' + servlist[0] + ' eif ethernet0/2' + ' trans-to eif-ip mode dynamicport sticky\nexit\n'

            # 写入
            else:
                None
            j += 1
        else:
        #print(list[k])#此时list[k]这一行是exit
        #这一条策略：list[i]是第一行，list[k]是最后一行
        #print(int)
            return j

        return j




    def netscren_policy(self,a_string,j,token):			#转换策略				#list是words,
                #现在列表中第一个元素是access-list,第4个元素是permit,第5个元素是tcp/ip/udp/icmp，第6个元素是host/object-group（src-ip/src-addr）,第8个元素是host/object-group（dst-ip/dst-addr），
    #prewritin1='rule\n'
    #prewritin1=prewritin1+' action '+list[3]+'\n'
    #---------------------------------------开始判断第5个元素------------------------------------------------------------------------
        words=a_string[j].split()        #将第i行分割成一个个元素放在列表words中，list[i]是一个字符串(文件中的一行)
        k = j
        while (not('exit' in words)):
            k = k + 1
            words = a_string[k].split()
        # else:
        # #print(list[k])#此时list[k]这一行是exit
        # #这一条策略：list[i]是第一行，list[k]是最后一行
        # #print(int)
        #     k += 1
        words = a_string[j].split()
        m = words.index('id')#获得’id‘索引值
        ruleid = words[m+1]#策略id是多少
        p = words.index('from')#获得’from‘索引值
        src_zone = words[p+1]#策略源域
        dst_zone = words[p+3]#策略目的域
        src_addr = words[p+4]#策略源地址
        dst_addr = words[p+5]#策略目的地址
        service = words[p+6]#策略的服务

        # for l in range(len(servlista)):
        #     if(strservi==servlista[l]):
        #         strservi=servlistb[l]
        action = words[p+7]#策略的动作

        log = ''
        schedule = ''
        status = ''
        description = ''

        if ('schedule' in words):
            n=words.index('schedule')
            schedule = words[n+1]
        if ('name' in words):
            n=words.index('name')
            description = words[n+1]

        # policy_tuple = ruleid, src_zone, dst_zone, src_addr, dst_addr, service, action, log, schedule, status, description, token
        # self.insert_data('policy', policy_tuple)

        j += 1
        while ( j < k ):
            words = a_string[j].split()
            if ('policy' in words and 'disable' in words):
                status = 'disable'
            elif ('src-address' in words):
                t = words.index('src-address')
                src_addr += ',' + words[t + 1]
                # policy_tuple = ruleid, '', '', src_addr, '', '', '', '', '', '', '', token
                # self.insert_data('policy', policy_tuple)

            elif ('dst-address' in words):
                t = words.index('dst-address')
                dst_addr += ',' + words[t + 1]
                # policy_tuple = ruleid, '', '', '', dst_addr, '', '', '', '', '', '', token
                # self.insert_data('policy', policy_tuple)

            elif ('service' in words):
                t = words.index('service')
                service += ',' + words[t + 1]
                # 将ICMP-ANY等，替换为ICMP
                # for l in range(len(servlista)):
                #     if (strservi == servlista[l]):
                #         strservi = servlistb[l]
                # servlist.append(strservi)
                # policy_tuple = ruleid, '', '', '', '', service, '', '', '', '', '', token
                # self.insert_data('policy', policy_tuple)

            elif ('session-init' in words):
                log = 'YES'
            j += 1
        policy_tuple = ruleid, src_zone, dst_zone, src_addr, dst_addr, service, action, log, schedule, status, description, token
        self.insert_data('policy', policy_tuple)
        return j


    ###########################天融信配置提取函数#########################################################################
    #提取地址对象(包括host、range、subnet、group_address)

    def get_address(self,line,token):
        try:
            linelist=line.split()
            addr_name=linelist[6]
            type=linelist[3]
            if type in ['host','group_address']:
                ip=linelist[8][1:]
                h=9
                while h<len(linelist):
                    if "'" not in linelist[h]:
                        ip+=','+linelist[h]
                    else:
                        break
                    h+=1                
            else:
                ip=linelist[8]+','+linelist[10]
            if type=='group_address':
                type='group'
            addrtuple=addr_name,type,ip,'topsec',token
            self.insert_data('address',addrtuple)#写入数据库的address表
        except Exception as e :
            self.m_textCtrl3.AppendText( '未转换的配置：'+line+'\n')
            traceback.print_exc(file=open('host'+'.log','w+'))#输出异常信息到文件

            
#提取服务对象(包括service、group_serivce)
    def get_service(self,line,token):
        try:
            linelist=line.split()
            serv_name=linelist[6]
            #判断协议类型或服务组
            if linelist[8]=='6':
                type='tcp'
            elif linelist[8]=='17':
                type='udp'
            elif linelist[8]=='1':
                type='icmp'
            elif linelist[3]=='group_service':
                type='group'
            else:
                type='unknow'
            #判断是服务还是服务组
            if linelist[3]=='service':
                dstport_start=linelist[10]
            else:
                dstport_start=linelist[8][1:]
                h=9
                while h<len(linelist):
                    if "'" not in linelist[h]:
                        port_start+=','+linelist[h]
                    else:
                        break
                    h+=1
            #判断是否有结束端口     
            if 'port2' in linelist:
                dstport_end=linelist[linelist.index('port2')+1]
            else:
                dstport_end=''
            #开始写数据库    
            servtuple=serv_name,type,'','',dstport_start,dstport_end,'topsec',token
            self.insert_data('service',servtuple)
        except:
            self.m_textCtrl3.AppendText( '未转换的配置：'+line+'\n')
            traceback.print_exc(file=open('service.log','w+'))#输出异常信息到文件
            
   #提取nat和policy中的源地址、目标地址和服务
    def get_element(self,find,linelist):
        if find not in linelist:#没有匹配的字段设置为any
            member='any'
        else:
            s=linelist.index(find)+1
            member=linelist[s][1:]
            while s<len(linelist):
                s+=1
                if linelist[s]=="'":
                    break
                else:
                    member+=','+linelist[s]
        return member
    #nat提取结果写入数据库            
    def get_nat(self,line,token):
        try:
            linelist=line.split()
            ruleid=linelist[1]
            srcaddr=self.get_element('orig_src',linelist)
            dstaddr=self.get_element('orig_dst',linelist)
            service=self.get_element('orig_service',linelist)
            #判断是否禁用
            if 'enable no' in line:
                status='disable'
            else:
                status=''
            #判断pat类型
            if 'pat no' in line:
                pat='static'
            else:
                pat='dynamicport'
            log=''
            
            #判断转换类型
            #判断是否为snat
            if 'trans_src' in line:
                trans_to=linelist[linelist.index('trans_src')+1]
                eif=''
                sticky=''                
                snattuple=ruleid,srcaddr,dstaddr,service,eif,trans_to,pat,sticky,log,status,'topsec',token
                self.insert_data('snat',snattuple)
            #判断是否为dnat
            if 'trans_dst' in line:
                trans_to=linelist[linelist.index('trans_dst')+1]
                in_if=''
                eif=''
                if 'trans_service' in line:
                    port=linelist[linelist.index('trans_service')+1]
                else:
                    port=''
                dnattuple=ruleid,in_if,srcaddr,dstaddr,service,trans_to,port,log,status,'topsec',token
                self.insert_data('dnat',dnattuple)
            
        except Exception as e:
            print('未转换配置：'+line+'\n')
            traceback.print_exc(file=open('nat.log','w+'))#输出异常信息到文件
 
 #提取策略内容到数据库
    def get_policy(self,line,token):
        try:           
            linelist=line.split()
            ruleid=linelist[1]
            src_zone=self.get_element('srcarea',linelist)
            dst_zone=self.get_element('dstarea',linelist)
            src_addr=self.get_element('src',linelist)
            dst_addr=self.get_element('dst',linelist)
            service=self.get_element('service',linelist)
            #判断是否禁用
            if 'enable no' in line:
                status='disable'
            else:
                status=''
            #判断策略是否动作
            if linelist[linelist.index('action')+1] in ['accept','connect']:
                action='permit'
            elif linelist[linelist.index('action')+1]=='deny':
                action='deny'
            else:
                action=''
            #判断是否启用日志           
            if 'log on' in line:
                log='yes'
            else:
                log=''
            schedule='' 
            policytuple=ruleid,src_zone,dst_zone,src_addr,dst_addr,service,action,log,schedule,status,'topsec',token
            self.insert_data('policy',policytuple)
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+line+'\n')
            traceback.print_exc(file=open('policy.log','w+'))#输出异常信息到文件
    #提取路由配置并写入到数据库
    def get_dstroute(self,line,token):
        try:
            linelist=line.split()
            dstnet=linelist[4]
            gw=linelist[6]
            if re.match('dev eth\d{1,2}',line):
                interface=linelist[linelist.index('dev')+1]
            else:
                interface=''
            metric=linelist[8]
            rid=linelist[linelist.index('id')+1]
            dstroute_tuple=dstnet,gw,metric,interface,rid,token
            self.insert_data('dstroute',dstroute_tuple)
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+line+'\n')
            traceback.print_exc(file=open('dstroute.log','w+'))#输出异常信息到文件
 ############################天融信结束######################################################################
 
 
    #网上找的一个子网掩码转换为长度的函数
    def exchange_mask(self,mask):
        # 计算二进制字符串中 '1' 的个数
        count_bit = lambda bin_str: len([i for i in bin_str if i=='1'])
    
        # 分割字符串格式的子网掩码为四段列表
        mask_splited = mask.split('.')
    
        # 转换各段子网掩码为二进制, 计算十进制
        mask_count = [count_bit(bin(int(i))) for i in mask_splited]
        mask_len=sum(mask_count)    
        return   str(mask_len)
    
    #反掩码转掩码函数
    def wildcard_mask(self,wildcard):
        masklist=wildcard.split('.')
        mask=''
        for m in masklist:
            n=255-int(m)
            mask+=str(n)+'.'

        return mask[:-1]
######
        
    
 ##############################H3C comware v7配置提取##################################################           
    #v7平台地址簿提取
    def h3cv7_address(self,filelist,l,token):
        try:
            fileline=filelist[l].split()
            addr_name=fileline[3]
            while l<len(filelist):
                l+=1
                subline=filelist[l].split()
                if re.match('^ \d{1,3} network host address',filelist[l]):
                    ip=subline[4]
                    type='host'
                elif re.match('^ \d{1,3} network subnet',filelist[l]):
                    ip=subline[3]+','+subline[4]
                    type='subnet'
                elif re.match('^ \d{1,3} network range',filelist[l]):
                    ip=subline[3]+','+subline[4]
                    type='range'
                elif filelist[l]=='':
                    continue
                elif filelist[l]=='#':
                    l-=1
                    break
                addr_tuple=addr_name,type,ip,'h3cv7_address',token
                self.insert_data('address',addr_tuple)
            return l
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+filelist[l]+'\n')
            traceback.print_exc(file=open('address.log','a+'))#输出异常信息到文件
        return l
    #v7平台服务簿提取
    def h3cv7_service(self,filelist,l,token):
        try:
            fileline=filelist[l].split()
            service_name=fileline[2]
            while l<len(filelist):
                l+=1
                subline=filelist[l].split()
                if re.match('^ \d{1,3} service \w{1,3} destination eq',filelist[l]):
                    dstport_start=subline[5]
                    dstport_end=''
                    type=subline[2]
                elif re.match('^ \d{1,3} service \w{1,3} destination gt',filelist[l]):
                    dstport_start=subline[5]
                    dstport_end='65535'
                    type=subline[2]
                elif re.match('^ \d{1,3} service \w{1,3} source gt',filelist[l]):
                    srcport_start=subline[5]
                    srcport_start='65535'
                    dstport_start='0'
                    dstport_end='65535'
                    type=subline[2]
                elif re.match('^ \d{1,3} service \w{1,3} destination range',filelist[l]):
                    dstport_start=subline[5]
                    dstport_end=subline[6]
                    type=subline[2]
                elif re.match('^ \d{1,3} service icmp',filelist[l]):
                    dstport_start=''
                    dstport_end=''
                    type=subline[2]
                elif filelist[l]=='':
                    continue
                elif filelist[l]=='#':
                    l-=1
                    break
    
                service_tuple=service_name,type,'','',dstport_start,dstport_end,'h3cv7_service',token
                self.insert_data('service',service_tuple)
            return l
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+filelist[l]+'\n')
            traceback.print_exc(file=open('service.log','a+'))#输出异常信息到文件
        return l

    #地址簿提取
    def h3c_address(self,filelist,l,token):
        fileline=filelist[l].split()
        addr_name=fileline[3]

        while l<len(filelist):
            l+=1
            subline=filelist[l].split()
            if re.match('^  host address',filelist[l]):
                ip=subline[2]
                type='host'
            elif re.match('^  subnet',filelist[l]):
                ip=subline[1]+','+self.wildcard_mask(subline[2])
                type='subnet'
            elif re.match('^  range',filelist[l]):
                ip=subline[1]+','+subline[2]
                type='range'
            else:
                l-=1
                break
            addr_tuple=addr_name,type,ip,'h3c_address',token
            self.insert_data('address',addr_tuple)
        return l

    #服务簿转换函数
    def h3c_service(self,filelist,l,token):
        try:
            fileline=filelist[l].split()
            service_name=fileline[(fileline.index('service'))+1]            
            while l<len(filelist):
                l+=1
                subline=filelist[l].split()
                type=subline[1]
                #判断服务配置场景
                if re.match('^  service \w{3} destination-port \d{1,5}',filelist[l]):
                    srcport_start=''
                    srcport_end=''
                    dstport_start=subline[3]
                    dstport_end=''
                elif re.match('^  service \w{3} destination-port \d{1,5} \d{1,5}',filelist[l]):
                    srcport_start=''
                    srcport_end=''
                    dstport_start=subline[3]
                    dstport_end=subline[4]
                elif re.match('^  service \w{3} source-port \d{1,5} \d{1,5} destination-port \d{1,5}',filelist[l]):
                    srcport_start=subline[3]
                    srcport_end=subline[4]
                    dstport_start=subline[6]
                    dstport_end=''
                elif re.match('^  service \w{3} source-port \d{1,5} \d{1,5} destination-port \d{1,5} \d{1,5}',filelist[l]):
                    srcport_start=subline[3]
                    srcport_end=subline[4]
                    dstport_start=subline[6]
                    dstport_end=subline[7]
                elif re.match('^  service \w{3} source-port \d{1,5} destination-port \d{1,5} \d{1,5}',filelist[l]):
                    srcport_start=subline[3]
                    srcport_end=''
                    dstport_start=subline[5]
                    dstport_end=subline[6]
                else:
                    l-=1
                    break
                service_tuple=service_name,type,srcport_start,srcport_end,dstport_start,dstport_end,'h3c_service',token
                self.insert_data('service',service_tuple)
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+filelist[l]+'\n')
            traceback.print_exc(file=open('service.log','w+'))#输出异常信息到文件
        return l
    #转换静态路由
    def h3c_dstroute(self,line,token):
        try:
            linelist=line.split()
            dstnet=linelist[2]+'/'+self.exchange_mask(linelist[3])
            metric=''
            rid=''
            #判断路由是否指定接口
            if re.match('^ ip route-static \S{1,100} \S{1,100} GigabitEthernet\d/\d',line):
                gw=linelist[5]
                interface=linelist[4]             
            else:
                gw=linelist[4]
                interface=''           
            dstroute_tuple=dstnet,gw,metric,interface,rid,token
            self.insert_data('dstroute',dstroute_tuple)
        except:
            self.m_textCtrl3.AppendText('未转换配置：'+line+'\n')
            traceback.print_exc(file=open('dstroute.log','w+'))#输出异常信息到文件            
        return 0
 
 
 #################################思科配置提取######################################################################
    #提取地找对象（地址、地址组、地址范围、子网）
    def asa_address(self,filelist,l,token):
        try:
            fileline=filelist[l].split()
            addr_name=fileline[2]
            ip=''
            type=''
            while l<len(filelist):
                l+=1
                subline=filelist[l].split()
                if re.match('^ host',filelist[l]):
                    ip+=subline[1]+','
                    type='host'
                elif re.match('^ subnet',filelist[l]):
                    ip=subline[1]+','+subline[2]
                    type='subnet'
                elif re.match('^ range',filelist[l]):
                    ip=subline[1]+','+subline[2]
                    type='range'
                elif re.match('^ network-object object',filelist[l]):
                    ip+=subline[2]+','
                    type='group'
                else:
                    l-=1
                    break
            if ip[-1:]==',':
                ip=ip[:-1]
            
            addr_tuple=addr_name,type,ip,'asa_address',token
            self.insert_data('address',addr_tuple)
            return l
        except:
            self.m_textCtrl3.AppendText('提取失败的配置：'+filelist[l]+'\n')
            traceback.print_exc(file=open('address.log','w+'))#输出异常信息到文件         
        return l
 
    #提取服务（服务组）    
    def asa_service(self,filelist,l,token):
        try:
            fileline=filelist[l].split()
            serv_name=fileline[2]
            port=''
            while l<len(filelist):
                l+=1
                subline=filelist[l].split()
                if re.match('^ port-object \S{2,5}',filelist[l]):
                    port+=fileline[3]+'-'+subline[2]+','
                else:
                    l-=1
                    break
            if port[-1:]==',':
                port=port[:-1]
            serv_tuple=serv_name,'group','','',port,'','asa_service',token
            self.insert_data('service',serv_tuple)
            return l
        except:
            self.m_textCtrl3.AppendText('提取失败的配置：'+filelist[l]+'\n')
            traceback.print_exc(file=open('service.log','w+'))#输出异常信息到文件         
        return l
     
    #策略提取
    def asa_policy(self,line,token):
        try:
            linelist=line.split()
            action=linelist[3]
            description=linelist[1]
            #print(line)
            if re.match('^access-list \S{1,30} extended \w{4,6} \w{2,3} \S{4,15} \S{1,100} \S{4,15} \S{1,100} ',line):
                #判断源地址类型
                if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',linelist[5]):
                    src=linelist[5]+'/'+linelist[6]
                else:
                    src=linelist[6]
                #判断目标地址类型  
                if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',linelist[7]):
                    dst=linelist[7]+'/'+linelist[8]
                else:
                    dst=linelist[8]
                if len(linelist)>9:
                    if linelist[9]=='eq':
                        service=linelist[4]+'-'+linelist[10]
                    elif linelist=='range':
                        service=linelist[4]+'-'+linelistp[10]+'-'+linelist[11]
                    else:
                        service=linelist[10]
                else:
                    service='any'
            
            if re.match('^access-list \S{1,30} extended \w{4,6} \w{2,3} any \S{4,100} \S{1,100} ',line):
                src=linelist[5]
                #判断目标地址类型  
                if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',linelist[6]):
                    dst=linelist[6]+'/'+linelist[7]
                else:
                    dst=linelist[7]
                
                #判断是否有端口
                if len(linelist)>8:
                    if linelist[8]=='eq':
                        service=linelist[4]+'-'+linelist[9]
                    elif linelist=='range':
                        service=linelist[4]+'-'+linelistp[9]+'-'+linelist[10]
                    else:
                        service=linelist[9]
                else:
                    service='any'
                    
            if re.match('^access-list \S{1,30} extended \w{4,6} \w{2,3} \S{4,100} \S{1,100} any',line):
                
                #判断源地址类型
                if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',linelist[5]):
                    src=linelist[5]+'/'+linelist[6]
                else:
                    src=linelist[6]
                #判断目标地址类型  
                dst=linelist[7]
                #判断是否有端口
                if len(linelist)>8:
                    if linelist[8]=='eq':
                        service=linelist[4]+'-'+linelist[9]
                    elif linelist=='range':
                        service=linelist[4]+'-'+linelistp[9]+'-'+linelist[10]
                    else:
                        service=linelist[9]
                else:
                    service='any'
            if description=='PDS-INSIDE-ACL':
                srczone='inside'
                dstzone='outside'
            elif description=='PDS-OUTSIDE-ACL':
                srczone='outside'
                dstzone='inside'
            else:
                srczone=''
                dstzone=''
            policy_tuple='',srczone,dstzone,src,dst,service,action,'','','',description,token
            self.insert_data('policy',policy_tuple)
        except:
            self.m_textCtrl3.AppendText('提取失败的配置：'+line+'\n')
            traceback.print_exc(file=open('policy.log','a+'))#输出异常信息到文件
 

              
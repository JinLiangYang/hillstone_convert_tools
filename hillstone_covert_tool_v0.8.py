# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import threading
import os
import datetime
import re
from get_config import *
import urllib.request
from hsconfig import *
import webbrowser



#######################pannel转换工具程序界面类#######################################
class covert_toolui ( wx.Panel ,Get_config,Hillstone_config):

	def __init__( self, parent ):
		Get_config.__init__(self)#实例化父类，后面会调用到父类的一些方法
		Hillstone_config.__init__(self)
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1100,680), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
				
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		tool_gbSizer = wx.GridBagSizer( 0, 0 )
		tool_gbSizer.SetFlexibleDirection( wx.BOTH )
		tool_gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.choice_source_file = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"选择需要转换的配置文件", u"*.*", wx.DefaultPosition, wx.Size( 650,-1 ), wx.FLP_DEFAULT_STYLE )
		tool_gbSizer.Add( self.choice_source_file, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )

		choice_typeChoices = [ u"选择厂商",u"cisco", u"H3Cv7",u"H3Cv5", u"迪普", u"天融信", u"netscreen" ]
		self.choice_type= wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_typeChoices, 0 )
		self.choice_type.SetSelection( 2 )
		tool_gbSizer.Add( self.choice_type, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		self.get_todb = wx.Button( self, wx.ID_ANY, u"提取配置", wx.DefaultPosition, wx.DefaultSize, 0 )
		tool_gbSizer.Add( self.get_todb, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		self.totran = wx.ToggleButton( self, wx.ID_ANY, u"开始转换", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.totran.Enable( False )
		tool_gbSizer.Add( self.totran, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		self.output = wx.Button( self, wx.ID_ANY, u"导出配置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.output.Enable( False )	
		tool_gbSizer.Add( self.output, wx.GBPosition( 1, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,300 ), wx.TE_MULTILINE )
		gbSizer2.Add( self.m_textCtrl2, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 4 ), wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 6 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"转换后配置：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gbSizer2.Add( self.m_staticText2, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"待转换配置：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gbSizer2.Add( self.m_staticText1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 6 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,300 ), wx.TE_MULTILINE )
		
		gbSizer2.Add( self.m_textCtrl1, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 6 )
		
		
		tool_gbSizer.Add( gbSizer2, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 5 ), wx.EXPAND, 6 )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 1000,150 ), wx.TE_MULTILINE )
		tool_gbSizer.Add( self.m_textCtrl3, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 6 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"信息输出：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		tool_gbSizer.Add( self.m_staticText3, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.SetSizer( tool_gbSizer )
		self.Layout()
		#self.statusbar = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		#self.statusbar.SetFont( wx.Font( 9, 74, 90, 90, False, "微软雅黑" ) )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.choice_source_file.Bind( wx.EVT_FILEPICKER_CHANGED, self.getsrcfile )
		self.totran.Bind( wx.EVT_TOGGLEBUTTON, self.tran )
		self.output.Bind( wx.EVT_BUTTON, self.output_config )
		self.get_todb.Bind( wx.EVT_BUTTON, self.todb )
	
	def __del__( self ):
		pass
	
	filelines=[]
	token=''
	# Virtual event handlers, overide them in your derived class
	#开始转换按钮触发函数
	def tran( self, event ):
		global token
		self.m_textCtrl2.Clear()
		t2=threading.Thread(target=Hillstone_config.create_hsconfig, args=(self,self.token,))
		t2.start()
		#self.m_textCtrl2.AppendText(self.m_textCtrl1.GetValue())
		self.totran.Enable( False )
	#创建token
	def create_token(self):
		token=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		tokentuple=token,
		self.newdb()
		self.insert_data('token',tokentuple)
		return token	
	#提取配置，写入数据库		
	def todb( self, event ):
		global token
		self.token=self.create_token()
		t=threading.Thread(target=Get_config.configtodb, args=(self,self.m_textCtrl1.GetValue(),self.choice_type.GetCurrentSelection(),self.token))
		t.start()
	#读取配置文件		
	def getsrcfile( self, event ):
		filepath=self.choice_source_file.GetPath()#读取文件路径
		support_codes=['utf-8','gbk','utf-16','GB18030', 'BIG5']#支持的文件编码
		#尝试用各种编码打开文件，适配各种文件编码
		for c in support_codes:
			try:
				file=open(filepath,'r',encoding=c)#打开文件
				bfile=file.read()#读取内容
				break
			except:
				continue
		#global filelines
		#self.filelines=bfile.split('\n')
		#print(self.filelines)
		#file=open(filepath,'rb')
		#bfile=file.read()
		self.m_textCtrl1.Clear()#清除窗口显示
		self.m_textCtrl1.AppendText(bfile)#显示文件内容到窗口
		self.m_textCtrl3.Clear()#清除窗口内容
		#统计分析配置条目数信息
		ip_host=len(re.findall("define host add name", bfile))
		ip_subnet=len(re.findall("define subnet add", bfile))
		ip_range=len(re.findall("define range add", bfile))
		ip_group=len(re.findall("define group_address", bfile))
		service=len(re.findall("define service add", bfile))
		service_group=len(re.findall("define group_service", bfile))
		nat=len(re.findall("nat policy add", bfile))
		policy=len(re.findall("firewall policy add", bfile))
		route=len(re.findall("network route add", bfile))
		#输出到界面
		self.m_textCtrl3.AppendText('------------------------------原始文件统计-------------------------------------\n')
		self.m_textCtrl3.AppendText('配置文件总行数：'+str(len(bfile.split('\n')))+'\n')#统计行数
		self.m_textCtrl3.AppendText('主机IP条目数：'+str(ip_host)+'\n')
		self.m_textCtrl3.AppendText('IP掩码条目数：'+str(ip_subnet)+'\n')
		self.m_textCtrl3.AppendText('IP范围条目数：'+str(ip_range)+'\n')
		self.m_textCtrl3.AppendText('地址组条目数：'+str(ip_group)+'\n')
		self.m_textCtrl3.AppendText('自定义服务条目数：'+str(service)+'\n')
		self.m_textCtrl3.AppendText('服务组条目数：'+str(service_group)+'\n')
		self.m_textCtrl3.AppendText('NAT条目数：'+str(nat)+'\n')
		self.m_textCtrl3.AppendText('POLICY条目数：'+str(policy)+'\n')
		self.m_textCtrl3.AppendText('ROUTE条目数：'+str(route)+'\n')
		self.m_textCtrl3.AppendText('-------------------------------------------------------------------------\n')
		
	#导出配置，生成hillstone配置文件	
	def output_config( self, event ):
		config=self.m_textCtrl2.GetValue()
		nowTime=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		newconfig=open('hillstone_config'+nowTime+'.txt','w')
		newconfig.write(config)
		newconfig.close()
		self.m_textCtrl3.AppendText('文件导出成功！配置文件路径在：'+os.getcwd()+'\\hillstone_config'+nowTime+'.txt')
		webbrowser.open('hillstone_config'+nowTime+'.txt')


####################################主界面######################################
class Mywin ( wx.Frame ):
	version='0.8'	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"友商配置转换工具v"+self.version, pos = wx.DefaultPosition, size = wx.Size( 1100,680), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 9, 74, 90, 90, False, "微软雅黑" ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVEBORDER ) )
		
		self.statusbar = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		self.statusbar.SetFont( wx.Font( 9, 74, 90, 90, False, "微软雅黑" ) )

		
		self.Centre( wx.BOTH )
		#self.versioncheck()
	#版本检测，有新版提示更新！
	def versioncheck(self):
		try:
			global version
			url="https://ps.hillstonenet.com/hillstone_tool_version_check.txt"
			req=urllib.request.Request(url)
			resp=urllib.request.urlopen(req)
			data=resp.read().decode('utf-8')
	
			if self.version not in data:
				get=wx.MessageBox('有新版本啦！是否下载更新?', "版本更新" ,wx.YES_NO | wx.ICON_INFORMATION)
				if get==wx.YES:
					webbrowser.open("https://ps.hillstonenet.com")
		except:
			pass
	
	def __del__( self ):
		pass

#程序创建时间：2018.8.17
#主程序开始
#if __name__ == '__main__':
    #app = wx.App(False)
    #frame= covert_toolui(None)
    #frame.Show()
    #app.MainLoop()
    #pass


if __name__ == '__main__':
    app = wx.App(False)
    framebox = Mywin(None)
    frame = wx.Notebook(framebox)
    frame.AddPage(covert_toolui(frame), "配置转换工具v0.8")
    #frame.AddPage(sendpktui(frame), "发包工具v1.3.2")
    #frame.AddPage(batchpatrol(frame), "巡检助手(批量)v1.0.4")
    #frame.AddPage(Pktsend(frame), "数据包模拟工具v1.3")
    #frame.AddPage(Pktrev(frame), "数据包模拟工具-抓包端v1.3")
    framebox.Show()
    #framebox.versioncheck()
    app.MainLoop()
    
    pass
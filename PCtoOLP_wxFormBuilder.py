# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 25 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PCtoOLP", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Planning Center Plan Selection" ), wx.VERTICAL )
		
		fgSizer3 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Service Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer3.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_serviceTypeComboBoxChoices = []
		self.m_serviceTypeComboBox = wx.ComboBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_serviceTypeComboBoxChoices, wx.CB_READONLY )
		self.m_serviceTypeComboBox.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer3.Add( self.m_serviceTypeComboBox, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Select Plan", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer3.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_selectPlanComboBoxChoices = []
		self.m_selectPlanComboBox = wx.ComboBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Select Plan Date", wx.DefaultPosition, wx.DefaultSize, m_selectPlanComboBoxChoices, wx.CB_READONLY )
		fgSizer3.Add( self.m_selectPlanComboBox, 2, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer3.Add( fgSizer3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( sbSizer3, 0, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"OpenLP Theme Settings" ), wx.VERTICAL )
		
		fgSizer5 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer5.AddGrowableCol( 1 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Song Theme", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer5.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_songThemeComboBoxChoices = []
		self.m_songThemeComboBox = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_songThemeComboBoxChoices, wx.CB_READONLY )
		self.m_songThemeComboBox.Enable( False )
		
		fgSizer5.Add( self.m_songThemeComboBox, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Slide Theme", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer5.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_slideThemeComboBoxChoices = []
		self.m_slideThemeComboBox = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_slideThemeComboBoxChoices, wx.CB_READONLY )
		self.m_slideThemeComboBox.Enable( False )
		
		fgSizer5.Add( self.m_slideThemeComboBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer2.Add( fgSizer5, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_themeDefaultCheckBox = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Save as Default Choices", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_themeDefaultCheckBox.SetValue(True) 
		self.m_themeDefaultCheckBox.Enable( False )
		
		sbSizer2.Add( self.m_themeDefaultCheckBox, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( sbSizer2, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_cancelButton = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_cancelButton, 0, wx.ALL, 5 )
		
		self.m_saveButton = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_saveButton.Enable( False )
		
		bSizer6.Add( self.m_saveButton, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer6, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_serviceTypeComboBox.Bind( wx.EVT_COMBOBOX, self.ServiceTypeSelected )
		self.m_selectPlanComboBox.Bind( wx.EVT_COMBOBOX, self.PlanSelected )
		self.m_cancelButton.Bind( wx.EVT_BUTTON, self.OnCancel )
		self.m_saveButton.Bind( wx.EVT_BUTTON, self.OnSave )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def ServiceTypeSelected( self, event ):
		event.Skip()
	
	def PlanSelected( self, event ):
		event.Skip()
	
	def OnCancel( self, event ):
		event.Skip()
	
	def OnSave( self, event ):
		event.Skip()
	


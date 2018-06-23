#!/usr/bin/python

import wx
import PCtoOLP_wxFormBuilder
import planningcenter_api
import sys
from datetime import datetime
import openlp
import os
from modulegraph.modulegraph import entry

class MainFrame(PCtoOLP_wxFormBuilder.MainFrame):
    def __init__(self,parent):
        PCtoOLP_wxFormBuilder.MainFrame.__init__(self,parent)
                
        # create an Planning Center API Object
        self.pcAPI = planningcenter_api.PlanningCenterAPI()
        
        # set the Service Type Dropdown Box from PCO
        serviceTypeList = self.pcAPI.GetServiceTypeList()
        
        for serviceType in serviceTypeList:
            self.m_serviceTypeComboBox.Append(serviceType['attributes']['name'],serviceType['id'])
        
        # set the default selection to the first item
        self.m_serviceTypeComboBox.SetSelection(0)
        
        self.ShowPlanListForServiceTypeSelection()
        
        # See if we can find the templates directory for OpenLP
        home = os.path.expanduser("~")
        mac_openlp_themes_dir = os.path.join(home,'Library','Application Support','openlp','Data','themes')
        
        # iterate through the themes directory and save the names of each directory that also 
        # contain an xml file inside the directory that matches the directory name
        
        theme_list = []
        if os.path.isdir(mac_openlp_themes_dir):
            for entry in os.listdir(mac_openlp_themes_dir):
                if os.path.isdir(os.path.join(mac_openlp_themes_dir,entry)):
                    if os.path.isfile(os.path.join(mac_openlp_themes_dir,entry,"{0}.xml".format(entry))):
                        theme_list.append(entry)
        
        # pull configuration data in from wx.config (registry or config file)
        config = wx.Config('PCtoOLP')
        default_song_template = config.Read('default_song_template')
        default_slide_template = config.Read('default_slide_template')
                 
        # if we found any themes, enable the theme selection dropdowns and populate them with themes
        if len(theme_list):
            for theme in theme_list:
                song_index = self.m_songThemeComboBox.Append(theme)
                slide_index = self.m_slideThemeComboBox.Append(theme)
                
                if default_song_template == theme:
                    self.m_songThemeComboBox.SetSelection(song_index)
                if default_slide_template == theme:
                    self.m_slideThemeComboBox.SetSelection(slide_index)
            
            # enable the GUI elements
            self.m_songThemeComboBox.Enable(True)   
            self.m_slideThemeComboBox.Enable(True)
            self.m_themeDefaultCheckBox.Enable(True)
        
            # set defaults to first element if not already set.
            if self.m_songThemeComboBox.GetSelection() == wx.NOT_FOUND:
                self.m_songThemeComboBox.SetSelection(0)
            if self.m_slideThemeComboBox.GetSelection() == wx.NOT_FOUND:
                self.m_slideThemeComboBox.SetSelection(0)
        
    def ShowPlanListForServiceTypeSelection(self):
        # get the service_type_id from the combo box
        serviceTypeID = self.m_serviceTypeComboBox.GetClientData(self.m_serviceTypeComboBox.GetSelection())

        # get the list of plans available for the service type
        plan_list = self.pcAPI.GetPlanList(serviceTypeID)
        
        self.m_selectPlanComboBox.Clear()
        self.m_selectPlanComboBox.Append('Select Plan Date')
        self.m_selectPlanComboBox.SetSelection(0)

        for plan in plan_list:
            self.m_selectPlanComboBox.Append(plan['attributes']['dates'],plan['id'])
        
    def ServiceTypeSelected( self, event ):
        self.ShowPlanListForServiceTypeSelection()

    def PlanSelected( self, event ):
        # we need to decrement the index of the selected value because 
        # we artifically increased the index count by adding a 'Select Plan Date'
        # selection at the beginning
        planSelectedIndex = event.Selection - 1
        
        if planSelectedIndex == -1:
            self.m_saveButton.Enable(False)
        else:
            self.m_saveButton.Enable(True)
        
    def OnCancel( self, event ):
        sys.exit()

    def OnSave( self, event ):
        # disable the save button so as to not get multiple clicks during the save operation
        self.m_saveButton.Enable(False)
        
        # save the song/slide template defaults if the checkbox is checked
        if self.m_themeDefaultCheckBox.GetValue():
            config = wx.Config('PCtoOLP')
            default_song_template = self.m_songThemeComboBox.GetStringSelection()
            default_slide_template = self.m_slideThemeComboBox.GetStringSelection()
            
            config.Write('default_song_template',default_song_template)
            config.Write('default_slide_template',default_slide_template)

        # get the plan ID from the combobox
        planID = self.m_selectPlanComboBox.GetClientData(self.m_selectPlanComboBox.GetSelection())
        items = self.pcAPI.GetItemsDict(planID)
        
        # create a YYYYMMDD plan_date 
        datetime_object = datetime.strptime(self.m_selectPlanComboBox.GetStringSelection(), '%B %d, %Y' )
        plan_date = datetime.strftime(datetime_object, '%Y%m%d')
        
        # create an OpenLP ServiceManager object
        service_manager = openlp.ServiceManager(plan_date)
        item_list_string = 'Transferred Items:\n'
        
        # iterate through the items and add them to the openLP Service Manager object
        for item in items['data']:
            item_title = item['attributes']['title']
            item_list_string += "\n  * {0}".format(item_title)
        
            if item['attributes']['item_type'] == 'song':
                arrangement_id = item['relationships']['arrangement']['data']['id']
                song_id = item['relationships']['song']['data']['id']
        
                # get arrangement from "included" resources
                arrangement_data = {}
                song_data = {}
                for included_item in items['included']:
                    if included_item['type'] == 'Song' and included_item['id'] == song_id:
                        song_data = included_item
                    elif included_item['type'] == 'Arrangement' and included_item['id'] == arrangement_id:
                        arrangement_data = included_item
                        
                    # if we have both song and arrangement set, stop iterating
                    if len(song_data) and len(arrangement_data):
                        break
                    
                author = song_data['attributes']['author']   
                if author is None:
                    author = "Unknown"
        
                lyrics = arrangement_data['attributes']['lyrics']
                arrangement_updated_at = arrangement_data['attributes']['updated_at']
        
                # split the lyrics into verses
                verses = []
                verses = planningcenter_api.SplitLyricsIntoVerses(lyrics)
        
                song = openlp.Song(item_title,author,verses,arrangement_updated_at)
                song.SetTheme(self.m_songThemeComboBox.GetStringSelection())
                service_manager.AddServiceItem(song)
        
            else:
        
                custom_slide = openlp.CustomSlide(item_title)
                custom_slide.SetTheme(self.m_slideThemeComboBox.GetStringSelection())
                service_manager.AddServiceItem(custom_slide)
        
        file_location_message = service_manager.WriteOutput()
        
        message = "{0}\n\n{1}".format(item_list_string,file_location_message)
        
        wx.MessageBox(message=message, style=wx.OK | wx.ICON_INFORMATION)
        
        # re-enable the save button now that we are done
        self.m_saveButton.Enable(True)
        
app = wx.App(False)
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
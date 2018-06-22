#!/usr/bin/python

import wx
import PCtoOLP_wxFormBuilder
import planningcenter_api
import sys
from datetime import datetime
import openlp

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
                service_manager.AddServiceItem(song)
        
            else:
        
                custom_slide = openlp.CustomSlide(item_title)
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
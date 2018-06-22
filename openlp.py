import json
import os
import zipfile
import re

from os.path import expanduser

home = expanduser("~")
default_path = os.path.join(home, "Documents")
full_path = os.path.join(default_path,"openlp_services")

if not os.path.exists(full_path):
    os.makedirs(full_path)

class ServiceManager:
    def __init__(self,plan_name):

        self.openlp_data = []
        self.plan_name = plan_name

        openlp_core = {}
        openlp_core['openlp_core'] = {}
        openlp_core['openlp_core']['lite-service'] = False
        openlp_core['openlp_core']['service-theme'] = ''

        self.openlp_data.append(openlp_core)

    def AddServiceItem(self,service_item):
        self.openlp_data.append(service_item.openlp_data)

    def WriteOutput(self):

        # write to a default path with plan_name as the filename
        osj_path = self.plan_name + '.osj'
        osz_path = self.plan_name + '.osz'
        
        # openlp doesn't like the "full path" to the osj file specified inside the zip file, 
        # so by using chdir, I can eliminate the need to put the full path to the file to be zipped
        os.chdir(full_path)

        with open(osj_path, 'w') as outfile:
            json.dump(self.openlp_data, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            
        with zipfile.ZipFile(osz_path, 'w') as osz_file:
            osz_file.write(osj_path,compress_type=zipfile.ZIP_DEFLATED)
            os.remove(osj_path)
            return "Wrote Service File to:\n {0}/{1}".format(full_path, osz_path)

class Verse:
    def __init__(self, verse_tag, verse_title, raw_slide):
        self.verseTag = verse_tag
        self.title = verse_title
        self.raw_slide = raw_slide

class ServiceItem:
    def __init__(self):

        self.openlp_data = {}
        self.openlp_data['serviceitem'] = {}

        self.openlp_data['serviceitem']['data'] = []

        self.openlp_data['serviceitem']['header'] = {}
        self.openlp_data['serviceitem']['header']['background_audio'] = []
        self.openlp_data['serviceitem']['header']['name'] = ''
        self.openlp_data['serviceitem']['header']['type'] = 1
        self.openlp_data['serviceitem']['header']['will_auto_start'] = False
        self.openlp_data['serviceitem']['header']['media_length'] = 0
        self.openlp_data['serviceitem']['header']['timed_slide_interval'] = 0

        self.openlp_data['serviceitem']['header']['data'] = {}

        self.openlp_data['serviceitem']['header']['auto_play_slides_loop'] = False
        self.openlp_data['serviceitem']['header']['theme'] = None
        self.openlp_data['serviceitem']['header']['audit'] = ""
        self.openlp_data['serviceitem']['header']['xml_version'] = None
        self.openlp_data['serviceitem']['header']['theme_overwritten'] = False
        self.openlp_data['serviceitem']['header']['title'] = ''
        self.openlp_data['serviceitem']['header']['processor'] = None
        self.openlp_data['serviceitem']['header']['start_time'] = 0
        self.openlp_data['serviceitem']['header']['icon'] = ''
        self.openlp_data['serviceitem']['header']['end_time'] = 0
        self.openlp_data['serviceitem']['header']['from_plugin'] = False
        self.openlp_data['serviceitem']['header']['capabilities'] = []
        self.openlp_data['serviceitem']['header']['footer'] = ["",""]
        self.openlp_data['serviceitem']['header']['search'] = ''
        self.openlp_data['serviceitem']['header']['auto_play_slides_once'] = False
        self.openlp_data['serviceitem']['header']['notes'] = ''
        self.openlp_data['serviceitem']['header']['plugin'] = ''
        
    def SetTheme(self, theme):
        self.openlp_data['serviceitem']['header']['theme'] = theme
        

class Song(ServiceItem):
    def __init__(self, song_title, authors, verses, update_timestamp):
        ServiceItem.__init__(self)

        self.update_timestamp = update_timestamp

        # set the custom elements that are unique for songs
        self.openlp_data['serviceitem']['header']['name'] = 'songs'
        self.openlp_data['serviceitem']['header']['data']['title'] = "{0}@".format(song_title.lower())
        self.openlp_data['serviceitem']['header']['data']['authors'] = authors
        self.openlp_data['serviceitem']['header']['audit'] = [song_title, [authors], '', '']
        self.openlp_data['serviceitem']['header']['title'] = song_title
        self.openlp_data['serviceitem']['header']['icon'] = ':/plugins/plugin_songs.png'
        self.openlp_data['serviceitem']['header']['capabilities'] = [2,1,5,8,9,13]
        self.openlp_data['serviceitem']['header']['footer'] = [song_title, "Written by: {0}".format(authors)]
        self.openlp_data['serviceitem']['header']['plugin'] = 'songs'

        # these are the openlp names for each of these PCO verse types
        # the OpenLP verse name is 1 letter and 1 number.
        # for the json format, the number can be repeated, but in the
        # embedded xml format, the verse name should be unique and lowercase
        # like:  v1a, v1b, v2, v3, p1, c1, b1
        verseTypePCOToOpenLP = {}
        verseTypePCOToOpenLP['VERSE'] = 'V'
        verseTypePCOToOpenLP['V'] = 'V'
        verseTypePCOToOpenLP['C'] = 'C'
        verseTypePCOToOpenLP['CHORUS'] = 'C'
        verseTypePCOToOpenLP['PRECHORUS'] = 'P'
        verseTypePCOToOpenLP['INTRO'] = 'I'
        verseTypePCOToOpenLP['ENDING'] = 'E'
        verseTypePCOToOpenLP['BRIDGE'] = 'B'

        for verse in verses:
            
            # lookup the verseTag from the dictionary and use only a 2-digit
            m = re.search("^([A-Za-z]+)\s*(\d*)$", verse['verseTag'])
            verseTypePCO = m.group(1)
            if m.lastindex == 2:
                verseTypePCONumber = m.group(2)
            else:
                verseTypePCONumber = 1
                
            # lookup the OpenLP VerseTag from the dictionary, with default of 'O' for OTHER
            openLPVerseType = 'O'
            if verseTypePCOToOpenLP.has_key(verseTypePCO.upper()):
                openLPVerseType = verseTypePCOToOpenLP[verseTypePCO.upper()]
                
            openLPVerseTag = "{0}{1}".format(openLPVerseType, verseTypePCONumber)
                
                
            self.AppendVerse(verse['raw_slide'],openLPVerseTag)
        self.UpdateXMLString()

    def UpdateXMLString(self):
        xml_string = u"""<?xml version='1.0' encoding='UTF-8'?>
<song xmlns=\"http://openlyrics.info/namespace/2009/song\" version=\"0.8\" \
createdIn=\"PCO\" modifiedIn=\"PCO\" modifiedDate=\"{2}\">\
<properties>\
<titles><title>{0}</title></titles>\
<authors><author>{1}</author></authors>\
</properties><lyrics>""".format(self.openlp_data['serviceitem']['header']['title'],self.openlp_data['serviceitem']['header']['data']['authors'],self.update_timestamp)

        versesUsed = {}

        for verse in self.openlp_data['serviceitem']['data']:
            
            verse_with_html_breaks = re.sub("\n","<br/>",verse.raw_slide)
            
            # make each verseTag unique, stupid index must be alpha instead of numeric
            index = 'a'
            xmlVerseTag = "{0}_{1}".format(verse.verseTag.lower(),index)
            
            while versesUsed.has_key(xmlVerseTag):
                index = chr(ord(index) + 1)
                xmlVerseTag = "{0}{1}".format(verse.verseTag.lower(),index)
                
            versesUsed[xmlVerseTag] = 1
            
            xml_string += u"<verse name=\"{0}\"><lines>{1}</lines></verse>".format(xmlVerseTag, verse_with_html_breaks)

        xml_string += u"</lyrics></song>"

        self.openlp_data['serviceitem']['header']['xml_version'] = xml_string

    def AppendVerse(self, lyrics, verse_tag = 'V1'):
        # create a verse title (first 25 characters of first line)
        lyrics_array = lyrics.split('\n')
        verse_title = lyrics_array[0][:35]
        verse = Verse(verse_tag, verse_title, lyrics)

        self.openlp_data['serviceitem']['data'].append(verse)

class CustomSlide(ServiceItem):
    def __init__(self,custom_slide_title):
        ServiceItem.__init__(self)

        # set the custom elements are the unique for CustomSlides

        custom_slide = Verse(None,custom_slide_title,custom_slide_title)
        self.openlp_data['serviceitem']['data'].append(custom_slide)

        self.openlp_data['serviceitem']['header']['name'] = 'custom'
        self.openlp_data['serviceitem']['header']['title'] = custom_slide_title
        self.openlp_data['serviceitem']['header']['icon'] = ':/plugins/plugin_custom.png'
        self.openlp_data['serviceitem']['header']['capabilities'] = [2,1,5,13,8]
        self.openlp_data['serviceitem']['header']['footer'] = [custom_slide_title]
        self.openlp_data['serviceitem']['header']['plugin'] = 'custom'

import json

class ServiceManager:
    def __init__(self,plan_name):
        
        self.openlp_data = []
        self.plan_name = plan_name
        
        openlp_core = {}
        openlp_core['openlp_core'] = {}
        openlp_core['openlp_core']['lite-service'] = False
        openlp_core['openlp_core']['service-theme'] = 'Blue Burst'
        
        self.openlp_data.append(openlp_core)
        
    def AddServiceItem(self,service_item):
        self.openlp_data.append(service_item.openlp_data)

    def WriteOutput(self):
        
        # write to a default path with plan_name as the filename
        default_path = "C:\Users\jkirklan\Documents"
        full_path = "{0}\{1}.osj".format(default_path,self.plan_name)
        
        with open(full_path, 'w') as outfile:
            json.dump(self.openlp_data, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            print "Wrote Output to {0}".format(full_path)

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
        
class Song(ServiceItem):
    def __init__(self, song_title, authors, lyrics, update_timestamp):
        ServiceItem.__init__(self)
        
        self.update_timestamp = update_timestamp
        
        # set the custom elements that are unique for songs
        self.openlp_data['serviceitem']['header']['name'] = 'songs'
        self.openlp_data['serviceitem']['header']['data']['title'] = "{0}@".format(song_title.lower())
        self.openlp_data['serviceitem']['header']['data']['authors'] = authors
        self.openlp_data['serviceitem']['header']['audit'] = [song_title, [authors], "", ""]
        self.openlp_data['serviceitem']['header']['title'] = song_title
        self.openlp_data['serviceitem']['header']['icon'] = ':/plugins/plugin_songs.png'
        self.openlp_data['serviceitem']['header']['capabilities'] = [2,1,5,8,9,13]
        self.openlp_data['serviceitem']['header']['footer'] = [song_title, "Written by: {0}".format(authors)]
        self.openlp_data['serviceitem']['header']['plugin'] = 'songs'
        self.openlp_data['serviceitem']['header']['theme'] = None

        self.AppendVerse(lyrics)
        
        
    def UpdateXMLString(self):
        xml_string = u"""<?xml version='1.0' encoding='UTF-8'?>\
<song xmlns=\"http://openlyrics.info/namespace/2009/song\" version=\"0.8\" 
createdIn=\"Planning Center Online\" modifiedIn=\"Planning Center Online\" modifiedDate=\"{2}\">\
<properties>\
<titles><title>{0}</title></titles>\
<authors><author>{1}</author></authors>\
</properties>""".format(self.openlp_data['serviceitem']['header']['title'],self.openlp_data['serviceitem']['header']['data']['authors'],self.update_timestamp)
                
        for verse in self.openlp_data['serviceitem']['data']:
            xml_string += u"""\
<lyrics>
<verse name=\"{0}\"><lines>{1}</lines></verse>
</lyrics>""".format(verse.verseTag, verse.raw_slide)
        
        xml_string += u"</song>"
        
        self.openlp_data['serviceitem']['header']['xml_version'] = xml_string
        
    def AppendVerse(self, lyrics, verse_tag = 'V1'):
        # create a verse title (first 25 characters of first line)
        lyrics_array = lyrics.split('\n')
        verse_title = lyrics_array[0][:25]
        verse = Verse(verse_tag, verse_title, lyrics)
        
        self.openlp_data['serviceitem']['data'].append(verse)
        
        self.UpdateXMLString()
        
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
        self.openlp_data['serviceitem']['header']['theme'] = 'Default Slide Theme'
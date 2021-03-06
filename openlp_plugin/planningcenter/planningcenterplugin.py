# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2017 OpenLP Developers                                   #
# Copyright (c) 2018 John Kirkland                                            #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The :mod:`~openlp.plugins.planningcenter.planningcenterplugin` module contains the Plugin class
for the PlanningCenter plugin.
"""

import logging
log = logging.getLogger(__name__)

""" 
When running the plugin from within a compiled, pyinstaller package (MacOS/Windows),
any attempt to import a module from a subdirectory of openlp.plugins.planningcenter
will fail with an ImportError saying that 'openlp.plugins.planningcenter' does not
exist.  This does not occur when running the code directly from python.  
In the compiled environment, you can import from 'plugins.planningcenter', but this fails
in a source-code environment.  Thus, the solution below.  
First, try importing 'openlp.plugins.planningcenter' directly as a module.  
If this fails with an ImportError, then import 'plugins.planningcenter' and 
then move the instantiated module to the name, 'openlp.plugins.planningcenter'.
"""
import sys
try:
    __import__('openlp.plugins.planningcenter')
except ImportError:
    __import__('plugins.planningcenter')
    sys.modules['openlp.plugins.planningcenter'] = sys.modules.pop('plugins.planningcenter')

from openlp.core.common import Registry, Settings, translate
from openlp.core.lib import Plugin, StringContent
from openlp.core.lib.ui import create_action
from openlp.plugins.planningcenter.forms.planningcenterform import PlanningCenterForm, PlanningCenterAuthForm


__default_settings__ = {
    'planningcenter/application_id': '',
    'planningcenter/secret': ''
}

class planningcenterplugin(Plugin):
    """
    This plugin enables the user to import services from Planning Center Online.
    """
    log.info('PlanningCenter Plugin loaded')

    def __init__(self):
        """
        Create and set up the PlanningCenter plugin.
        """
        super(planningcenterplugin, self).__init__('planningcenter', __default_settings__, version='0.1')
        self.planningcenterselect_form = None

    def initialise(self):
        """
        Initialise the plugin
        """
        log.info('PlanningCenter Initialising')
        super(planningcenterplugin, self).initialise()
        
        
        
        # Determine which dialog to show based on whether the auth values are set yet
        self.application_id = Settings().value("planningcenter/application_id")
        self.secret = Settings().value("planningcenter/secret")
        
        if len(self.application_id) == 0 or len(self.secret) == 0:
            self.planningcenterselect_form = PlanningCenterAuthForm(Registry().get('main_window'), self)
        else:
            self.planningcenterselect_form = PlanningCenterForm(Registry().get('main_window'), self)
        self.planningcenterselect_form.initialise()

    def add_import_menu_item(self, import_menu):
        """
        Add "PlanningCenter Service" to the **Import** menu.

        :param import_menu: The actual **Import** menu item, so that your actions can use it as their parent.
        """
        self.import_planningcenterelect_item = create_action(
            import_menu, 'import_planningcenterelect_item', text=translate('planningcenterplugin', 'Planning Center Service'),
            statustip=translate('planningcenterplugin', 'Import Planning Center Service Plan from Planning Center Online.'),
            triggers=self.on_import_planningcenterelect_item_triggered
        )
        import_menu.addAction(self.import_planningcenterelect_item)

    def on_import_planningcenterelect_item_triggered(self):
        """
        Run the PlanningCenter importer.
        """
        self.planningcenterselect_form.exec()

    @staticmethod
    def about():
        """
        Provides information for the plugin manager to display.

        :return: A translatable string with some basic information about the PlanningCenter plugin
        """
        return translate('planningcenterplugin', '<strong>PlanningCenter Plugin</strong>'
                                        '<br />The planningcenter plugin provides an interface to import service plans from the Planning Center Online v2 API.')

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        # Name PluginList
        self.text_strings[StringContent.Name] = {
            'singular': translate('planningcenterplugin', 'PlanningCenter', 'name singular'),
            'plural': translate('planningcenterplugin', 'PlanningCenter', 'name plural')
        }
        # Name for MediaDockManager, SettingsManager
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('planningcenterplugin', 'PlanningCenter', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            'load': '',
            'import': translate('planningcenterplugin', 'Import All Plan Items into Current Service'),
            'new': translate('planningcenterplugin', 'Add a new song.'),
            'edit': translate('planningcenterplugin', 'Edit the selected song.'),
            'delete': translate('planningcenterplugin', 'Delete the selected song.'),
            'preview': translate('planningcenterplugin', 'Preview the selected song.'),
            'live': translate('planningcenterplugin', 'Send the selected song live.'),
            'service': translate('planningcenterplugin', 'Add the selected song to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info('PlanningCenter Finalising')
        self.new_service_created()
        super(planningcenterplugin, self).finalise()

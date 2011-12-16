'''
Created on Aug 28, 2011

@author: eric
'''

import sys
import pkg_resources
from paste.script.appinstall import Installer
class PyramidInstaller(Installer):
    use_cheetah = False
    config_file = 'config/deployment.ini_tmpl'

    def config_content(self, command, vars):
        """
        Called by ``self.write_config``, this returns the text content
        for the config file, given the provided variables.
        """
        modules = [line.strip()
                    for line in self.dist.get_metadata_lines('top_level.txt')
                    if line.strip() and not line.strip().startswith('#')]
        if not modules:
            print >> sys.stderr, 'No modules are listed in top_level.txt'
            print >> sys.stderr, \
                'Try running python setup.py egg_info to regenerate that file'
        for module in modules:
            if pkg_resources.resource_exists(module, self.config_file):
                return self.template_renderer(
                    pkg_resources.resource_string(module, self.config_file),
                    vars, filename=self.config_file)
        # Legacy support for the old location in egg-info
        return super(PyramidInstaller, self).config_content(command, vars)
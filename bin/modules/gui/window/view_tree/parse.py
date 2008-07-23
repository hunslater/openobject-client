# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import gtk
import gobject
from xml.parsers import expat

import gettext

class parse(object):
    def __init__(self, fields):
        self.fields = fields
        self.pixbufs = {}

    def _psr_start(self, name, attrs):
        if name=='tree':
            self.title = attrs.get('string',_('Tree'))
            self.toolbar = bool(attrs.get('toolbar',False))
        elif name=='field':
            type = self.fields[attrs['name']]['type']
            if type!='checkbox':
                column = gtk.TreeViewColumn(self.fields[attrs['name']]['string']) #, cell, text=self.pos)
                if 'icon' in attrs:
                    render_pixbuf = gtk.CellRendererPixbuf()
                    column.pack_start(render_pixbuf, expand=False)
                    column.add_attribute(render_pixbuf, 'pixbuf', self.pos)
                    self.fields_order.append(str(attrs['icon']))
                    self.pixbufs[self.pos]=True
                    self.pos+=1

                cell = gtk.CellRendererText()
                cell.set_fixed_height_from_font(1)
                if type=='float':
                    cell.set_property('xalign', 1.0)
                column.pack_start(cell, expand=False)
                column.add_attribute(cell, 'text', self.pos)
            else:
                cell = gtk.CellRendererToggle()
                column = gtk.TreeViewColumn (self.fields[attrs['name']]['string'], cell, active=self.pos)
            self.pos+=1
            column.set_resizable(1)
            self.fields_order.append(str(attrs['name']))
            self.tree.append_column(column)
        else:
            import logging
            log = logging.getLogger('view')
            log.error('unknown tag: '+str(name))
            del log
    def _psr_end(self, name):
        pass
    def _psr_char(self, char):
        pass
    def parse(self, xml_data, tree):
        cell = gtk.CellRendererText()
        cell.set_fixed_height_from_font(1)
        column = gtk.TreeViewColumn('ID', cell, text=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(60)
        column.set_visible(False)
        tree.append_column(column)
        self.tree = tree
        self.pos = 1

        self.fields_order=[]

        psr = expat.ParserCreate()
        psr.StartElementHandler = self._psr_start
        psr.EndElementHandler = self._psr_end
        psr.CharacterDataHandler = self._psr_char
        psr.Parse(xml_data)
        return self.pos



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


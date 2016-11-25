# -*- coding: utf-8 -*-

import openerp

import logging
import sys
import os
from os.path import join as joinpath, isdir

from openerp.modules import get_modules, get_module_path
import openerp.modules.registry
import openerp.modules.loading as loading
import openerp.tools as tools
from lxml import etree, builder

from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class xml_import(object):
    def __init__(self,cr, module):
        self.cr = cr
        self.module = module
        self.noupdate = False
        self.update_record_dict = []
        self._tags = {
            'record': self._tag_record,
        }

    @staticmethod
    def nodeattr2bool(node, attr, default=False):
        if not node.get(attr):
            return default
        val = node.get(attr).strip()
        if not val:
            return default
        return val.lower() not in ('0', 'false', 'off')

    def isnoupdate(self, data_node=None):
        return self.noupdate or (len(data_node) and self.nodeattr2bool(data_node, 'noupdate', False))

    def parse(self, de):
        roots = ['openerp','data','odoo']
        if de.tag not in roots:
            raise Exception("Root xml tag must be <openerp>, <odoo> or <data>.")
        for rec in de:
            if rec.tag in roots:
                self.parse(rec)
            elif rec.tag in self._tags:
                try:
                    self._tags[rec.tag](rec, de)
                except Exception, e:
                    _logger.info("parse error:%s", e.message)
        return True

    def write_noupdate_flag(self):
        if self.noupdate and self.update_record_dict:
            for i in self.update_record_dict:
                if i['id'].find('.') != -1:
                    self.cr.execute("update ir_model_data set noupdate=True where module=%s and model=%s and name=%s", (i['module'], i['model'], i['id'].split('.')[1]))
                else:
                    self.cr.execute("update ir_model_data set noupdate=True where module=%s and model=%s and name=%s", (i['module'], i['model'], i['id']))
        return True

    def _tag_record(self,rec, data_node=None):
        """
        <?xml version="1.0" encoding="utf-8"?>
        <openerp>
            <data>
                <record model="ir.actions.act_window" id="hr_dimission_action">
                    <field name="name">Batch Termination</field>
                    <field name="type">ir.actions.act_window</field>
                    <field name="res_model">hr.dimission</field>
                    <field name="view_type">form</field>
                    <field name="view_mode">tree,form</field>
                    <field name="context">{}</field>
                    <field name="help" type="html">
                      <p class="oe_view_nocontent_create">
                            Description：
                      </p>
                      <p>
                      Click here to create batch leave apply sheet.
                      </p>
                    </field>
                </record>
            </data>
        </openerp>
        :param cr:
        :param rec:
        :param data_node:
        :param mode:
        :return:
        """
        rec_model = rec.get("model").encode('ascii')
        rec_id = rec.get("id").encode('ascii')
        self.noupdate = self.isnoupdate(data_node)
        if self.noupdate:
            self.update_record_dict.append({'module': self.module, 'model':rec_model, 'id':rec_id})

def get_installed_module(cr):
    sql = "SELECT name from ir_module_module WHERE state in ('installed')"
    cr.execute(sql)
    installed_module_list = [name for (name,) in cr.fetchall()]
    return installed_module_list

def get_module(installed_modules):
    module_info = {}
    for i in openerp.modules.get_modules():
        mod_path = openerp.modules.get_module_path(i)
        if not mod_path:
            continue
        if i not in installed_modules:
            continue

        # This will raise an exception if no/unreadable descriptor file.
        info = openerp.modules.load_information_from_description_file(i)

        if not info:
            continue
        else:
            module_info.update({i:info})
    return module_info

def start_run():
    _logger.info('start...')
    args = sys.argv[1:]
    print args

    openerp.tools.config.parse_config(args)
    config = openerp.tools.config
    _logger.info('config:%s', str(config))

    conn_db = openerp.sql_db.db_connect(config['db_name'])
    cr = conn_db.cursor()
    cr.autocommit(False)

    try:
        installed_module_list = get_installed_module(cr)
        # _logger.info('module:%s', installed_module_list)

        #需要测试独立装载xml文件功能
        # tools.convert_file(cr, module_name, filename, idref, mode, noupdate, kind, report)

        #需要测试命令行程序执行odoo所有方法功能
        # registry = openerp.registry(config['db_name'])
        # modobj = registry['ir.module.module']
        # ids = modobj.search(cr, SUPERUSER_ID, [('state', '=', 'installed')])
        # print 'ids:', ids

        module_info = get_module(installed_module_list)
        # _logger.info('module_info:%s', module_info)

        for module_name in module_info.keys():
            for filename in module_info[module_name]['data']:
                pathname = os.path.join(module_name, '%s/%s' % (openerp.modules.get_module_path(module_name),filename))
                _logger.info("loading %s, %s", module_name, pathname)
                ext = os.path.splitext(filename)[1].lower()
                if ext == '.xml':
                    doc = etree.parse(pathname)
                    obj = xml_import(cr, module_name)
                    obj.parse(doc.getroot())
                    if obj.noupdate:
                        _logger.info('%s update: %s, %s', module_name, obj.noupdate, obj.update_record_dict)
                        obj.write_noupdate_flag()


    except Exception, e:
        _logger.error('error:%s', e.message)
    finally:
        cr.commit()
        cr.close()

    _logger.info('end')


start_run()

# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
from openerp.tools.translate import _


class ChangeManagementChange(orm.Model):
    _inherit = 'change.management.change'

    def _create_change_project(self, cr, uid, change, context=None):
        data = {
            'name': '%s - %s' % (change.name, change.description),
            'parent_id': change.project_id.analytic_account_id.id
            }
        return data

    _columns = {
        'change_project_id': fields.many2one('project.project',
                                             'Change Management Project')
    }

    def button_create_change_project(self, cr, uid, ids, context=None):
        for change in self.browse(cr, uid, ids, context=context):
            if change.change_project_id:
                raise orm.except_orm(_('Error!'),
                                     _('A Change Management Project already '
                                       'exists.'))
            project_obj = self.pool['project.project']
            project_data = self._create_change_project(cr, uid, change,
                                                       context=context)
            project_id = project_obj.create(cr, uid, project_data,
                                            context=context)
            self.write(cr, uid, [change.id],
                       {'change_project_id': project_id},
                       context=context)
        return True

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ChangeManagementChange, self).write(cr, uid, ids, vals,
                                                        context=context)
        if 'project_id' in vals:
            project_obj = self.pool['project.project']
            for change in self.browse(cr, uid, ids, context=context):
                if change.change_project_id:
                    project_obj.write(
                        cr, uid, [change.change_project_id.id],
                        {'parent_id':
                            change.project_id.analytic_account_id.id})
        return res

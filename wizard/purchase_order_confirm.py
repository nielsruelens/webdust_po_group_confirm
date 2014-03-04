
from openerp.osv import osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import pooler

class purchase_order_confirm(osv.TransientModel):

    _name = "purchase.order.confirm"
    _description = "Confirm the selected purchases"

    def purchase_confirm(self, cr, uid, ids, context=None):

        wf_service = netsvc.LocalService('workflow')
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        data_inv = pool_obj.get('purchase.order').read(cr, uid, context['active_ids'], ['state'], context=context)

        for record in data_inv:
            if record['state'] != 'draft':
                raise osv.except_osv(_('Warning!'), _("Selected purchases(s) cannot be confirmed as they are not in 'Draft' state."))
            wf_service.trg_validate(uid, 'purchase.order', record['id'], 'purchase_confirm', cr)
        return {'type': 'ir.actions.act_window_close'}

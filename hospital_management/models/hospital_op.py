from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class OP(models.Model):
    _name="hospital.op"
    _description="Hospital OP"
    _rec_name = "op_number"


    card_id = fields.Many2one("patient.card", ondelete ="set null", string="Patient Card", Index=True)
    dob = fields.Date(string = "DOB")
    # patient_name = fields.Char(string = "Patient Name")
    patient_id = fields.Many2one('res.partner')
    patient_age = fields.Integer(string = "Age")
    patient_gender = fields.Char("Gender")
    patient_blood = fields.Char("Blood Group")
    doctor_id = fields.Many2one("hr.employee", ondelete="cascade", string = "Doctor", Index=True
                                , required=True)
    doctor_fee = fields.Monetary(string = "Doctor Fee", currency_field='company_currency')
    company_id = fields.Many2one('res.company', string='Company', required=True)

    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    currency_id = fields.Many2one('res.currency', string='Currency')
    department_id = fields.Char(string = "Department")
    date_op= fields.Date(string = "Date", default = fields.Date.today())
    active = fields.Boolean('Active', default = True)
    op_number = fields.Char(string='OP Number', required=True, copy=False, readonly=True,
                      default='New')
    # token_no = fields.Integer(string = 'Token No', default = lambda self: self.env['hospital.op'].search([], limit=1, order='create_date desc').token_no + 1)
    token_no = fields.Integer(string = 'Token No')
    # token_no = fields.Integer(string="Token No", unique = True,
    #                            default=lambda self: self.env['ir.sequence'].next_by_code('increment_token_no'))
    appointment_id = fields.Many2one('hospital.appointment')
    consultation_type = fields.Selection([
        ('OP', 'OP'),
        ('IP', 'IP')
    ], string = "Consultation Type", realated_field = 'hospital.consult.type')

    journal_type = fields.Many2one('account.journal', 'Journal',
                                   default=lambda self: self.env['account.journal'].search([('id', '=', 1)]))
    account_type = fields.Many2one('account.account', 'Account',
                                   default=lambda self: self.env['account.account'].search([('id', '=', 17)]))

    _sql_constraints = [
        # Partial constraint, complemented by a python constraint (see below).
        ('token_no_uniq', 'UNIQUE(token_no,date_op)', 'You can not have two patients with the same token!'),
    ]



    #python constraint
    @api.constrains('token_no')
    def _check_token_no(self):
        tokens =[]
        for r in self.env['hospital.op'].search([('date_op','=',fields.Date.today())]):
            # if r.date_op == fields.Date.today():#todays tokens
            tokens.append(r.token_no)
        print('today tokens',tokens)
        r = self.env['hospital.op'].search([('date_op','=',fields.Date.today())])
        if len(r) != 0:
            tokens[-1] = None #because it loads the current entry also
        if self.token_no in tokens:
            raise ValidationError("Token number should be unique")
        #     return False
        # else:
        #     return True

    # _constraints = [
    #     ('_check_token_no', 'Token number must be unique', ['token_no'])
    # ]

    @api.model

    def create(self, vals):
        if vals.get('op_number', 'New') == 'New':
            vals['op_number'] = self.env['ir.sequence'].next_by_code(
                'op.card') or 'New'
        result = super(OP, self).create(vals)
        return result



    @api.onchange('card_id')

    def _onchange_card_id(self):

        # self.token_no += self.token_no + 1

        for r in self:
            r.dob = self.card_id.dob
            # r.patient_name = self.card_id.patient_id.name
            r.patient_id = self.card_id.patient_id
            r.patient_age = self.card_id.age
            r.patient_gender = self.card_id.sex
            r.patient_blood = self.card_id.blood_group

            print(r.dob)
        for r in self:
            # if r.token_no == self.token_no:
            #     print('same')
            # else:
            #     print('no duplicate')
            print(r)
        #return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):

        # self.department_id = self.doctor_id.department_id.name
        self.department_id = self.doctor_id.department_id.name
        self.doctor_fee = self.doctor_id.fee
        print('doc fee',self.doctor_fee)
        return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}


    # @api.onchange('op_number')
    #
    # def _onchange_op_number(self):

        # print("lenth of self",len(self))
        # total_rec = sum(self.mapped('op_number'))
        # print("toal rec :",total_rec)



    #         pStart = 1
    #         pInterval = 1
    #         if rec == 0:
    #             rec = pStart
    #         else:
    #             rec += pInterval
    #          rec
    #         self.token_no = rec
    #
    #         # self.token_no = self.token_no + 1



    # def autoIncrement():
    #     global rec
    #     pStart = 1
    #     pInterval = 1
    #     if rec == 0:
    #         rec = pStart
    #     else:
    #         rec += pInterval
    #     return rec

    # @api.onchange('card_id')
    # def _onchange_card_id(self):
    #
    #      td = datetime.date.today() #today
    #      mon = td.month
    #      day = td.day
    #
    #      if len(str(mon)) == 1 :
    #          mon = '0' + str(mon)
    #      if len(str(day)) == 1 :
    #          day = '0' + str(day)
    #
    #      td_str = str(td.year)[2:4] + '/' + str(mon) + '/' + str(day)
    #      #print(OP.objects.filter(token_no = 1))
    #      # if td_str == self.op_number[3:11] :
    #      #
    #      #     self.token_no += 1
    #      # else:
    #      #     self.token_no = 1
    #

    # def token_number_update(self, cr, uid, ids=None, context=None):
    #     sequence_obj = self.pool.get('hospital.op')
    #     seq_id = sequence_obj.search(cr, uid, [('code', '=', 'sale.order')])
    #     if seq_id:
    #         value = sequence_obj.browse(cr, uid, seq_id[0])
    #         number_next = value.number_next
    #         sequence_obj.write(cr, uid, seq_id, {'number_next': 1})
    #     return None

    # @api.onchange('op_number')
    # def _onchange_op_number(self):
    #
    #     self.token_no = self.token_no +1
        # record_ids = self.search([('op_number', '=', self.op_number.id)], order='id desc', limit=1)
        # last_id = record_ids.id
        # print(self.last_id.op_number)
        #code
        # print('token_no',self.token_no)
        # latest_rec = self.env['hospital.op'].search([], limit=1, order='create_date desc')
        # print(latest_rec.op_number)
        # print(self.op_number)
        #code
        tokens = [] #for checking duplicate token

            #print('openv :', r.op_number)
            # if self.token_no == r.token_no:
            #     tokens.append(r.token_no)
            #     print('token repats',r.token_no)


        # print('token after clear',self.token_no)

        #compare todays date with last sequence and set token according to it

        #code
        # td = datetime.date.today()  # today
        # mon = td.month
        # day = td.day
        #
        # if len(str(mon)) == 1 :
        #      mon = '0' + str(mon)
        # if len(str(day)) == 1 :
        #      day = '0' + str(day)
        # #today string
        # td_str = '/'+str(td.year)[2:4] + '/' + str(mon) + '/' + str(day)+'/'
        # if str(latest_rec.op_number)[2:12] != td_str:#compare wiht last sequence
        #     #remove previous entries
        #     for r in self.env['hospital.op'].search([], order='create_date desc'):
        #         r.token_no = None
        #     self.token_no = 1
            #code


    # _sql_constraints = [
    #     ('token_no_unique', 'UNIQUE(token_no)',
    #      'You can not have two users with the same token_no !')
    # ]
    # @api.onchange('token_no')
    # def _onchange_token_no(self):
    #
    #     tokens = []
    #     for r in self.env['hospital.op'].search([]):
    #         tokens.append(r.token_no)
    #     print(tokens)

    @api.onchange('op_number')
    def _onchange_op_number(self):

        if not self.appointment_id:
            # get number of records today
            r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
            print('today count', len(r))

            if len(r) == 0:
                for i in self.env['hospital.op'].search([]):
                    i.token_no = None  # delete token numbers everyday
                # set initial token of the day
                self.token_no = 1
            else:
                existing_tokens = []

                for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
                    existing_tokens.append(r.token_no)
                    # check for duplication of token
                for i in sorted(existing_tokens):
                    n = i + 1
                    if n not in existing_tokens:
                        self.token_no = i + 1
                        break
                print('tokens ex', existing_tokens)
                # r_appointment.token = self.token_no

        """ 
        code connected with appointment token
       

        r_appointment = self.env['hospital.appointment'].search([('date','=',fields.Date.today())])
        #[('card_id.id','=',self.card_id.id)]

        try:

            if r_appointment.token == 0: #if token not set on appointment
                #get number of records today
                r = self.env['hospital.op'].search([('date_op','=',fields.Date.today())])
                print('today count',len(r))

                if len(r) == 0 :
                     for i in self.env['hospital.op'].search([]):
                         i.token_no = None#delete token numbers everyday
                     # set initial token of the day
                     self.token_no = 1
                else:
                    existing_tokens = []

                    for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
                        existing_tokens.append(r.token_no)
                        # check for duplication of token
                    for i in sorted(existing_tokens):
                        n = i + 1
                        if n not in existing_tokens:
                            self.token_no = i + 1
                            break
                    print('tokens ex', existing_tokens)
                    r_appointment.token = self.token_no
                #write an else for setting from other
        except :

            r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
            print('today count', len(r))

            if len(r) == 0:
                for i in self.env['hospital.op'].search([]):
                    i.token_no = None  # delete token numbers everyday
                # set initial token of the day
                self.token_no = 1
            else:
                existing_tokens = []

                for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
                    existing_tokens.append(r.token_no)
                    # check for duplication of token
                for i in sorted(existing_tokens):
                    n = i + 1
                    if n not in existing_tokens:
                        self.token_no = i + 1
                        break
                print('tokens ex', existing_tokens)
        """
    def action_op_register_payment(self):
        r = self.env['hr.employee'].search([('name', '=', self.doctor_id.name)])
        r = self.env['hr.employee'].search([('id', '=', self.doctor_id.id)])
        print("fees", r.fee)
        fval = r.fee
        print(self.doctor_id.fee)
        return self.env['account.payment'] \
            .with_context(active_ids=self.ids, active_model='hospital.op', active_id=self.id, default_amount = self.doctor_id.fee, default_payment_type='inbound',
                          default_partner_id = self.patient_id.id) \
            .action_register_payment()

    def action_invoice_create(self):

        inv_obj = self.env['account.move']
        inv_line_obj = self.env['account.move.line']
        patient = self.patient_id
        inv_data = {
            'name': patient.name,
            'ref': patient.name,
            'type': 'out_invoice',
            # 'account_id': supplier.property_account_payable_id.id,
            'partner_id': patient.id,
            'currency_id': self.account_type.company_id.currency_id.id,
            'journal_id': self.journal_type.id,
            'invoice_origin': self.op_number,
            'company_id': self.account_type.company_id.id,
            # 'invoice_date_due': self.rent_end_date,
        }
        inv_id = inv_obj.create(inv_data)
        # self.first_payment_inv = inv_id.id
        # if inv_id:
        #     list_value = [(0, 0, {
        #         # 'name': self.vehicle_id.name,
        #         'price_unit': self.doctor_fee,
        #         'quantity': 1.0,
        #         # 'account_id': income_account,
        #         # 'product_id': product_id.id,
        #         'move_id': inv_id.id,
        #     })]
        #     inv_id.write({'invoice_line_ids': list_value})

        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_move_out_invoice_type')
        result = {
            'name': action.name,
            'type': 'ir.actions.act_window',
            'views': [[False, 'form']],
            'target': 'current',
            'res_id': inv_id.id,
            'res_model': 'account.move',
        }
        return result

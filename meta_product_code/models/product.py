# from odoo import models, fields, api

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     @api.model_create_multi
#     def create(self, vals_list):
#         for vals in vals_list:
#             print(f"Creating product with vals:------------------- {vals}")
#             if vals.get('categ_id'):
#                 code = self._generate_default_code(vals['categ_id'])
#                 print(f"Generated code:----------------------- {code}")
#                 vals['default_code'] = code
#         return super(ProductTemplate, self).create(vals_list)

#     def write(self, vals):
#         if vals.get('categ_id'):
#             vals['default_code'] = self._generate_default_code(vals['categ_id'])
#         return super(ProductTemplate, self).write(vals)

#     def _generate_default_code(self, categ_id):
#         category = self.env['product.category'].browse(categ_id)
#         parent_code = category.parent_id.code if category.parent_id else ''
#         category_code = category.code or ''
        
#         # Get the last sequence number for this category
#         last_product = self.search([
#             ('default_code', 'like', f'{parent_code}{category_code}%')
#         ], order='default_code desc', limit=1)
        
#         if last_product and last_product.default_code:
#             try:
#                 sequence = str(int(last_product.default_code[-5:]) + 1).zfill(5)
#             except ValueError:
#                 sequence = '00001'
#         else:
#             sequence = '00001'
            
#         return f'{parent_code}{category_code}{sequence}'


from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        # Keep track of the next sequence for each category
        category_sequences = {}
        
        for vals in vals_list:
            print(f"Creating product with vals:------------------- {vals}")
            if vals.get('categ_id'):
                categ_id = vals['categ_id']
                
                # Use cached sequence if already processed a product with this category
                if categ_id in category_sequences:
                    next_sequence = category_sequences[categ_id]
                    category_sequences[categ_id] += 1
                else:
                    # Initialize the sequence for this category
                    next_sequence = self._get_next_sequence(categ_id)
                    category_sequences[categ_id] = next_sequence + 1
                
                # Generate the code
                code = self._generate_default_code(categ_id, next_sequence)
                print(f"Generated code:----------------------- {code}")
                vals['default_code'] = code
                
        return super(ProductTemplate, self).create(vals_list)

    def write(self, vals):
        if vals.get('categ_id'):
            categ_id = vals['categ_id']
            next_sequence = self._get_next_sequence(categ_id)
            vals['default_code'] = self._generate_default_code(categ_id, next_sequence)
        return super(ProductTemplate, self).write(vals)
    
    def _get_next_sequence(self, categ_id):
        category = self.env['product.category'].browse(categ_id)
        parent_code = category.parent_id.code if category.parent_id else ''
        category_code = category.code or ''
        
        # Get the last sequence number for this category
        last_product = self.search([
            ('default_code', 'like', f'{parent_code}{category_code}%')
        ], order='default_code desc', limit=1)
        
        if last_product and last_product.default_code:
            try:
                return int(last_product.default_code[-5:]) + 1
            except ValueError:
                return 1
        else:
            return 1
    
    def _generate_default_code(self, categ_id, sequence_number=None):
        category = self.env['product.category'].browse(categ_id)
        parent_code = category.parent_id.code if category.parent_id else ''
        category_code = category.code or ''
        
        if sequence_number is None:
            sequence_number = self._get_next_sequence(categ_id)
            
        # Format as 5-digit sequence
        sequence = str(sequence_number).zfill(5)
        
        return f'{parent_code}{category_code}{sequence}'
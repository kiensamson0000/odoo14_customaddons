"""
    GỌI API CỦA ODOO BẰNG XML-RPC
    Viết thành class có thể import khi cần sử dụng. Hàm CRUD: Create: create(), Read: read(), Update: update(), Delete: delete(), Bonus: soft_delete() sẽ set field active = False, lúc này record vẫn trong database nhưng nó ẩn khỏi các câu query => không hiển thị lên giao diện Odoo.
"""

import xmlrpc.client

ODOO_BACKEND = 'http://localhost:8069'
ODOO_DB = 'test_db'
ODOO_USER = 'admin'   #  USER,NAME PASSWORD của  user mặc định (còn user, password trong odoo-server.conf là của databases)
ODOO_PASS = 'admin'


def myprint(data_list, title=''):
    if title:
        print(title)
    for line in data_list:
        print('-', line)
    pass

# https://www.odoo.com/documentation/14.0/webservices/odoo.html

class XMLRPC_API():
    def __init__(self, url, db, username='admin', password='admin'):   #Xác thực với Odoo server
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        pass

    # get fields names of the model
    def get_fields(self, model_name, required=False):
        data = self.models.execute_kw(self.db,
                                      self.uid,
                                      self.password,
                                      model_name,
                                      'fields_get',
                                      [], {'attributes': ['string', 'type', 'required', 'readonly']})

        if required:
            key_list = list(data.keys())
            for k in key_list:
                if not data[k].get('required', False):
                    data.pop(k)   # xoa pt k
                pass
        return data

    def search(self, model_name, conditions=[()]):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      model_name,
                                      'search',
                                      [conditions])

    # Create
    def create(self, model_name, data_dict):
        """
        Eg.
            model_name: 'res.users'
            data_dict: { 'name': "Minh", 'age': 27 }
        """
        id = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [data_dict])
        return id

    # Read
    def read(self, model_name, conditions=[()], params={}):
        """
        Eg.
            model_name: 'res.users'
            conditions: [('id', '>', 1)]
            params: {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        """
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      model_name,
                                      'search_read',
                                      [conditions],
                                      params)

    # Update
    def update(self, model_name, id_list, new_data_dict):
        """
        Eg.
            model_name: 'res.users'
            id_list: [7]
            new_data_dict: { 'name': "Newer partner", 'age': 27 }
        """
        self.models.execute_kw(self.db,
                               self.uid,
                               self.password,
                               model_name,
                               'write',
                               [id_list, new_data_dict])

    # Delete
    def delete(self, model_name, id_list):
        self.models.execute_kw(self.db, self.uid, self.password, model_name, 'unlink', [id_list])
        pass

    # Soft delete
    def soft_delete(self, model_name, id_list):
        self.update(model_name, id_list, {
            'active': False,
        })

    # 17/5/2021
    def call(self, model_name, method, params=[]):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, params)

    def call2(self, model_name, method, param1, param2):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, param1, param2)


def main():
    client = XMLRPC_API(url=ODOO_BACKEND, db=ODOO_DB, username=ODOO_USER, password=ODOO_PASS)

    # list vendor accounts
    myprint(client.read(model_name='my.pet',
                        conditions=[('id', '>=', 1)],
                        params={'fields': ['name', 'nickname'], }), title='Read My Pet')

    myprint(client.call2(model_name="my.pet", method="search_read", param1=[[('id', '>=', 1)]], param2={}),
            title='General Call')

    client.create(model_name="my.pet", data_dict={"name": "Kien", "nickname": "Kyz"})
    print("Created new pet")

    client.update(model_name="my.pet", id_list=[1], new_data_dict={"name": "Kitte", "nickname": "Sugar Baby"})
    print("Update new pet")

    pass


if __name__ == '__main__':
    main()


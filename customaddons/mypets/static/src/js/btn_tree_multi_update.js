// khi nhấn vào chưa xảy ra vì chưa hiện thực hành động cho nút (trigger action).
// Button mới thêm ở Qweb frontend => đính sự kiện vào button được hiện thực ở Javascript.
// Button mới "Multi Update" có class là o_list_button_multi_update (tự định nghĩa), nó sẽ liên kết với code js khai báo link sự kiện click
// Hành động thực thi sẽ gọi đến backend phương thức btn_multi_update trong model my.pet, tham số truyền vào args là rỗng
// Kết quả trả về từ backend sẽ được thực thi ở frontend với phương thức built-in do_action.
// Note: hàm renderButtons() của web.ListController mà ta thừa kế từ Odoo tại: https://github.com/odoo/odoo/blob/13.0/addons/web/static/src/js/views/list/list_controller.js#L128

odoo.define('mypets.btn_tree_multi_update', function (require) {
    "use strict";
    var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons.on('click', '.o_list_button_multi_update', this._onBtnMultiUpdate.bind(this)); // add event listener
            }
        },
        _onBtnMultiUpdate: function (ev) {
            // we prevent the event propagation because we don't want this event to
            // trigger a click on the main bus, which would be then caught by the
            // list editable renderer and would unselect the newly created row
            if (ev) {
                ev.stopPropagation();
            }
            var self = this;
            return this._rpc({
                model: 'my.pet',
                method: 'btn_multi_update',
                args: [],
                context: this.initialState.context,
            }).then(function(result) {
                // location.reload();
                self.do_action(result);
            });
        },
    });
});

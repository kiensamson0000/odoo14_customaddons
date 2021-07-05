
// Odoo use framework backbone.js cho web client
// Code 1 widget đơn giản là bôi đậm char field
//
// Quá trình dev JS, dùng console.log() để in ấn giá trị, check xem code mới được áp dụng chưa.

odoo.define('mypets.bold', function (require) {  //gói sau có thể kế thừa hay mở rộng bằng cách lệnh require()
    "use strict";
    // import packages
    var basic_fields = require('web.basic_fields'); //nơi hiện thực widget FieldChar, thừa kế để hiệu chỉnh nó.
    var registry = require('web.field_registry');

    // widget implementation
    // Override hàm _renderReadonly() để render text in đậm màu đỏ, code js, html (frontend developer).
    var BoldWidget = basic_fields.FieldChar.extend({
        _renderReadonly: function () {
            this._super();
            var old_html_render = this.$el.html();
            var new_html_render = '<b style="color:#ff0000;">' + old_html_render + '</b>'
            this.$el.html(new_html_render);
        },
    });

    registry.add('bold_red', BoldWidget); // add our "bold" widget to the widget registry
});
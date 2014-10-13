KindEditor.ready(function(K) {
    var editor1 = K.create('textarea[name="markdown"]', {
    cssPath : "{{ static_url('kindeditor/plugins/code/prettify.css') }}",
    uploadJson : '/upload/',
    fileManagerJson : '/upload/',
    allowFileManager : true,
    afterCreate : function() {
        var self = this;
        K.ctrl(document, 13, function() {
            self.sync();
            K('form[name=edit]')[0].submit();
            });
        K.ctrl(self.edit.doc, 13, function() {
            self.sync();
            K('form[name=edit]')[0].submit();
            });
        }
    });
    prettyPrint();
});

var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}
function init () {
    var text = document.getElementById('text');
    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}
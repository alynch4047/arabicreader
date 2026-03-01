
console.debug('arabic tt');

dojo.provide("arabic_reader_widgets.Tooltip");
dojo.require("dijit.Tooltip");
dojo.declare("arabic_reader_widgets.Tooltip",

        [ dijit.Tooltip ],

        {
        templatePath: dojo.moduleUrl("arabic_reader_widgets","templates/Tooltip.html"),
        
        postCreate: function() {
   		  this.label = '<div style="font-size:40px">' + this.label + '</div>';
   		  this.inherited("postCreate", arguments);
		}
        
});
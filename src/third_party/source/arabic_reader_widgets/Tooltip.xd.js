dojo._xdResourceLoaded({
depends: [["provide", "arabic_reader_widgets.Tooltip"],
["require", "dijit.Tooltip"]],
defineResource: function(dojo, dijit, dojox){if(!dojo._hasResource["arabic_reader_widgets.Tooltip"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["arabic_reader_widgets.Tooltip"] = true;

console.debug('arabic tt');

dojo.provide("arabic_reader_widgets.Tooltip");
dojo.require("dijit.Tooltip");
dojo.declare("arabic_reader_widgets.Tooltip",

        [ dijit.Tooltip ],

        {
        templateString:"<div class=\"dijitTooltip dijitTooltipLeft arwTooltip\" id=\"dojoTooltip\">\n\t<div class=\"dijitTooltipContainer dijitTooltipContents\" dojoAttachPoint=\"containerNode\" waiRole='alert'></div>\n\t<div class=\"dijitTooltipConnector\"></div>\n</div>\n",
        
        postCreate: function() {
   		  this.label = '<div style="font-size:40px">' + this.label + '</div>';
   		  this.inherited("postCreate", arguments);
		}
        
});

}

}});
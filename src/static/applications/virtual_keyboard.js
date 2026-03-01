/**
 * @author alynch
 */

virtual_keyboard = {
	
   show_virtual_keyboard: function() {
       
   	  var keyboard = dojo.byId('virtual_keyboard');
   	  
   	  if (! keyboard) return;
   	  
      for (var unicode_char_code = 0x621; unicode_char_code < 0x653; unicode_char_code++) {
      	if (unicode_char_code >= 0x63b & unicode_char_code <= 0x63f) {
      		continue;
      	}
      	var place_holder = document.createElement("div");
      	place_holder.className = 'keyboard_button';
      	place_holder.id = 'virtual_button_' + unicode_char_code;
        keyboard.appendChild(place_holder);
       
      	// create button
      	var hamza = String.fromCharCode(0x621);
      	var unicode_char = String.fromCharCode(unicode_char_code);
      	var label_text = '';
      	if (unicode_char_code > 0x64A) {
      		label_text = hamza + unicode_char;
      	}
      	else {
      		label_text = unicode_char;
      	}
      	
      	var button = new dijit.form.Button(
      					{label: label_text,
      					 id: 'virtual_button_' + unicode_char_code},
      				place_holder);
      	dojo.connect(button, 'onClick', virtual_keyboard.virtual_keyboard_clicked);
      	// add tooltip
        ttip = new arabic_reader_widgets.Tooltip(
        	{connectId: [button.titleNode.id], label: label_text});
      }
   },
   
   virtual_keyboard_clicked: function(){
   	  var txt = new_definition.recently_edited_dijit.attr('value');
   	  var caret_position = doGetCaretPosition(new_definition.recently_edited_dojo);
   	  var unicode_char_code = this.id;
   	  var unicode_char = String.fromCharCode(unicode_char_code.substr(15,19));
   	  var new_text = txt.substring(0, caret_position) + unicode_char + 
   	         txt.substring(caret_position);
   	  new_definition.recently_edited_dijit.attr('value', new_text);
   	  setCaretPosition(new_definition.recently_edited_dojo, caret_position + 1);
   	  if (new_definition.is_root_widget(new_definition.recently_edited_dijit)) {
   	     new_definition.root_changed();
   	  }
   }
};
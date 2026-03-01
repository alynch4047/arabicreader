font_manager = {

	_dialog_selected_arabic_family: null,
	_dialog_selected_arabic_size: null,

	init : function() {
		font_manager.populate_font_family();
		font_manager.populate_font_size();
		login_.register_authentication_change_callback(font_manager.update_state);
		preferences_manager.register_authentication_change_callback(
												font_manager.preferences_changed);
		font_manager.preferences_changed();
	},
	
    preferences_changed: function() {
		var preferences = preferences_manager.get_preferences();
		var central_text_node = dojo.byId('central_text');
		if (preferences.central_text_font_family) {
			central_text_node.style.fontFamily = preferences.central_text_font_family;
		}
		if (preferences.central_text_font_size) {
			central_text_node.style.fontSize = preferences.central_text_font_size + 'px';
		}
    },
	
    populate_font_family: function(user_id) {
   	
        var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: [{name: 'Arabic Typesetting'},
			                {name: 'Simplified Arabic'},
			                {name: 'Simplified Arabic Bold'},
			                {name: 'Simplified Arabic Fixed'},
			                {name: 'Traditional Arabic'},
			                {name: 'Traditional Arabic Bold'},
			                {name: 'Arial'},
			                {name: 'Verdana'},
			        		{name: 'Tahoma'} ] }
			}
		   );
        
        var arabic_font_families_combo = dijit.byId('central_text_arabic_font_family');
        arabic_font_families_combo.store = options;
	},
	
    populate_font_size: function(user_id) {
   	
	    var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: [{name: '14'},
			                {name: '16'},
			                {name: '18'},
			                {name: '20'},
			                {name: '24'},
			                {name: '28'},
			        		{name: '32'} ] }
			}
		   );
	    
	    var arabic_font_size_combo = dijit.byId('central_text_arabic_font_size');
	    arabic_font_size_combo.store = options;
	},
	
	choose_arabic_font_family: function(font_family) {
		console.debug('family is ' + font_family);
		font_manager._dialog_selected_arabic_family = font_family;
	},
	
	choose_arabic_font_size: function(font_size) {
		console.debug('size is ' + font_size);
		font_manager._dialog_selected_arabic_size = font_size;
	},
	
	change_font: function() {
		console.debug('change font to ' + font_manager._dialog_selected_arabic_family + 
								font_manager._dialog_selected_arabic_size);
		var central_text_node = dojo.byId('central_text');
		if (font_manager._dialog_selected_arabic_family) {
			central_text_node.style.fontFamily = font_manager._dialog_selected_arabic_family;
		}
		if (font_manager._dialog_selected_arabic_size) {
			central_text_node.style.fontSize = font_manager._dialog_selected_arabic_size + 'px';
		}
		console.debug('new family is ' + central_text_node.style.fontFamily);
		console.debug('new size is ' + central_text_node.style.fontSize);
		
		var preferences = {
				central_text_font_family: font_manager._dialog_selected_arabic_family,
				central_text_font_size: font_manager._dialog_selected_arabic_size
				};
		preferences_manager.set_preferences(preferences);
	},

	update_state : function() {
		var user_id = read_cookie('user_id');
	}
};

/**
 * @author alynch
 */

new_definition = {
	
   recently_edited_dijit:  null,
   
   recently_edited_dojo:  null,
   
   state: 'New', // could be 'New' or 'Update'
   
   hide: function() {
     var new_definition_node = dojo.byId('maintain_database_panel');
     new_definition_node.style.display = 'none';
   },
   
   init: function() {
   	
      virtual_keyboard.show_virtual_keyboard();

      var root_f = dojo.byId('root_f');
      var root_c = dojo.byId('root_c');
      var root_l = dojo.byId('root_l');
      
      dojo.connect(root_f, 'onfocus', new_definition.enter_widget);
      dojo.connect(root_c, 'onfocus', new_definition.enter_widget);
      dojo.connect(root_l, 'onfocus', new_definition.enter_widget);
      
      dojo.connect(root_f, 'onchange', new_definition.root_changed);
      dojo.connect(root_c, 'onchange', new_definition.root_changed);
      dojo.connect(root_l, 'onchange', new_definition.root_changed);
      
      new_definition.hide();
      
      new_definition.set_title('Database Definitions');
   },
   
   root_changed: function() {
      console.debug('root changed');
      var root_f = dijit.byId('root_f').attr('value');
      var root_c = dijit.byId('root_c').attr('value');
      var root_l = dijit.byId('root_l').attr('value');
      var root_ =root_f + root_c + root_l;
      if (root_ !== '') {root.get_word_meanings_of_root(root_);}
   },

   add_word_from_sample: function(word_text) {
   	  console.debug('add new word for ' + word_text);
   	  
   	  new_definition.set_state('New');
   	
      var new_definition_header = dojo.byId('new_definition_header');
	  new_definition_header.innerHTML = 'Definition for ' + word_text;
	  
	  var possible_texts_combo = dijit.byId('possible_word_texts');
	  possible_texts_combo.attr('value', word_text);
	  
	  new_definition.get_possible_texts_word(word_text);
	  
	  var speed_aids_dialog = dijit.byId('speed_aids_dialog');
	  speed_aids_dialog.show();
	  
   },
   
   set_state: function(state) {
       new_definition.state = state;
	   if (state == 'New') {
	   	  db_navigate.current_kalima_id = 'New';
	   }
	   db_data_form.new_();
   },
   
   set_title: function(title) {
      var new_definition_header = dojo.byId('new_definition_header');
	  new_definition_header.innerHTML = title;
   },
   
   get_possible_texts_word: function (word){
      var address = "/services/sarf/possiblewordtexts/" + encodeURIComponent(word);
      function set_possible_texts_(data) {
        return new_definition.set_possible_texts(data, word);
      }
      network.pass_reponse_to_function(address, set_possible_texts_, 'json');
   },
   
   set_possible_texts: function(data, word) {
   	  console.debug('get possible texts ' + word);
      var success = data.success;
      var texts = data.data;
      console.debug(texts);
      
      var text_strings = [];
      var text = null;
      for (text_ix in texts) {
    	 text = texts[text_ix][0];
    	 text_strings[text_ix] = text;
      }
      remove_array_duplicates(text_strings);
      var option_items = [];
      for (text_ix in text_strings) {
    	 text = text_strings[text_ix];
    	 console.debug('add item ' + text);
    	 option_items[text_ix] = {name: text};
      }
      var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: option_items }
			}
		);
	
      var possible_texts_combo = dijit.byId('possible_word_texts');
      possible_texts_combo.store = options;
      
      new_definition.possible_text_changed();
      
   },
   
   possible_text_changed: function() {
   	  console.debug('possible text changed');
   	  var possible_texts_combo = dijit.byId('possible_word_texts');
   	  var text = possible_texts_combo.attr('value');
   	  
	  db_data_form.initialise_words_from_sample(text);
	  new_definition.get_and_set_proposed_roots(text);
	  
   },
   
   get_and_set_proposed_roots: function (word){
      var address = "/services/sarf/possibleroots/" + encodeURIComponent(word);
      network.pass_reponse_to_function(address, new_definition.set_proposed_roots, 'json');
   },
   
   set_proposed_roots: function(data) {
      var success = data.success;
      var roots = data.data;
     
      if (success === 0) {
          return;
      }
       
      console.debug('possible roots are %s', roots);
   	  
      var proposed_roots = dijit.byId("proposed_roots");
      
      var option_items = [];
      for (root_ix in roots) {
    	 var root = roots[root_ix];
    	 console.debug('add item ' + root);
    	 option_items[root_ix] = {name: root};
      }
      var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: option_items }
			}
		);
	
      proposed_roots.store = options;
      
      new_definition.possible_root_changed();
   },
   
   possible_root_changed: function() {
   	  console.debug('possible root changed');
   	  var proposed_roots_combo = dijit.byId('proposed_roots');
   	  var root = proposed_roots_combo.attr('value');
   	  
 	  var root_f = dijit.byId('root_f');
	  root_f.attr('value', root.substring(0,1));
	  
	  var root_c = dijit.byId('root_c');
	  root_c.attr('value', root.substring(1,2));
	  
	  var root_l = dijit.byId('root_l');
	  root_l.attr('value', root.substring(2,3));
	  
	  new_definition.root_changed();
   },
   
   
   show_status: function (status_) {
   	var status_node = dojo.byId('add_to_db_status');
   	status_node.innerHTML = status_;
   },
   
   is_root_widget: function (widget) {
   	  var root_f = dijit.byId('root_f');
      var root_c = dijit.byId('root_c');
      var root_l = dijit.byId('root_l');
      if (widget == root_f)	{return true;}
      if (widget == root_c)	{return true;}
      if (widget == root_l)	{return true;}
      return false;
   },
   
   enter_widget: function () {
   	  console.debug('enter widget this is ' + this.id);
      new_definition.recently_edited_dijit = dijit.byId(this.id);
      new_definition.recently_edited_dojo = dojo.byId(this.id);
   }
};
/**
 * @author alynch
 */
 
db_data_form = {
	
	rows: {},
	
   noun_verb_changed: function() {
	 db_data_form._save_state_to_rows();
	 db_data_form._set_word_type_from_html();
	 for (ix in db_data_form.rows) {
      	var row = db_data_form.rows[ix];
      	row.word_type = db_data_form.word_type;
	 }
   	 db_data_form._create_words_table();
   },
	
   _create_words_table: function() {
   	var words_table_html = '';
      for (ix in db_data_form.rows) {
      	var row = db_data_form.rows[ix];
      	words_table_html += row.get_html();
      }
      table_html = '<table>' + words_table_html + '</table>';
      var words_table_node = dojo.byId('vocab_db_words_table');
      words_table_node.innerHTML = table_html;
      dojo.parser.parse(words_table_node);
      for (ix in db_data_form.rows) {
      	var row = db_data_form.rows[ix];
      	row.connect_text_to_enter_widget();
      }
   },
   
   _create_rows_from_words: function() {
   	  db_data_form.rows = {};
      for (ix in db_data_form.words) {
      	var word = db_data_form.words[ix];
      	var kalvar_id = word[0];
        var text = word[1];
        var tense = word[2];
        var number = word[3];
        var gender = word[4];
      	var row = new DBDataFormRow(db_data_form.word_type,
      								kalvar_id, text, tense, number, gender);
      	db_data_form.rows[row.row_id] = row;
      }
   },
   
   _save_state_to_rows: function() {
   	// save the state of the html rows to the rows object
   	
   	for (ix in db_data_form.rows) {
      	var row = db_data_form.rows[ix];
      	row.word_type = db_data_form.word_type;
      	row.save_state();
    }
   },
   
   add_new_variation: function() {
   	 console.debug('add new variation');
   	 db_data_form._save_state_to_rows();
   	 var row = new DBDataFormRow(db_data_form.word_type, 'new', '', 1, 1, 0);
   	 db_data_form.rows[row.row_id] = row;
   	 db_data_form._create_words_table();
   },
   
   delete_variation: function(row_id) {
   	 console.debug('delete variation row ' + row_id);
   	 db_data_form._save_state_to_rows();
   	 delete db_data_form.rows[row_id];
   	 db_data_form._create_words_table();
   },
   
   initialise_words_from_sample: function(word_text) {
   	 db_data_form._set_word_type_from_html();
   	 var row = new DBDataFormRow(db_data_form.word_type, 'new', word_text, 1, 1, 0);
   	 db_data_form.rows = {};
   	 db_data_form.rows[row.row_id] = row;
   	 db_data_form._create_words_table();
   },
   
   _set_word_type_from_html: function() {
   	 word_type_desc = dijit.byId('word_type').attr('value');
   	 db_data_form.word_type = lookups.word_types_reverse[word_type_desc];
   },
   
   new_: function() {
   	 db_data_form.rows = {};
   	 db_data_form._create_words_table();
   },
   
   set_form_data: function(data) {
      success = data.success;
      form_data = data.data;
      if (success === 0) {
      	 console.debug('error getting form data');
      	 return;
      }
      db_data_form.kalima_id = form_data[0];
      db_data_form.root = form_data[1];
      db_data_form.word_type = form_data[2];
      db_data_form.meaning = form_data[3];
      db_data_form.nickname = form_data[4];
      db_data_form.words = form_data[5];
      
      db_navigate.current_kalima_id = db_data_form.kalima_id;
	  
	  var meaning_widget = dijit.byId('new_word_text_meaning');
	  meaning_widget.attr('value', db_data_form.meaning);
	  
	  var nickname_node = dojo.byId('new_word_creator_nickname');
	  nickname_node.innerHTML = db_data_form.nickname;
	  
	  var root_f = dijit.byId('root_f');
      var root_c = dijit.byId('root_c');
      var root_l = dijit.byId('root_l');
      if (db_data_form.root !== null && db_data_form.root.length >= 3) {
      	root_f.attr('value', db_data_form.root.substring(0,1));
      	root_c.attr('value', db_data_form.root.substring(1,2));
      	root_l.attr('value', db_data_form.root.substring(2,3));
      }
      else {
      	root_f.attr('value', '');
      	root_c.attr('value', '');
      	root_l.attr('value', '');
      }
      
      var word_type_widget = dijit.byId('word_type');
      word_type_widget.attr('value', lookups.word_types[db_data_form.word_type]);
      
      db_data_form._create_rows_from_words();
      db_data_form._create_words_table(db_data_form.words);
      
      // update the title bar
      var title = '';
      if (db_data_form.words.length > 0) {title = db_data_form.words[0][1];}

      if (db_data_form.meaning !== null) {
      	title = title + ' (' + db_data_form.meaning + ')';
      	title = title + ' :' + db_data_form.kalima_id;
      }
      
      new_definition.set_title('Definition for ' + title);
      
      var combined_root = root_f.attr('value') + root_c.attr('value') + root_l.attr('value');
      return combined_root;
      
   },
   
   get_form_query: function() {
      var word_type_str = dijit.byId('word_type').attr('value');
      var word_type = lookups.word_types_reverse[word_type_str];
      var root_f = dijit.byId('root_f').attr('value');
      var root_c = dijit.byId('root_c').attr('value');
      var root_l = dijit.byId('root_l').attr('value');
   	  var meaning = dijit.byId('new_word_text_meaning').attr('value');
   	  
   	  var query = '?kalima_id=' + db_navigate.current_kalima_id;
   	  query += '&word_type=' + word_type;
   	  query += '&root_f=' + encodeURIComponent(root_f);
   	  query += '&root_c=' + encodeURIComponent(root_c);
   	  query += '&root_l=' + encodeURIComponent(root_l);
   	  query += '&meaning=' + encodeURIComponent(meaning);
   	  
   	  for (ix in db_data_form.rows) {
      	var row = db_data_form.rows[ix];
      	query += row.get_form_query(ix);
   	  }

   	  return query;
   }
  
};
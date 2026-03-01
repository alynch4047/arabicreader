/**
 * @author alynch
 */

known_word_sets = {};

floating_panels = {
		
	set_root_html: function(html) {
		var floating_root_node_content = dojo.byId('floating_word_root_pane_content');
		if (! floating_root_node_content) return;
		floating_root_node_content.innerHTML = html;
        dojo.query(".root_meaning", floating_root_node_content).forEach(
		    function(node) {
		        node.style.fontSize = dynamic_css.root_english_font_size * 0.75 + 'px';
		    }
		);
		dojo.query(".root_word", floating_root_node_content).forEach(
		    function(node) {
		        node.style.fontSize = dynamic_css.root_arabic_font_size * 0.75 + 'px';
		    }
		);
	},
		
	set_meaning_html: function(html) {
		var floating_meaning_node = dojo.byId('floating_word_meaning_pane_content');
		if (! floating_meaning_node) return;
		floating_meaning_node.innerHTML = html;
	  	dojo.parser.parse(floating_meaning_node);
	  	dojo.query(".root_meaning", floating_meaning_node).forEach(
		    function(node) {
		        node.style.fontSize = dynamic_css.word_meaning_english_font_size * 0.75 + 'px';
		    }
		);
		dojo.query(".root_word", floating_meaning_node).forEach(
		    function(node) {
		        node.style.fontSize = dynamic_css.word_meaning_arabic_font_size * 0.75 + 'px';
		    }
		);
	}
		
};

word_meaning = {

  update_word_meaning: function (word) {
  	var message_node = dojo.byId('word_meaning');
  	var no_meaning_found_header_node = dojo.byId('no_meaning_found_header');
  	var no_meaning_found_message_node = dojo.byId('no_meaning_found_message');
  	var add_new_word_button_node = dojo.byId('add_new_word');
  	message_node.style.display = "none";
  	add_new_word_button_node.style.display = "none";
  	no_meaning_found_header_node.style.display = "block";
  	no_meaning_found_message_node.innerHTML = 'getting meaning for ' + word;
    word_meaning.get_meanings_for_word(word);
  },
  
  get_meanings_for_word: function (word){
    var address = "/services/dictionary/wordsetsmatchingtext/" + encodeURIComponent(word);
    function set_meanings(data) {
      retval = word_meaning.set_meanings_html(data, word);
      root.update_root_info(word);
      return retval;
    }
    var dfd = network.pass_reponse_to_function(address, set_meanings, 'json');
    status_.track_event('Get meaning of ' + word, dfd);
  },
  
  _set_meaning_nodes_html: function(html) {
  	var meaning_node = dojo.byId('word_meaning');
  	meaning_node.innerHTML = html;
  	dojo.parser.parse(meaning_node);
	var widget = dijit.byId('word_meaning_pane');
	widget._layoutChildren();
	floating_panels.set_meaning_html(html);
  },
   
  set_meanings_html: function (data, word) {
  	    var meaning_node = dojo.byId('word_meaning');
  	    var no_meaning_found_header_node = dojo.byId('no_meaning_found_header');
  	    var no_meaning_found_message_node = dojo.byId('no_meaning_found_message');
        console.dir(data);
        var success = data.success;
        var word_sets = data.data;
        var node_meaning = dojo.byId('word_meaning');
        node_meaning.innerHTML = '';
        if (success === 0) {
            no_meaning_found_message_node.innerHTML = 'Error looking up word';
            return;
        }
  	    meaning_node.style.display = 'block';
  	    no_meaning_found_header_node.style.display = 'none'; 
        var html = '';
        if (data.num_elements === 0) {
            meaning_node.style.display = 'none';
            no_meaning_found_header_node.style.display = 'block';
            word_meaning.show_add_new_definition_option(word);
            return;
        }
        else
        {
        	var meaning_html = word_meaning._get_meanings_html(word_sets);
        	word_meaning._set_meaning_nodes_html(meaning_html);
        }
   },
   
   _get_meanings_html: function (word_sets_json) {
   	  var html = '';
   	  var word_set_html = '';
      console.dir(word_sets_json);
      for (word_set_ix in word_sets_json) {
    	  var word_set_ = new WordSet();
      	  word_set_.populate_from_ajax_data(word_sets_json[word_set_ix]);
      	  known_word_sets[word_set_.kalima_id] = word_set_;
      	  word_set_html = word_set_.get_html();
      	  html += rounded.wrap_in_round_corners(word_set_html, ' . ');
      }
      return html;
   },
   
   show_add_new_definition_option: function (word) {
    var message_node = dojo.byId('no_meaning_found_message');
    message_node.innerHTML = '<div>No meaning found for ' + word + '</div>';
    var add_new_word_button = dojo.byId('add_new_word');
    add_new_word_button.style.display = "block";
	var show_dialog_func = function() {
       word_meaning.show_add_new_word(word);
    };
    add_new_word_button.onclick = show_dialog_func;
   },
   
   show_add_new_word: function (word) {
		mode.goto_database(true);
		new_definition.add_word_from_sample(word);
   }
};
 
/**
 * @author alynch
 */

vocab = {
	
  word_sets: {},
  
  recently_added_word_sets: [],
  
  init: function () {
  	login_.register_authentication_change_callback(vocab.login_changed);
  },
  	
  login_changed: function () {
  	vocab.word_sets = {};
  	var address = "/services/vocabulary/allwords/";
    function populate_words(data) {
        var success = data.success;
        var word_sets_data = data.data;
        if (success === 0) {
            return;
        }
        for (word_set_ix in word_sets_data) {
            var word_set_data = word_sets_data[word_set_ix];
            var word_set_ = new WordSet();
            word_set_.populate_from_ajax_data(word_set_data);
            var kalima_id = word_set_.kalima_id;
            vocab.word_sets[kalima_id] = word_set_;
        }
        vocab.re_layout();
    }
    network.pass_reponse_to_function(address, populate_words, 'json');
    vocab.re_layout();
  },
  
  add_word_set: function (kalima_id) {
	  var word_set = known_word_sets[kalima_id]
	  vocab.word_sets[kalima_id] = word_set;
	  ix = dojo.indexOf(vocab.recently_added_word_sets, word_set);
	  if (ix == -1) {
		  vocab.recently_added_word_sets.unshift(word_set);
		  if (vocab.recently_added_word_sets.length > 3) {
			  vocab.recently_added_word_sets.splice(3, 1);
		  }
	  }
	  var address = "/services/vocabulary/addword/" + kalima_id;
	  function word_added_to_vocab(data) {
		  return ;
	  }
	  network.pass_reponse_to_function(address, word_added_to_vocab, 'json');
    
	  vocab.re_layout();
  },
  
  remove_word_set: function(kalima_id) {
	  var word_set = known_word_sets[kalima_id]
	  delete vocab.word_sets[kalima_id];
	  var ix = dojo.indexOf(vocab.recently_added_word_sets, word_set);
	  console.debug('found set at ix ' + ix);
	  if (ix !== -1) {
		  console.debug('remove ix ' + ix);
		  vocab.recently_added_word_sets.splice(ix, 1);
	  }
    
	  var address = "/services/vocabulary/removeword/" + kalima_id;
	  function word_removed_from_vocab(data) {
		  return ;
	  }
	  network.pass_reponse_to_function(address, word_removed_from_vocab, 'json');
    
	  vocab.re_layout();
  },
  
  re_layout: function () {
  	var vocab_widget = dijit.byId('vocabulary_text');
  	var html = '';
  	var word_set_ = null;
  	var word_set_html = '';
  	for (ix in vocab.recently_added_word_sets) {
  		word_set_ = vocab.recently_added_word_sets[ix];
        word_set_html = word_set_.get_html(['remove_button']);
        html += rounded.wrap_in_round_corners(word_set_html, ' . ', 'black');
    }
  	vocab_widget.attr('content', html);
  },
  
  vocab_word_clicked: function (word_id, word, meaning) {
   	 console.debug('vocab clicked');
  }
};
 
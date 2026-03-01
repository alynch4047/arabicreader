/**
 * @author alynch
 */

root = {
	
  update_root_info: function (word) {
    root.get_word_meanings_of_same_root(word);
  }, 
  
  get_word_meanings_of_root: function (root_){
     var address = "/services/dictionary/wordsofroot/" + encodeURIComponent(root_);
	 network.pass_reponse_to_function(address, root.set_roots_html, 'json');
   },
  
  get_word_meanings_of_same_root: function (word_){
     var address = "/services/dictionary/wordsofsameroot/"+ encodeURIComponent(word_);
	 var dfd = network.pass_reponse_to_function(address, root.set_roots_html, 'json');
	 status_.track_event('Get root of ' + word_, dfd);
   },
   
   set_roots_html: function (data) {
        var html = '';
        var success = data.success;
        var roots = data.data;
        if (success === 0) {
            return 'The server had an error: ' + roots;
        }
        for (root_ix in roots) {
            var root_data = roots[root_ix];
            var root_letters = root_data[0];
            var root_word_sets = root_data[1];
            var variation_html = null;
            var word_set_html = null;
            for (word_set_ix in root_word_sets) {
            	var word_set_ = new WordSet();
            	word_set_.populate_from_ajax_data(root_word_sets[word_set_ix]);
            	known_word_sets[word_set_.kalima_id] = word_set_;
            	word_set_html = word_set_.get_html();
            	html += rounded.wrap_in_round_corners(word_set_html, ' . ');
            }
        }
        var rootText = dijit.byId('root_text');
        rootText.attr('content', html);
        floating_panels.set_root_html(html);
   },
   
   goto_db: function(kalima_id) {
   	mode.goto_database(true);
   	db_navigate.goto_word_of_kalima_id(kalima_id);
   }

};
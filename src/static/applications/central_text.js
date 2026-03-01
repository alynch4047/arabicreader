/**
 * @author alynch
 */

central_text =  {
	
  MODE_TEXT: 1,
  
  MODE_HTML: 2,
  
  MODE_IFRAME: 3,
  
  _current_user_id: 0,
  _current_title: '',
  _current_page_no: 0,
  _num_pages: 0,
  _further_pages_available: false,
  
  _words_array: [],
  
  set_central_text: function (text) {
  	central_text.show_iframe(false);
    var central_node = dojo.byId('central_text_content');
    paragraphs = central_text._split_paragraphs(text);
    var paragraphs_html = '';
    var words_html = '';
    var next_ix = 0;
    central_text._words_array = [];
    for (pix in paragraphs) {
    	text = paragraphs[pix];
    	words = central_text._split_central_text_words(text);
    	words_html = central_text._get_words_span_html(words, next_ix);
    	next_ix += words.length;
    	paragraphs_html += '<P>' + words_html + '</P>';
    }
    central_node.innerHTML = paragraphs_html; 
  },
  
  set_central_html: function (html) {
  	central_text.show_iframe(false);
    var central_node = dojo.byId('central_text_content');
    central_node.innerHTML = html;
    dojo.parser.parse(central_node);
  },
  
  set_central_srclink: function(url) {
  	central_text.show_iframe(true);
    var central_node = dojo.byId('central_text_iframe');
    central_node.src = "/services/proxy/geturl/" + url;
  },
  
  goto_previous_page: function() {
	var next_page_no = central_text._current_page_no - 1;
	var bookmark = 'documents_' + central_text._current_user_id + '_' + 
								central_text._current_title + '_' + next_page_no;
	mode.add_to_back_history(bookmark);  
  	central_text.set_central_librarytext(central_text._current_user_id, 
  										 central_text._current_title,
  										 next_page_no);
  },
  
  goto_next_page: function() {
	var next_page_no = central_text._current_page_no + 1;
	var bookmark = 'documents_' + central_text._current_user_id + '_' + 
								central_text._current_title + '_' + next_page_no;
	mode.add_to_back_history(bookmark);  
  	central_text.set_central_librarytext(central_text._current_user_id, 
  										 central_text._current_title,
  								    	 next_page_no);
  },
  
  set_central_librarytext: function(user_id, title, page_no) {
  	central_text.show_iframe(true);
    var address = "/services/library/documents/" + user_id + "/" + title + "/" + (page_no - 1);
    function _populate_text(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
        }
        else {
        	var result = data.data;
        	var text = result.text;
        	var num_pages = result.num_pages;
        	var further_pages_available = result.further_pages_available
        	console.debug('num pages = ' + num_pages);
        	console.debug('further_pages_available = ' + further_pages_available);
        	central_text.set_central_text(text);
        	central_text._current_user_id = user_id;
  			central_text._current_title = title;
  			central_text._current_page_no = page_no;
  			central_text._num_pages = num_pages;
  			central_text._further_pages_available = further_pages_available;
  			central_text._disable_previous_next_button();
        }
     }
     var login_response = network.pass_reponse_to_function(address, _populate_text, 'json');
  },
  
  _disable_previous_next_button: function() {
	var previous_page_widget = dijit.byId('navigate_previous_page');
	var next_page_widget = dijit.byId('navigate_next_page');
	if (central_text._current_page_no == 1) {
		previous_page_widget.attr('disabled', true);
	}
	else {
		previous_page_widget.attr('disabled', false);
	}
	if (! central_text._further_pages_available) {
		next_page_widget.attr('disabled', true);
	}
	else {
		next_page_widget.attr('disabled', false);
	}
  },
  
  show_iframe: function(show) {
  	var central_iframe_node = dojo.byId('central_text_iframe');
  	var central_plain_node = dojo.byId('central_text');
  	if (show) {
  		central_iframe_node.style.display = 'block';
  		central_plain_node.style.display = 'none';
  	}
  	else {
  		central_iframe_node.style.display = 'none';
  		central_plain_node.style.display = 'block';
  	}
  },
  
  resize_inner_frame: function() {
  	// this is called from code in the IFrame HTML (iframe_ar.js)
  	var central_node = dojo.byId('central_text_iframe');
    inner_height = (central_node.contentWindow.document.body.scrollHeight + 50) + "px";
  	central_node.style.height = inner_height;
  },
  
  _split_paragraphs: function(text) {
	  return text.split('\n');
  },
  
  _split_central_text_words: function(text) {
  	return text.split(/\s+/);
  },
  
  _get_words_span_html: function (words, ix_offset) {
    var span_html = '';
    var ix = 0;
    for (ix in words) {
        word = words[ix];
        words_array_ix = parseInt(ix, 10) + ix_offset;
        central_text._words_array[words_array_ix] = word;
        word_span = '<span id=central_word_'+ words_array_ix +
                  ' onclick="central_text.central_word_clicked_by_ix(' + words_array_ix + ')"' +
                  ' onmouseover="central_text.mouse_over_central_word('+ words_array_ix + ')"' +
                  ' onmouseout="central_text.mouse_out_central_word('+ words_array_ix + ')">' +
                   word + ' </span>';
        span_html = span_html.concat(word_span);
    }
    return span_html;
  },
  
  mouse_over_central_word: function (ix) {
    var word_element = dojo.byId('central_word_'+ ix);
    word_element.className = 'moused_central_word';
  },
  
  mouse_out_central_word: function (ix) {
    var word_element = dojo.byId('central_word_'+ ix);
    word_element.className = 'normal_central_word';
  },
  
  central_word_clicked_by_ix: function (ix) {
    var word = central_text._words_array[ix];
    word = central_text._strip_punctuation(word);
    word_meaning.update_word_meaning(word);
  },
  
  _strip_punctuation: function (word) {
  	var skip_letters = ['(',')','[',']','{','}',',','.','\u060c','\t',
  	                    ':',';','?','\u061f', '؟'];
  	var changed = true;
  	while (changed) {
  		changed = false;
	  	for (ix in skip_letters) {
	  		skip_letter = skip_letters[ix];
	  		if (central_text._last_letter(word) == skip_letter) {
		  		word = word.substring(0, word.length - 1);
		  		changed = true;
		  		break;
		  	}
		  	if (central_text._first_letter(word) == skip_letter) {
		  		word = word.substring(1, word.length);
		  		changed = true;
		  		break;
		  	}
	  	}
  	}
  	return word;
  },
  
  _last_letter: function (word) {
  	return word.substring(word.length - 1, word.length);
  },
  
   _first_letter: function (word) {
  	return word.substring(0, 1);
  },
  
  _get_unique_arabic_words: function (node) {
	  var all_words = {};
	  function find_words(text) {
			// good trim implementation
			text = text.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
			text = text.replace('\n', '');
			var words = text.split(/[\s\!\?\.\:\}\{\؟]+/);
			for (ix in words) {
				if (arabic.is_arabic_word(words[ix])) {
					all_words[words[ix]] = true;
				}
			}
	  }
	  word_finder = new Translator(find_words);
	  word_finder.traverse(node);
	  return all_words;
  },
  
  _highlight_words: function (words) {
	  node = dojo.byId('central_text');
	  console.debug('words is');
	  console.debug(words);
	  function highlight_words(text, node) {
		  // good trim implementation
		  text = text.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
		  text = text.replace('\n', '');
		  text = central_text._strip_punctuation(text);
		  // if text matches one of the words then return highlighted node
		  if (text in words) {
			  node.parentNode.setAttribute('style', 'color:red');
		  } else {
			  node.parentNode.setAttribute('style', 'color:black');
		  }
		  
	  }
	  word_finder = new Translator(highlight_words);
	  word_finder.traverse(node);
  },
  
  highlight_unknown_words: function () {
	  node = dojo.byId('central_text');
	  var all_words = central_text._get_unique_arabic_words(node);
	  console.debug(all_words);
	  var address = "/services/dictionary/unknownwords/";
	  function _highlight_words(data) {
	      var success = data.success;
	      var error = data.data;
	      if (success === 0) {
	            console.debug(error);
	      }
	      else {
	        	var words = data.data;
	        	var num_words = 0;
	        	for (word in words) { num_words ++;}
	        	alert('ArabicReader found ' + num_words + ' unknown words!');
	        	central_text._highlight_words(words);
	      }
	  }
	  var dfd = network.pass_reponse_to_function(address, _highlight_words, 'json',
			  								null, true, {words: all_words},
			  											120000);
	  var num_words = 0;
  	  for (word in all_words) { num_words ++;}
	  status_.track_event('Check ' + num_words + ' words', dfd);
  },
  
  central_word_clicked: function (word) {
    word_meaning.update_word_meaning(word);
  }
  
};
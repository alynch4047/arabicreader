
/**
 * @author alynch
 */

function init_arabic_reader()
  {
	  dojo.back.setInitialState(mode.goto_about);
	  mode.goto_about(true);
  	  login_.init();
      navigate_.init();
      vocab.init();
      new_definition.init();
      library.init();
      html_maker.init();
   	  upload_.init();
   	  main_menu.init();
   	  my_reader.init();
   	  db_navigate.init();
   	  font_manager.init();
   	  revise.init();
      
      login_.server_changed_user_id();
      
      app_url = window.location.href;
      if (app_url.split("#").length > 1) {
    	  bookmark = app_url.split("#")[1];
    	  mode.goto_bookmark(bookmark);
      }
      else {
    	  mode.goto_about(true);
      }
      // show example word
      reader = 'قراءة';
      setTimeout(function () {word_meaning.update_word_meaning(reader);}, 1000);
  }
  

preferences_manager = {
		
  authentication_change_callbacks: [],
  
  _preferences: {},
  
  _preferences_fetched: false,
  
  get_preferences: function() {
	  if (! preferences_manager._preferences_fetched) {
		  preferences_manager.fetch_preferences();
		  preferences_manager._preferences_fetched = true;
	  }
	  return preferences_manager._preferences;
  },
  
  fetch_preferences: function() {
	var address = "/services/session/get_preferences/";
	function _preferences_received(data) {
		var success = data.success;
		var error = data.data;
		if (success === 0) {
			console.debug(error);
		}
		else {
			preferences_manager._preferences = data.data;
			console.debug('preferences is ' + data.data);
			preferences_manager._notify_authentication_callbacks();
		}
	}
	var login_response = network.pass_reponse_to_function(address, _preferences_received, 'json');
  },
  
  update_preferences: function() {
	  function preferences_updated() {
		  var success = data.success;
			var error = data.data;
			if (success === 0) {
				console.debug(error);
			}
			else {
				console.debug('preferences updated');
			}
	  }	  
	  var address = "/services/session/set_preferences/";
	  var arg_details = {
	   			address: address,
	   			func: preferences_updated,
	   			use_post: true,
	   			post_data: {preferences: preferences_manager._preferences},
	   			handle_as_type: 'json'
	   	 };
	     network.pass_reponse_to_function(arg_details);
  },
  
  set_preferences: function(preferences) {
	  for (preference in preferences) {
		  preferences_manager._preferences[preference] = preferences[preference];
		  preferences_manager.update_preferences();
	  }
	  console.dir(preferences_manager._preferences);
	  preferences_manager.update_preferences();
  },
  
  register_authentication_change_callback: function(func) {
	preferences_manager.authentication_change_callbacks.push(func);
  },
  
  _notify_authentication_callbacks: function() {
  	 console.dir(preferences_manager.authentication_change_callbacks);
     for (ix in preferences_manager.authentication_change_callbacks) {
    	var callback = preferences_manager.authentication_change_callbacks[ix];
    	callback();
    }
  }
};

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



lookups = {

	word_types: { 1: 'Noun', 2: 'Verb', 3: 'Preposition', 4: 'Conjunction',
	 	5: 'Interrogative', 6: 'Name'
	},
	
	word_types_reverse: { 'Noun': 1, 'Verb': 2, 'Preposition': 3, 'Conjunction': 4,
	 	'Interrogative': 5, 'Name': 6
	}

};



arabic =  {

  // always use caps for hex
  replacement:  { 'x600': 0x600,
//                  'x649': 0x64A,
                  'x6E1': 0x652,
                  'x670': 0x627,
                  'x671': 0x627
  },
  //PDF pop directional format
  skip: { 'x202c': 1
  },
  
  is_arabic_word: function(text) {
		var char_0 = text.charCodeAt(0);
		if (char_0 < 0x600 || char_0 > 0x700) {
			return false;
		}
		return true;
  },

  normalise_arabic: function (text) {
    // remove all 0x0A s
  	text = text.replace('\n', '');
  	var normalised_text = '';
  	var chrs = text.split('');
  	for (chr_ix in chrs) {
  		var chr = chrs[chr_ix];
  		// add hexadecimal of charcode to 'x'
  		var chr_code_s = 'x' + chr.charCodeAt(0).toString(16).toUpperCase();
  		if (chr_code_s in this.replacement) {
  			normalised_text = normalised_text + 
  					String.fromCharCode(this.replacement[chr_code_s]);
  		}
  		else if (chr_code_s > 0xFB00 && chr_code_s < 0xFF00) { 
  			console.debug('lost presentation character code ' + chr + '!');
  		}
  		else if (chr_code_s in this.skip) { 
  			console.debug('skip ' + chr + '!');
  		}
  		else {
  			normalised_text = normalised_text + chr;
  		}
  	}
 	return normalised_text;
  }
};

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

/**
 * @author alynch
 */

data = {

  essay1:  "بشِّروا و لا تنفِّروا و يسِّروا و لا تعسِّروا، هذا كلام الرسول المعصوم (و إعلان صريح و خطاب واضح موجّه لحملة الإسلام، معناه التبشير بالدِّين الجديد و التّيسير على الناس و عدم تنفيرهم بالغلظة و الفظاظة، بل دعوتهم بالحكمة و الموعظة الحسنة و تذكيرهم برحمة أرحم الراحمين، إن العلماء و الدعاة و حملة الهم الإسلامي هم رسل سلام و رحمة في الحقيقة، فإذا خالف أحدهم هذا المنهج و أصبح ينفِّر الناس بشدّته و قسوته و يقنّطهم من رحمة الله فإنما لخلل في نفسه هو، و إلا فإن رسالة الإسلام رسالة حب و سلام و رحمة و هداية، يقول الله تعالى (و ما أرسلناك إلا رحمةً للعالمين)، و لهذا أنهى إخواني من الدعاة الذين يهدِّدون الناس بخطبهم و يتوعَّدونهم و كأن الرحمة و العذاب بأيديهم، و البعض يتكلم للناس بمثالية و تعالٍ، و كأنه في برج عالٍ أو من فصيلة أخرى لا يذنب و لا يخطئ، و الله يقول: (و لو لا فضل الله عليكم و رحمته ما زكى منكم من أحد أبدا)، لماذا لا نعترف بإنسانيتنا و قصورنا و عجزنا؟ و لماذا لا نخاطب الناس على أننا مثلهم و هم مثلنا كلّنا بشرٌ نصيب ونخطئ، نذنب ونستغفر، ننجح و نخفق، لا أحد منّا يملك الوصاية المطلقة على الإسلام، و لا أحد منّا هو الناطق الرسمي الوحيد باسم بالدِّين، فليس عندنا في الإسلام (بابا) و لا (ماما) كلّنا أهل رسالة ربّانّية عالمية هي رسالة سلام و إخاء و بشرى و هداية و رحمة، لا أحد أذكى و لا أطهر ولا أنبل و لا أكرم من محمد، و لهذا ذكّره ربه بالأسلوب الجميل في الدعوة فقال: (فبما رحمة من الله لنت لهم و لو كنت فظا غليظ القلب لانفضوا من حولك فاعف عنهم و استغفر لهم و شاورهم في الأمر) إن كلمات الوعيد و التهديد في الموعظة و التّنفير و الحِدّة المتناهية معناها أن المتكلم لم يفهم إلى الآن مقاصد هذه الشريعة المحمدية، فهو يتكلم على حسب طبيعته هو المركَّبة من الفظاظة و الغلظة و القسوة، فأخذ يعبِّر عن الإسلام لكن بفكرته التشاؤمية السوداوية و كيف يصغي لخطابنا من نخبره أنه شرّير و أن الله لا يغفر له و أن النار تنتظره و نمطره صباح مساء بالويل و الثبور و عظائم الأمور، مع العلم بأن الكتاب و السنة بشَّرا بالتوبة و اللطف من الله و الرحمة الواسعة و المستقبل الجميل و المنقلب الحسن (قل يا عبادي الذين أسرفوا على أنفسهم لا تقنطوا من رحمة الله إن الله يغفر الذنوب جميعا إنه هو الغفور الرحيم) إن مفاتيح الجنّة بيد الله وحده جل في علاه، و هو الذي خلقنا من تراب و علم ضعفنا، و هو غني عنّا و مع ذلك دعانا بالرفق و اللين و وعدنا رحمته و هو ارحم الراحمين، فكيف يأتي بعضنا يستعرض علينا قدراته البيانية و ملكاته الخطابية و يحاصرنا بالتّبكيت و التأنيب و التّسفيه و التّجهيل؟ و في الحديث الصحيح أن رجلاً عابداً نصح أحد العصاة فلم يستجب له العاصي، فقال العابد للعاصي: و الله لا يغفر الله لك، فقال الله تعالى: من الذي يتألَّى عليَّ؟ أشهدكم أني غفرت لهذا العاصي و أحبطتُ عمل هذا العابد.",
  
  essay2:  "يكتب  تكتب ولدتُ ولدت  ولد يُسْر خلق قتن و طلع للكتاب لكتاب الكتاب كتاب بالكتاب بكتاب خالق يسر"

};




html_maker = {
	
	init: function() {
		var tags = ['div', 'table', 'tr', 'td', 'p'];
		html_maker._tag_wrapper(tags);
	},
	
	_tag_wrapper: function(tag_list) {
		var tag;
		for (ix in tag_list) {
		  tag = tag_list[ix];
		  lambda = html_maker._make_func(tag);
		  html_maker[tag] = lambda;
		}
		
	},
	
	make_row: function(cells) {
	  html = '';
	  for (ix in cells) {
	  	cell = cells[ix];
	  	html += html_maker.td(cell);	
	  }
	  html = html_maker.tr(html);
	  return html;
		
	},
	
	_make_func: function(tag) {
		function lambda(content) {
		  	return '<' + tag + '>' + content + '</' + tag + '>';
		  }	
		 return lambda;
	}
	
};




/**
 * @author alynch
 */

mode = {
	
	_in_full_screen: false,
	
   initial_state: {
       back: function() {
       },
       
       forward: function() {
       }	
   },
   
   state_in_about: {
   	   
   	   changeUrl: 'about',
   	
       back: function() {
          mode.goto_about();	
       },	
       forward: function() {
          mode.goto_about();	
       }
   },
   
   state_in_login: {
   	   
   	   changeUrl: 'login',
   	
       back: function() {
          mode.goto_login();	
       },	
       forward: function() {
          mode.goto_login();	
       }
   },
   
   state_in_signup: {
   	   
   	   changeUrl: 'signup',
   	
       back: function() {
          mode.goto_signup();	
       },	
       forward: function() {
          mode.goto_signup();	
       }
   },
   
   state_in_help: {
   	   
   	   changeUrl: 'help',
   	
       back: function() {
          mode.goto_help();	
       },	
       forward: function() {
          mode.goto_help();	
       }
   },
   
   state_in_myreader: {
   	   
   	   changeUrl: 'myreader',
   	
       back: function() {
          mode.goto_my_reader();	
       },	
       forward: function() {
          mode.goto_my_reader();	
       }
   },
   
   state_in_read: {
   	   
   	   changeUrl: 'read',
   	
       back: function() {
       	var hash = location.hash;
       	if(hash.charAt(0) == "#"){
       		hash = hash.substring(1); 
       	}
       	console.debug('hash is ' + hash);
       	  if (hash != 'read') {
       	  	var memento = hash.substr(5);
       	  	mode.goto_memento(memento);
       	  }
       	  else {
          	mode.goto_read();
       	  }	
       },	
       forward: function() {
          mode.state_in_read.back();	
       }
   },
   
   state_in_upload: {
   	   
   	   changeUrl: 'upload',
   	
       back: function() {
          mode.goto_upload();	
       },	
       forward: function() {
          mode.goto_upload();	
       }
   },
   
   state_in_forum: {
   	   
   	   changeUrl: 'forum',
   	
       back: function() {
          mode.goto_forum();	
       },	
       forward: function() {
          mode.goto_forum();	
       }
   },
   
   state_in_revise: {
   	   
   	   changeUrl: 'revise',
   	
       back: function() {
          mode.goto_revise();	
       },	
       forward: function() {
          mode.goto_revise();	
       }
   },
   
   state_in_database: {
   	
   	   changeUrl: 'database',
   	
       back: function() {
          mode.goto_database(false);	
       },	
       forward: function() {
          mode.goto_database(false);	
       }
   },
   
   switch_large_web: function () {
   	 mode._in_full_screen = ! mode._in_full_screen;
     mode._show_large_web(mode._in_full_screen);
   },
   	
   _show_large_web:function(full_screen) {	
   	var text_browser_container_node = dojo.byId('text_browser_border_container');
   	var large_iframe_holder_node = dojo.byId('large_iframe_holder');
   	var embedded_iframe_holder_node = dojo.byId('embedded_iframe_holder');
   	var full_screen_button = dojo.byId('floating_full_screen_pane');
   	var iframe_node = dojo.byId('central_text_iframe');
   	var floating_word_root_node = dojo.byId('floating_word_root_pane');
   	var floating_word_meaning_node = dojo.byId('floating_word_meaning_pane');
   	if (full_screen) {
   		floating_word_meaning_node.style.display = 'block';
   	    floating_word_root_node.style.display = 'block';
   		text_browser_container_node.dislay = 'none';
   		large_iframe_holder_node.display = 'block';
   		embedded_iframe_holder_node.display = 'none';
   		large_iframe_holder_node.insertBefore(iframe_node, null);
   		full_screen_button.innerHTML = 'Exit Full Screen';
   	}
   	else {
   		floating_word_meaning_node.style.display = 'block';
   	    floating_word_root_node.style.display = 'block';
   		text_browser_container_node.dislay = 'block';
   		large_iframe_holder_node.display = 'none';
   		embedded_iframe_holder_node.display = 'block';
   		embedded_iframe_holder_node.insertBefore(iframe_node, null);
   		full_screen_button.innerHTML = 'Full Screen';
   	}
   },
   
   show_navigate_section: function (section) {
	 if (section == 'navigate_forum') {
		 window.open("http://www.arabicreader.net/smf_forum");
	   	 return;
	 }  	  
	   	 
   	 mode.show_central_text();
   	 var full_screen_button_node = dojo.byId('floating_full_screen_pane');
   	 var floating_word_meaning_node = dojo.byId('floating_word_meaning_pane');
   	 var floating_word_root_node = dojo.byId('floating_word_root_pane');
   	 var navigate_read_text_node = dojo.byId('navigate_read_text_area');
   	 var read_pane_toolbar_node = dojo.byId('read_pane_toolbar');
   	 var maintain_database_node = dojo.byId('maintain_database_panel');
   	 var about_node = dojo.byId('navigate_about');
   	 var login_node = dojo.byId('navigate_login');
   	 var signup_node = dojo.byId('navigate_signup');
   	 var read_node = dojo.byId('navigate_read');
   	 var upload_node = dojo.byId('navigate_upload');
   	 var my_reader_node = dojo.byId('navigate_my_reader');
   	 var revise_node = dojo.byId('navigate_revise');
   	 var revise_test_node = dojo.byId('revise_test');
   	 var revise_organise_node = dojo.byId('revise_organise');
   	 var revise_download_node = dojo.byId('revise_download');
   	 var help_node = dojo.byId('navigate_help');
   	 var forum_node = dojo.byId('forum_placeholder');
   	 navigate_read_text_node.style.display = 'none';
   	 full_screen_button_node.style.display = 'none';
   	 floating_word_meaning_node.style.display = 'none';
   	 floating_word_root_node.style.display = 'none';
   	 read_pane_toolbar_node.style.display = 'none';
   	 dijit.byId('navigate_and_reader_panel').resize();
   	 if (section == 'navigate_about') {
   	   about_node.style.display = 'block';
   	 }
   	 else {
   	   about_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_login') {
   	   login_node.style.display = 'block';
   	 }
   	 else {
   	   login_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_read') {
   	   navigate_read_text_node.style.display = 'block';
   	   read_pane_toolbar_node.style.display = 'block';
   	   read_pane_toolbar_node.style.height = '35px';
   	   dijit.byId('navigate_and_reader_panel').resize();
   	   read_node.style.display = 'block';
   	 }
   	 else {
   	   read_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_signup') {
   	   signup_node.style.display = 'block';
   	 }
   	 else {
   	   signup_node.style.display = 'none';
   	 }
//   	 if (section == 'navigate_web') {
//   	   //full_screen_button_node.style.display = 'block';
//   	   if (mode._in_full_screen) {
//	   	   floating_word_meaning_node.style.display = 'block';
//	   	   floating_word_root_node.style.display = 'block';
//   	   }
//   	   web_node.style.display = 'block';
//   	   central_node_iframe.style.display = 'block';
//   	   navigate_title_widgit.attr('title', 'Web');
//   	 }
//   	 else {
//   	   web_node.style.display = 'none';
//   	 }
   	 if (section == 'navigate_upload') {
   	   upload_node.style.display = 'block';
   	 }
   	 else {
   	   upload_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_database') {
   	   maintain_database_node.style.display = 'block';
   	 }
   	 else {
   	   maintain_database_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_my_reader') {
   	   my_reader_node.style.display = 'block';
   	   my_reader.populate();
   	 }
   	 else {
   	   my_reader_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_revise' || section == 'navigate_download_vocab'
   		 || section == 'navigate_organise_vocab' || section == 'navigate_test_vocab') {
   	   revise_node.style.display = 'block';
       if (section == 'navigate_test_vocab') {
       	   revise_test_node.style.display = 'block';
   	   }
   	   else {
   		   revise_test_node.style.display = 'none';
   	   }
       if (section == 'navigate_download_vocab') {
       	   revise_download_node.style.display = 'block';
   	   }
   	   else {
   		   revise_download_node.style.display = 'none';
   	   }
       if (section == 'navigate_organise_vocab') {
     	     revise_organise_node.style.display = 'block';
  	   }
  	    else {
  	        revise_organise_node.style.display = 'none';
  	   }
   	 }
   	 else {
   	   revise_node.style.display = 'none';
   	 }

   	 if (section == 'navigate_help') {
   	   help_node.style.display = 'block';
   	 }
   	 else {
   	   help_node.style.display = 'none';
   	 }
   },

   goto_about: function(push_stack) {
   	 main_menu.item_selected('about');
   	 mode.show_navigate_section('navigate_about');
   	 if (push_stack) {
			console.debug('push TBABOUT state onto stack');
			dojo.back.addToHistory(mode.state_in_about);
		}
   },
   
   goto_login: function(push_stack) {
     main_menu.item_selected('login');
   	 mode.show_navigate_section('navigate_login');
   	 if (push_stack) {
			console.debug('push TBLOGIN state onto stack');
			dojo.back.addToHistory(mode.state_in_login);
	 }
	 if (login_.authenticated) {
 	   login_.offer_logout();
     }
   },
   
   goto_signup: function(push_stack) {
   	 main_menu.item_selected('login');
   	 mode.show_navigate_section('navigate_signup');
   	 if (push_stack) {
			console.debug('push TBSIGNUP state onto stack');
			dojo.back.addToHistory(mode.state_in_signup);
		}
   },
   
   goto_help: function(push_stack) {
   	 main_menu.item_selected('help');
   	 mode.show_navigate_section('navigate_help');
   	 if (push_stack) {
			console.debug('push TBHELP state onto stack');
			dojo.back.addToHistory(mode.state_in_help);
		}
   },
   
   goto_my_reader: function(push_stack) {
   	 main_menu.item_selected('my_reader');
   	 mode.show_navigate_section('navigate_my_reader');
   	 if (push_stack) {
			console.debug('push TBMYREADER state onto stack');
			dojo.back.addToHistory(mode.state_in_myreader);
		}
   },
   
   goto_read: function(push_stack) {
   	 main_menu.item_selected('read');
	 mode.show_navigate_section('navigate_read');
   	 if (push_stack) {
			console.debug('push TBREAD state onto stack');
			mode.state_in_read.changeUrl = 'read';
			dojo.back.addToHistory(mode.state_in_read);
	 }
   },
   
   goto_upload: function(push_stack) {
   	 main_menu.item_selected('upload');
	 mode.show_navigate_section('navigate_upload');
   	 if (push_stack) {
			console.debug('push TBUPLOAD state onto stack');
			dojo.back.addToHistory(mode.state_in_upload);
		}
   },
   
   goto_forum: function(push_stack) {
   	 main_menu.item_selected('forum');
	 mode.show_navigate_section('navigate_forum');
   	 if (push_stack) {
			console.debug('push TBFORUM state onto stack');
			dojo.back.addToHistory(mode.state_in_forum);
		}
   	//location.href = 'http://www.arabicreader.net/smf_forum';
   },
   
   goto_database: function(push_stack) {
   	 main_menu.item_selected('database');
	 mode.show_navigate_section('navigate_database');
   	 if (push_stack) {
	  console.debug('push TBDATABASE state onto stack');
      dojo.back.addToHistory(mode.state_in_database);
	 }
   },
   
   goto_revise: function(push_stack) {
   	 main_menu.item_selected('revise');
	 mode.show_navigate_section('navigate_revise');
   	 if (push_stack) {
	  console.debug('push TBREVISE state onto stack');
      dojo.back.addToHistory(mode.state_in_revise);
	 }
   	 mode.goto_organise_vocab();
   },
   
   goto_test_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_test_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
},
   
   goto_download_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_download_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
   },
   
   goto_organise_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_organise_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
	   	 organise_vocab.populate();
 },
   
   goto_url: function(url) {
   	mode.goto_read(true);
    central_text.set_central_srclink(url);
  },
  
   goto_library_document: function(user_id, title) {
   	mode.goto_read(true);
    central_text.set_central_librarytext(user_id, title, 1);
  },
   
   add_to_back_history: function(bookmark) {
	   bookmark = encodeURIComponent(bookmark);
	   history_state = {
		   	   
		   	   changeUrl: bookmark,
		   	
		       back: function() {
		          mode.goto_bookmark(bookmark);	
		       },	
		       forward: function() {
		          mode.goto_bookmark(bookmark);	
		       }
	   };
	   dojo.back.addToHistory(history_state);
   },	   
   
   goto_bookmark: function(bookmark) {
	   bookmark = decodeURIComponent(bookmark);
	   console.debug('bookmark is ' + bookmark + bookmark.slice(0,9));
	   if (bookmark == 'database') {
		   dojo.back.setInitialState(mode.goto_database);
		   mode.goto_database();
	   }
	   else if (bookmark == 'read') {
		   dojo.back.setInitialState(mode.goto_read);
		   mode.goto_read();
	   }
	   else if (bookmark == 'revise') {
		   dojo.back.setInitialState(mode.goto_revise);
		   mode.goto_revise();
	   }
	   else if (bookmark.slice(0,9) == 'documents') {
		   dojo.back.setInitialState(mode.goto_read);
		   mode.goto_read();
		   details = bookmark.split('_');
		   user_id = details[1];
		   title = details[2];
		   page_no = details[3];
		   console.debug('load document ' + user_id + ' '  + title +' ' + page_no);
		   central_text.set_central_librarytext(user_id, title, page_no);
	   }
	   else {
		   dojo.back.setInitialState(mode.goto_about);
	       mode.goto_about(true);
	   }
   },
   
   show_central_text: function() {
   	 var new_definition_node = dojo.byId('maintain_database_panel');
	 var text_browser = dojo.byId('navigate_and_reader_panel');
	 new_definition_node.style.display = "none";
	 text_browser.style.display = "block";
   },
   
   show_demo_text: function () {
   	 mode.goto_read(true);
   	 navigate_.use_essay_1();
   }

};

navigate_ =  {
	
  init: function () {
    console.debug('init navigate' );
    navigate_.init_current_location();
    var full_screen_button = dojo.byId('floating_full_screen_pane');
    full_screen_button.style.display = 'none';
    var floating_word_meaning_pane = dijit.byId('floating_word_meaning_pane');
    var floating_root_pane = dijit.byId('floating_word_root_pane');
    new_dim = {w: 225, h: 80, t: 60, l: 20};
    floating_word_meaning_pane.resize(new_dim);
    new_dim.t = 150;
    new_dim.h = 250;
    floating_root_pane.resize(new_dim);
  },
  
  show_qisas: function() {
	    mode.goto_read(true);
	    central_text.set_central_srclink('www.arabicreader.net/documents/qisas/qisas_modified.htm');
	  },
  
  show_demo_web: function() {
    mode.goto_read(true);
    central_text.set_central_srclink('www.asharqalawsat.com');
  },
  
  init_current_location: function () {
  	console.debug('init current location ' + this);
  	var current_location = dojo.byId('navigate_current_location');
    dojo.connect(current_location, 'onkeypress', navigate_.current_location_keypress);
  	var current_location_widget = dijit.byId('navigate_current_location');
  	var last_visited = dojo.cookie('last_visited');
//    current_location_widget.attr('value', last_visited);
  },
  
  use_essay_1: function () {
  	console.debug('goto essay 1');
    central_text.set_central_text(data.essay1);
  },
  
  use_essay_2:  function () {
  	console.debug('goto essay 2');
    central_text.set_central_text(data.essay2);
  },
  
  nav_goto_clicked: function() {
     var sura_no_node = dojo.byId('navigate_sura_no');
     var ayat_no_node = dojo.byId('navigate_ayat_no');
     var sura_no = sura_no_node.value;
     var ayat_no = ayat_no_node.value;
     navigate_.get_ayat_text(sura_no, ayat_no);
  },
  
  get_ayat_text: function (sura_no, ayat_no) { 
    address = "/services/quran/ayat/" + sura_no + '/' + ayat_no;
	network.pass_reponse_to_function(address, central_text.set_central_text, 'text');
  },
  
  current_location_keypress: function (event) {
  	if (event.keyCode != dojo.keys.ENTER) {
  		return;
  	}
  	navigate_._goto_current_url();
  },
  
  web_suggested_urls_changed: function() {
  	console.debug('suggested url changed');
  	var suggested_urls_combo = dijit.byId('web_suggested_urls');
  	url = suggested_urls_combo.attr('value');
  	navigate_.goto_url(url);
  },
  	
  _goto_current_url: function () {	
    var current_location = dijit.byId('navigate_current_location');
    new_location = current_location.attr('value');
    console.debug('curr loc is ' + new_location + ' ' + new_location.substr(0, 7));
    if (new_location.substr(0, 7) === 'http://') {
    	new_location = new_location.substr(7);
    	console.debug('change curr loc to ' + new_location);
    }
    navigate_.goto_url(new_location);
  },
  
  goto_url: function(url) {
    dojo.cookie('last_visited', url, { expires: 5 });
    central_text.set_central_srclink(url);
  },
  
  set_url_text_and_links: function (data) {
    var body = data;
    central_text.set_central_text(body);
    
  }
};
  

/**
 * @author alynch
 */

network = {
	
  last_nickname: '',
	
  _user_id_changed: function () {
  	var nickname = read_cookie('nickname');
  	var user_id = read_cookie('user_id');
  	if (nickname !== network.last_nickname) {
	  	console.debug('new nickname is ' + nickname);
	  	network.last_nickname = nickname;
	  	login_.server_changed_user_id();
  	}
  },

  pass_reponse_to_function: function (arg0, func, handle_as_type, query,
		  							  use_post, post_data, timeout_override) {
	  
	var current_user_id = read_cookie('user_id');
  	network.last_nickname = read_cookie('nickname');
  	var hostname = location.hostname;
  	var port = location.port;
  	if (port !== '80') {
    	  hostname += ':' +  port;
    	}
  	
	var address;
	  
	if (arguments.length === 1) {
		var arg_details = arg0;
		address = arg_details.address;
		func = arg_details.func;
		handle_as_type = arg_details.handle_as_type;
		use_post = arg_details.use_post;
		post_data = arg_details.post_data;
		timeout_override = arg_details.timeout_override;
		var query_args = arg_details.query_args;
		for (key in query_args) {
			if (query) {
				query += '&';
			}
			else {
				query = '?';
			}	
			query += key + '=' + encodeURIComponent(query_args[key]);
		}
	}	
	else {
		address = arg0;
	}	

  	if (handle_as_type === 'json') {
  	    address = address + '/json';
  	}
  	
  	address = 'http://' + hostname + address;
  	
  	if (query) {
  		address = address + query;
  	}
  	
  	timeout = timeout_override || 10000;
  	
  	var xhr_func = dojo.xhrGet;
  	if (use_post === true) {
  		xhr_func = dojo.xhrPost;
  		// post_data must come in as an object e.g. {font_size: 12, font_family, 'abc'}
  		// so that it can be converted to kwargs by cherrypy
  		post_data = 'post_data=' + dojo.toJson(post_data);
  	}
  	else {
  		address = network._add_cache_buster(address);
  	}
  	
  	var dfd = xhr_func(
	 { 
        url: address, 
        handleAs: handle_as_type,
        timeout: timeout, 
        postData: post_data,

        load: function(response, ioArgs) {
          if (current_user_id != read_cookie('user_id')) {
          	try {
            	network._user_id_changed();
          	}
          	catch(e) {
          		console.error('user id change mechanism problem');
          	}
          }
          func(response);
          return response;
        },

        error: function(response, ioArgs) { 
          console.dir(response);
          console.dir(ioArgs);
          console.error("HTTP status code: ", ioArgs.xhr.status);
          return response;
        }
    }
	);
  	return dfd;
  },
  
  _add_cache_buster: function(url) {
  	var current_date = new Date();
  	var tag = '_' + current_date.getTime() + 'cb';
  	return url + tag;
  },
  
  get_text_and_links_of_url: function (url, callback_func) {
  	if (url.substr(0, 7) == 'http://') {
  		url = url.substr(7);
  	}
  	// we need to get text via proxy server because security restrictions limit
    // cross site access
  	var address = "/services/proxy/geturl/" + url;
	this.pass_reponse_to_function(address, callback_func);
  }
};


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

/**
 * @author alynch
 */

rounded = {

   wrap_in_round_corners: function(content, headline, colour) {
   	
		if (! colour) {
			colour = 'blue';
		}
		
		var class_main = 'rr_box_' + colour;
		var class_outer = 'rr_box_outer_' + colour;
		var class_inner = 'rr_box_inner_' + colour;
		var class_header = 'rr_box_header_' + colour;
	
   	    var outer_html = '<div class="' + class_main + '">' +
	   				       '<div class="' + class_outer + '">' +
	   				         '<div class="' + class_inner + '">' +
	   				           '<div class="' + class_header + '">' + headline + '</div>' +
	   				           '<div class="rr_box_content">' + content + '</div>' +
	   				         '</div>' +  
	   				       '</div>' +
	   				     '</div>'; 
   				 
   	    return outer_html;   
   }
   
};

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
 

/**
 * @author alynch
 */
 
about = {
	
//   init: function() {
//       about.populate_about();
//   },
//   
//   populate_about: function() {
//     var address = "/static/applications/about.html";
//     function _populate_about(data) {
//       central_text.set_central_html(data);
//     }
//     about_text = network.pass_reponse_to_function(address, _populate_about);
//   }   

};




/**
 * @author alynch
 */
 
login_ = {
	
   authenticated: false,
   username: '',
   nickname: '',
   
   authentication_change_callbacks: [],
	
   init: function() {
   	login_._authentication_changed();
   	login_._populate_cached_credentials();
   	
   	login_.error_dialog = new dijit.Dialog(
   			{
   			 title: "Email Already In Use",
   		     content: "<p>That email address is already in use!</p>" +
   		     		  "<p>A new password for it will be emailed to you now.</p>" +
   		     		  "<button dojoType=dijit.form.Button type='submit'>OK</button>"
   		    });
	dojo.body().appendChild(login_.error_dialog.domNode);
	login_.error_dialog.startup();
   },
   
   _populate_cached_credentials: function() {
   	  var login_name_widget = dijit.byId('login_username');
   	  var username = read_cookie('username');
   	  if (username) {
   	  	login_name_widget.attr('value', username);
   	  }
   },
   
   _save_cached_credentials: function() {
   	  var login_name_widget = dijit.byId('login_username');
   	  var user_name = login_name_widget.attr('value');
   	  console.debug('save username: ' + user_name);
   	  create_cookie('username', user_name, 1000);
   },
   
   _authentication_changed: function() {
     var nickname = read_cookie('nickname');
   	 if (! nickname || nickname.substring(0,5) === 'Guest') {
   	 	login_.authenticated = false;
   	 }
   	 else {
   		login_.authenticated = true;
   	 }
   	 login_.nickname = nickname;
   	 login_.username = read_cookie('username');
   	 login_._notify_authentication_callbacks();
   	 preferences_manager.fetch_preferences();
   },
   
   register_authentication_change_callback: function(func) {
     login_.authentication_change_callbacks.push(func);
   },
   
   _notify_authentication_callbacks: function() {
   	 console.dir(login_.authentication_change_callbacks);
     for (ix in login_.authentication_change_callbacks) {
     	var callback = login_.authentication_change_callbacks[ix];
     	callback();
     }
   },
   
   server_changed_user_id: function() {
   	login_._authentication_changed();
   },
   
   offer_logout: function() {
   	 login_.logout();
   },
   
   logout: function() {
   	 console.debug('logout 1');
   	 login_.authenticated = false;
   	 erase_cookie('nickname');
   	 erase_cookie('user_id');
   	 create_cookie('nickname', 'Guest', 1);
   	 login_._notify_authentication_callbacks();
   	 login_.show_status('You have logged off.');
   },
	
   submit_signup: function() {
   	 login_.show_status('Working...');
   	 var email_widget = dijit.byId('signup_emailaddress');
   	 var nickname_widget = dijit.byId('signup_nickname');
   	 var email = email_widget.attr('value');
   	 var nickname = nickname_widget.attr('value');
   	 
   	 var address = "/services/session/signup/" + encodeURIComponent(email) + 
   	 												"/" + encodeURIComponent(nickname);
   	 function _after_signup(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            if (error == "ERROR_EMAIL_ALREADY_IN_USE") {
            	login_.show_signup_status("That email address is already in use");
            	login_.error_dialog.show();
            	login_.show_status('Sending new password...');
            	login_.send_new_password(email);
            	mode.goto_login();
            }
            else {
            	login_.show_signup_status(error);
            }
        }
        else {
        	login_.show_signup_status('Your password has been emailed to you');
        }
        
     }
     var login_response = network.pass_reponse_to_function(address, _after_signup, 'json');
   },
   
   show_status: function(status_) {
   	 var login_status_node = dojo.byId('login_status');
   	 login_status_node.innerHTML = status_;
   },
   
   show_signup_status: function(status_) {
   	 var signup_status_node = dojo.byId('signup_status');
   	 signup_status_node.innerHTML = status_;
   },
   
   submit_login: function() {
   	 login_.show_status('Working...');
   	 var email_widget = dijit.byId('login_username');
   	 var password_widget = dijit.byId('login_password');
   	 var email = email_widget.attr('value');
   	 var password = password_widget.attr('value');
   	 console.debug('password is ' + password);
   	 var password_hash = hex_md5(password);
   	 // dummy submit to trigger browser autocomplete - unfortunately causes page to reload
   	 var login_form_node = dojo.byId('login_form');
   	 AIM.submit(login_form_node, {});
   	 var address = "/services/session/logon/" + encodeURIComponent(email) + 
   	 															"/" + password_hash;
   	 function _after_login(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            login_.show_status(error);
            login_.authenticated = false;
        }
        else {
        	login_.show_status('You have successfully logged on');
        	login_.authenticated = true;
        	login_._save_cached_credentials();
        }
     }
     var login_response = network.pass_reponse_to_function(address, _after_login, 'json');
   },
   
   forgotten_password: function() {
   	var email_address_widget = dijit.byId('login_username');
   	var forgotten_email_address_widget = dijit.byId('forgotten_email');
   	var entered_email_address = email_address_widget.attr('value');
   	forgotten_email_address_widget.attr('value', entered_email_address);
   	var forgotten_password_pane_widget = dijit.byId('forgotten_password_pane');
	forgotten_password_pane_widget.show();
   },
   
   reset_password: function(dialog_fields) {
	   login_.show_status('Sending new password...');
	   login_.send_new_password(dialog_fields.email_address);
   },
	   
   send_new_password: function(email_address) {
   	 var address = "/services/session/reset_password/" + encodeURIComponent(email_address);
   	 function _after_reset_password(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            login_.show_status(error);
        }
        else {
        	login_.show_status('You new password has been sent to you by email.');
        }
     }
     var response = network.pass_reponse_to_function(address, _after_reset_password, 'json');
 }

};




// from http://www.quirksmode.org/js/cookies.html and then tidied up

function create_cookie(name, value, days) {
	var expires = "";
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		expires = "; expires="+date.toGMTString();
	}
	document.cookie = name+"="+value+expires+"; path=/";
}

function read_cookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') {
			c = c.substring(1,c.length);
		}
		if (c.indexOf(nameEQ) === 0) {
			return c.substring(nameEQ.length,c.length);
		}
	}
	return null;
}

function erase_cookie(name) {
	create_cookie(name,"",-1);
}


/**
 * @author alynch
 */

main_menu = {
	
  init: function() {
  	login_.register_authentication_change_callback(main_menu.login_changed);
  },
  
  login_changed: function() {
  	var nickname = read_cookie('nickname');
  	main_menu._set_nickname(nickname);
  	if (login_.authenticated) {
  	  main_menu.show_logout_item();
  	}
  	else {
  	  main_menu.show_login_item();
  	}
  }, 
	
  _set_nickname: function (nickname) {
  	var nickname_node = dojo.byId('menu_nickname');
  	console.debug('set node nickname data to ' + nickname);
  	nickname_node.firstChild.data = nickname;
  },
  
  show_logout_item: function() {
    var menu_login_node = dojo.byId('menu_login');
    menu_login_node.innerHTML = 'Logout';
  },
  
  show_login_item: function() {
    var menu_login_node = dojo.byId('menu_login');
    menu_login_node.innerHTML = 'Login/Register';
  },
  
  item_selected: function (item) {
  	var menu_ids = ['read', 'upload', 'revise', 'database', 'forum',
  			    'about', 'login', 'help', 'my_reader'];
  	var menu_id = '';
  	var menu_node = null;
  	for (ix in menu_ids) {
  		menu_id = menu_ids[ix];
  		menu_node = dojo.byId('menu_' + menu_id);	
  		if (menu_id == item) {
  			menu_node.className = 'google_menu_text google_menu_chosen';
  		} 
  		else {
  			menu_node.className = 'google_menu_text';
  		}
  	}
  }
 
};


upload_ = {
	
  init: function() {
  	login_.register_authentication_change_callback(upload_.authentication_changed);
  },
  
  authentication_changed: function() {
  	upload_.update_state();
  },

  update_state: function () {
  	var upload_button_widget = dijit.byId('upload_submit');
  	if (! login_.authenticated) {
  		upload_button_widget.attr('disabled', true);
  		upload_button_widget.attr('label', 'Upload (please log on first)');
  	}
  	else {
  		upload_button_widget.attr('disabled', false);
  		upload_button_widget.attr('label', 'Upload');
  	}
  },
	
  start: function () {
  	console.debug('start upload');
  	return true;
  },
  
  finish: function () {
  	console.debug('finish upload');
  	library.update_state();
  	alert('Your document has been uploaded and should now be available from your private library.');
  }
	
};

/**
 * @author alynch
 */
 
library = {
	
   background_colour: 0xFFFFFF,
   
   colour:  0x0000,
   
   request_delete_user_id: 0,
   request_delete_title: '',
   request_share_user_id: 0,
   request_share_title: '',
	
   init: function() {
   	var download_widget = dijit.byId("library_download");
   	var text_sample_node = dojo.byId("library_colour_sample");
   	text_sample_node.innerHTML = 'هذه كتابة';  
    dojo.connect(download_widget, 'onClick', library._download_personal_text);
    library.change_colour_scheme();
    library.select_text();
    login_.register_authentication_change_callback(library.update_state);
   },
   
   select_text_old: function() {
   	 console.debug('select text');
	 var select_text_dialog_widget = dijit.byId('library_select_text_dialog');
	 select_text_dialog_widget.show();
   },
   
   get_text: function(dialog_fields) {
   	
   },
   
   select_preferences: function() {
	 var select_preferences_dialog_widget = dijit.byId('library_preferences_dialog');
	 select_preferences_dialog_widget.show();
   },
   
   preferences_done: function() {
		 var select_preferences_dialog_widget = dijit.byId('library_preferences_dialog');
		 select_preferences_dialog_widget.hide();
   },
   
   highlight_unknown_words: function() {
	   	 console.debug('highlight_unknown_words');
	   	central_text.highlight_unknown_words();
   },
   
   set_preferences: function(dialog_fields) {
   	
   },
	
   update_state: function() {
//   	 var user_id = read_cookie('user_id');
//   	 library.populate_personal_texts(user_id);
   },
   
   change_colour_scheme: function () {
   	var text_area = dojo.byId('central_text');
   	text_area.style.backgroundColor = library.background_colour;
   	text_area.style.color = library.colour;
   },
   
   set_background_colour: function(colour) {
   	 var text_sample_node = dojo.byId("library_colour_sample");
   	 library.background_colour = colour;
   	 text_sample_node.style.backgroundColor = colour;
   },
   
   set_font_colour: function(colour) {
   	 var text_sample_node = dojo.byId("library_colour_sample");
   	 library.colour = colour;
   	 text_sample_node.style.color = colour;
   },
   
   do_delete_library_file: function(user_id, title) {
   	  var address = "/services/library/delete/"+ library.request_delete_user_id + "/" + library.request_delete_title;
   	  function library_file_deleted(data) {
   	  	if (data.success) {
   	  		var message = data.data;
   	  		alert(message);
   	  	}
   	  	else {
   	  		var error = data.data;
   	  		alert(error);
   	  	}
   	  }
	  network.pass_reponse_to_function(address, library_file_deleted, 'json');
   },
   
   do_share_library_file: function(user_id, title) {
	   	  var address = "/services/library/share/"+ library.request_share_user_id + "/" + library.request_share_title;
	   	  function library_file_shared(data) {
	   	  	if (data.success) {
	   	  		var message = data.data;
	   	  		alert(message);
	   	  	}
	   	  	else {
	   	  		var error = data.data;
	   	  		alert(error);
	   	  	}
	   	  }
		  network.pass_reponse_to_function(address, library_file_shared, 'json');
	   },
   
   delete_library_file: function(user_id, title) {
   		library.request_delete_user_id = user_id;
   		library.request_delete_title = title;
   		var library_delete_message_node = dojo.byId('library_delete_message');
   		var message = "This will delete your library file titled <b>" + title + "</b>.\n" +
			          "Click OK to continue or click on the 'x' to cancel.";
		library_delete_message_node.innerHTML = message;
		var confirm_delete_dialog = dijit.byId('confirm_library_delete_dialog');	
		confirm_delete_dialog.show();
   },
   
   share_library_file: function(user_id, title) {
   		library.request_share_user_id = user_id;
   		library.request_share_title = title;
   		var library_share_message_node = dojo.byId('library_share_message');
   		var message = "This will share your library file titled <b>" + title + "</b>.\n" +
			          "Click OK to continue or click on the 'x' to cancel.";
   		library_share_message_node.innerHTML = message;
		var confirm_share_dialog = dijit.byId('confirm_library_share_dialog');	
		confirm_share_dialog.show();
   },
   
   _download_personal_text: function() {
   	var personal_texts_combo = dijit.byId('library_personal_texts');
   	selected_title = personal_texts_combo.attr('value');
   	function _show_personal_text(data) {
   	  	if (data.success) {
   	  		central_text.set_central_text(data.data);
   	  	}
   	  }
   	if (selected_title) {
   	  var address = "/services/library/download/"+ selected_title;
	  network.pass_reponse_to_function(address, _show_personal_text, 'json');
   	}
   },
   
   select_text: function() {
   	 console.debug('select text');
   	 function _populate_search_page(data) {
   	 	if (data.success) {
   	 		central_text.set_central_html(data.data);
   	 	}
   	 }
   	 var address = "/services/library/search_page/";
   	 
	 network.pass_reponse_to_function(address, _populate_search_page, 'json');
	 
   },	
   
   populate_personal_texts: function(user_id) {
   	  function _populate_personal_texts(data) {
   	  	if (data.success === 0) {
   	  		return;
   	  	}
   	  	var personal_titles = data.data;
   	    var option_items = [];
        for (ix in personal_titles) {
    	  title = personal_titles[ix];
    	  console.debug('add item ' + title);
    	  option_items[ix] = {name: title};
        }
        var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: option_items }
			}
		   );
	
        var personal_texts_combo = dijit.byId('library_personal_texts');
        personal_texts_combo.store = options;
   	  }
   	  
   	  var address = "/services/library/dir/";
	  network.pass_reponse_to_function(address, _populate_personal_texts, 'json');
   }
};




/**
 * @author alynch
 */

dynamic_css =  {

    word_meaning_arabic_font_size: 28,
    
    word_meaning_english_font_size: 14,
    
    root_arabic_font_size: 28,
    
    root_english_font_size: 14
    
};



/**
 * @author alynch
 */

db_navigate = {
	
   current_kalima_id: 0,
   
   init: function() {
   	 var filter_text_node = dojo.byId('db_navigate_filter');
   	 var filter_text_widget = dijit.byId('db_navigate_filter');
   	 dojo.connect(filter_text_node, 'onfocus', new_definition.enter_widget);
   	 dojo.connect(filter_text_widget, "onKeyUp", db_navigate.filter_changed);
   },
   
   filter_changed: function() {
   	 var filter_text_widget = dijit.byId('db_navigate_filter');
   	 var text = filter_text_widget.attr('value');
   	 console.debug('filter changed to ' + text);
   },
	
   delete_word: function() {
   	 var address = "/services/modifyword/deletekalima/" + db_navigate.current_kalima_id;
     network.pass_reponse_to_function(address, db_navigate._word_deleted, 'json');
   },
   
   _word_deleted: function(data) {
        var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
	        var previous_kalima_id = data.data;
	        db_navigate.goto_word_of_kalima_id(previous_kalima_id);
	        message = 'Word set deleted from the database';
        }
        new_definition.show_status(message);
   },
   
   last_word: function() {
   	 var address = "/services/modifyword/getlastkalima";
     network.pass_reponse_to_function(address, db_navigate.goto_last_word, 'json');
   },
   
   goto_last_word: function(data) {
   	 last_word_id = data.data;
   	 console.debug('last id is ' + last_word_id);
   	 if (last_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(last_word_id);
   	 }
   	 else {
   	 	console.debug('no next word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   goto_next_or_previous: function(next_or_previous, callback) {
	 if (db_navigate.current_kalima_id == 'New') {return;}
	 var filter_widget = dijit.byId('db_navigate_filter');
	 var filter_text = filter_widget.attr('value');
   	 var address = "/services/modifyword/" + next_or_previous + "/" + db_navigate.current_kalima_id;
   	 var arg_details = {
   			address: address,
   			func: callback,
   			handle_as_type: 'json'
   	 };
   	 if (filter_text) {
   		arg_details.query_args = {filter: filter_text};
   	 }
     network.pass_reponse_to_function(arg_details);
	   
   },
   
   next_word: function() {
	 db_navigate.goto_next_or_previous("getnextkalima", db_navigate.goto_next_word);  
   },
   
   goto_next_word: function(data) {
   	 next_word_id = data.data;
   	 console.debug('next id is ' + next_word_id);
   	 if (next_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(next_word_id);
   	 }
   	 else {
   	 	console.debug('no next word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   previous_word: function() {
	 db_navigate.goto_next_or_previous("getpreviouskalima", db_navigate.goto_previous_word);    
   },
   
   goto_previous_word: function(data) {
   	 previous_word_id = data.data;
   	 console.debug('previous id is ' + previous_word_id);
   	 if (previous_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(previous_word_id);
   	 }
   	 else {
   	 	console.debug('no previous word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   goto_word: function(word_id) {
   	new_definition.set_state('Update');
   	function _show_word(data) {
   		var combined_root = db_data_form.set_form_data(data);
   		root.get_word_meanings_of_root(combined_root);
   	}
   	var address = "/services/modifyword/getvariationforkalvarid/" + word_id;
      network.pass_reponse_to_function(address, _show_word, 'json');
   },

   goto_word_of_kalima_id: function(word_id) {
   	new_definition.set_state('Update');
   	function _show_word(data) {
   		var combined_root = db_data_form.set_form_data(data);
   		root.get_word_meanings_of_root(combined_root);
   	}
   	var address = "/services/modifyword/getvariation/" + word_id;
      network.pass_reponse_to_function(address, _show_word, 'json');
   },
      
   new_word: function() {
   	  new_definition.set_state('New');
   },
   
   save_word: function() {
   	  new_definition.show_status('Working...');
   	  var query = db_data_form.get_form_query();
   	  console.debug('save query is' + query);
      if (new_definition.state == 'Update') {
	   	  db_navigate.update_word_in_db(query);
      }
      else {
          db_navigate.add_word_to_db(query);	
      }
   },
   
   update_word_in_db: function(query) {
       var address = "/services/modifyword/updatewordset/form";
	   function update_db(data) {
	       return db_navigate.show_update_db_result(data);
	   }
	   network.pass_reponse_to_function(address, update_db, 'json', query);
   },
   
   show_update_db_result: function (data) {
   		var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
        	db_navigate.goto_word_of_kalima_id(db_navigate.current_kalima_id);
	        message = ' Words updated in the database';
  	    }
        new_definition.show_status(message);
   },
   
   add_word_to_db: function(query) {
   	  var address = "/services/modifyword/addwordset/form";
      network.pass_reponse_to_function(address, db_navigate.show_add_to_db_result,
      								 'json', query);
   },
   
   show_add_to_db_result: function (data) {
   		var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
	        var num_added = data.data[0];
	        var new_kalima_id = data.data[1];
	        if (num_added === 0) {
	            message = 'Addition to database failed';
	        }
	        else {
	           db_navigate.goto_word_of_kalima_id(new_kalima_id);
	           message = num_added + ' words added to the database';
	        }
        }
        new_definition.show_status(message);
   }
   
};

/**
 * @author alynch
 */
 
 
function DBDataFormRow(word_type, kalvar_id, text, tense, number, gender) {
	
	this.row_id = DBDataFormRow.prototype.get_next_id();
	
	this.word_type = word_type;
	
	this.kalvar_id = kalvar_id;
    this.text = text;
    this.tense = tense;
    this.number = number;
    this.gender = gender;
    
    this.dom_id = null;
    
}

DBDataFormRow.prototype.next_id = 0;
DBDataFormRow.prototype.next_dom_id = 0;

DBDataFormRow.prototype.get_next_id = function() {
	DBDataFormRow.prototype.next_id += 1;
	return DBDataFormRow.prototype.next_id;
};

DBDataFormRow.prototype.update_dom_id = function() {
	DBDataFormRow.prototype.next_dom_id += 1;
	this.dom_id = DBDataFormRow.prototype.next_dom_id; 
};

DBDataFormRow.prototype.get_delete_button_html = function() {
	return '<button dojoType="dijit.form.Button" baseClass="crudButton" label="Delete"' + 
 	'" iconClass="delete_icon" onclick="db_data_form.delete_variation(' + this.row_id + ')"' +
 	'></button>';
};

DBDataFormRow.prototype.get_tense_html = function() {
	var id1 = 'db_form_var_tense_past_' + this.dom_id;
	var id2 = 'db_form_var_tense_present_' + this.dom_id;
	var name = 'group_tense_' + this.dom_id;
	var id1_checked = '';
	var id2_checked = '';
	if (this.tense === 1) {
		id1_checked = ' checked="checked" ';
	}
	else {
		id2_checked = ' checked="checked" ';	
	}
	
	return '<input dojoType="dijit.form.RadioButton" id="'+ id1 +'" name="'+ name + '"' +
          id1_checked + ' value=1 type="radio" />' +
    '<label for="'+ id1 + '"> Past </label>' +
    '<input dojotype="dijit.form.RadioButton" id="'+id2 + '"  name="'+ name + '"' + 
           id2_checked + 'value=2 type="radio" />' + 
    '<label for="'+id2+'"> Present </label>';
};

DBDataFormRow.prototype.connect_text_to_enter_widget = function() {
	var text_node = dojo.byId('db_form_var_text_' + this.dom_id);
	dojo.connect(text_node, 'onfocus', new_definition.enter_widget);
};

DBDataFormRow.prototype.get_number_html = function() {
	var id1 = 'db_form_var_number_singular_' + this.dom_id;
	var id2 = 'db_form_var_number_dual_' + this.dom_id;
	var id3 = 'db_form_var_number_plural_' + this.dom_id;
	var name = 'group_number_' + this.dom_id;
	var id1_checked = '';
	var id2_checked = '';
	var id3_checked = '';
	if (this.number === 1) {
		id1_checked = ' checked="checked" ';
	}
	else if (this.number === 2){
		id2_checked = ' checked="checked" ';	
	}
	else {
		id3_checked = ' checked="checked" ';
	}
	
	return '<input dojoType="dijit.form.RadioButton" id="'+ id1 +'" name="'+ name + '"' +
          id1_checked + ' value=1 type="radio" />' +
    '<label for="'+ id1 + '"> Si </label>' +
    '<input dojotype="dijit.form.RadioButton" id="'+id2 + '"  name="'+ name + '"' + 
           id2_checked + 'value=2 type="radio" />' + 
           '<label for="'+id2+'"> Du </label>' + 
    '<input dojotype="dijit.form.RadioButton" id="'+id3 + '"  name="'+ name + '"' + 
           id3_checked + 'value=3 type="radio" />' + 
    '<label for="'+id3+'"> Pl </label>';
};

DBDataFormRow.prototype.get_text_html_value = function() {
	var widget = dijit.byId('db_form_var_text_' + this.dom_id);
	return widget.attr('value');
};

DBDataFormRow.prototype.get_number_html_value = function() {
	var widget = dijit.byId('db_form_var_number_singular_' + this.dom_id);
	var val = widget.attr('value');
	console.debug('num radio value for ' + this.dom_id + ' is ' + val);
	if (val) {return 1;}
	else {
	  widget = dijit.byId('db_form_var_number_dual_' + this.dom_id);
	  val = widget.attr('value');
	  if (val) {return 2;}
	  else {return 3;}	
	}
};

DBDataFormRow.prototype.get_tense_html_value = function() {
	var widget = dijit.byId('db_form_var_tense_past_' + this.dom_id);
	var val = widget.attr('value');
	console.debug('radio value for ' + this.dom_id + ' is ' + val);
	if (val) {return 1;}
	else {return 2;}
};

DBDataFormRow.prototype.get_enter_arabic_text_html = function() {
	return '<input dojoType="dijit.form.TextBox"' + 
	'id="db_form_var_text_' + this.dom_id + '" value="' + this.text + '"' + 
 	'></input>';
};

DBDataFormRow.prototype.save_state = function() {
   	if (db_data_form.word_type === 2) {this.tense = this.get_tense_html_value();}
    else {this.tense = 0;}
    if (db_data_form.word_type === 1) {this.number = this.get_number_html_value();}
    else {this.number = 0;}
    this.text = this.get_text_html_value(); 
};

DBDataFormRow.prototype.get_word = function() {
	
};
	
DBDataFormRow.prototype.get_html = function() {
    this.update_dom_id();
	var row_html = '';
  	row_html += html_maker.td(this.kalvar_id); 
  	row_html += html_maker.td(this.get_enter_arabic_text_html()); 
  	if (this.word_type === 2) {row_html += html_maker.td(this.get_tense_html());} 
  	if (this.word_type === 1) {row_html += html_maker.td(this.get_number_html());} 
  	//if (this.word_type === 1) {row_html += html_maker.td(this.gender);}
  	row_html += html_maker.td(this.get_delete_button_html());
  	row_html = html_maker.tr(row_html);
  	return row_html;
};

DBDataFormRow.prototype.get_form_query = function(row_ix) {
	this.save_state();
	var query = '&kalvar_id_' + row_ix + '=' + this.kalvar_id;
	query += '&tense_' + row_ix + '=' + this.tense;
	query += '&number_' + row_ix + '=' + this.number;
	query += '&text_' + row_ix + '=' + encodeURIComponent(this.text);
	return query;
};
	


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

my_reader = {
	
 init: function() {
 	login_.register_authentication_change_callback(my_reader.update_state);
 },
 
 update_state: function() {
 	if (login_.authenticated) {
 		my_reader.show_status('');
 		my_reader.populate();
 	}
 	else {
 		my_reader.show_status('Please log on to use the My Reader functionality.');
 	}
 },
 
 populate: function() {
 	var address = "/services/session/session_info";
    var response = network.pass_reponse_to_function(address,
    									 my_reader.populate_session_details, 'json');
 },	
 
 populate_session_details: function(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
			my_reader._populate_widgets('', read_cookie('nickname'), '');
        }
        else {
        	var email_address = data.data[0];
        	var nickname = data.data[1];
        	var num_words_added = data.data[2];
        	my_reader._populate_widgets(email_address, nickname, num_words_added);
        }
 },
 
 _populate_widgets: function(email_address, nickname, num_words_added) {
 	var my_reader_email_address_node = dojo.byId('my_reader_email_address');
	my_reader_email_address_node.innerHTML = email_address;
	var my_reader_nickname_node = dojo.byId('my_reader_nickname');
	my_reader_nickname_node.innerHTML = nickname;
	var my_reader_num_added_node = dojo.byId('my_reader_num_words_added');
	my_reader_num_added_node.innerHTML = '' + num_words_added;
 },
	
 show_deregister: function() {
	var deregister_pane_widget = dijit.byId('deregister_pane');
	deregister_pane_widget.show();
 },
 
 cancel_deregister: function() {
		var deregister_pane_widget = dijit.byId('deregister_pane');
		deregister_pane_widget.hide();
 },
 
 deregister: function(dialog_fields) {
     my_reader.show_status('Working...');
     
     var password_hash = hex_md5(dialog_fields.password);
   	 
   	 var address = "/services/session/deregister/" + password_hash;
   	 function _after_deregister(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            my_reader.show_status(error);
        }
        else {
        	my_reader.show_status('You have been successfully deregistered.');
        }
     }
     var response = network.pass_reponse_to_function(address, _after_deregister, 'json');
 },

 show_change_password: function() {
	var change_password_pane_widget = dijit.byId('change_password_pane');
	change_password_pane_widget.show();
 },
 
 cancel_change_password: function() {
		var change_password_pane_widget = dijit.byId('change_password_pane');
		change_password_pane_widget.hide();
 },
 
 submit_change_password: function(old_password, new_password) {
   	 my_reader.show_status('Working...');
   	 
   	 var old_password_hash = hex_md5(old_password);
   	 var new_password_hash = hex_md5(new_password);
   	 
   	 var address = "/services/session/change_password/" + old_password_hash + "/" + new_password_hash;
   	 function _after_change_password(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            my_reader.show_status(error);
        }
        else {
        	my_reader.show_status('Your password has been changed successfully');
        }
        
     }
     var response = network.pass_reponse_to_function(address, _after_change_password, 'json');
   },
   
   show_status: function(status_) {
   	 var my_reader_status_node = dojo.byId('my_reader_status');
   	 my_reader_status_node.innerHTML = status_;
   },
 
   change_password: function(dialog_fields) {
 	 if (dialog_fields.change_password_new != dialog_fields.change_password_new_confirm) {
       alert("Confirmation password is different.  Password is unchanged.");
       return;
     }
    my_reader.submit_change_password(dialog_fields.change_password_old,
    			dialog_fields.change_password_new);
   }
	
};

/**
 * @author alynch
 */
 
 
 function Variation(word_type, kalvar_id, text, number, tense) {
 	this.word_type = word_type;
 	this.kalvar_id = kalvar_id;
 	this.text = text;
 	this.number = number;
 	this.tense = tense;
 }
 
Variation.prototype.next_image_dom_id = 0;
 
Variation.prototype.get_html = function() {
  var image_html = this._get_word_sarf_image_html();
  return '<div class="root_word" style="font-size: 20px">' + this.text + image_html + '</div>';
};

Variation.prototype._get_word_sarf_image_html = function() {
       var number_image = null;
       var image_url_extender = '';
       if (dojo.isIE && dojo.isIE < 7) {
    	   image_url_extender = '_ie6';
       }
       var tooltip = '';
       if (this.word_type === 1) {
	       number_image = 'miim' + image_url_extender;
	       tooltip = 'مفرد';
	       if (this.number == 3) {
	       	number_image = 'jiim' + image_url_extender;
	       	tooltip = 'جمع';
	       }
       }
	   else if (this.word_type === 2) {
	   	   number_image = 'daad' + image_url_extender;
	   	tooltip = 'ماض';
	       if (this.tense == 2) {
	       	number_image = 'ayn' + image_url_extender;
	       	tooltip = 'مضارع';
	       }
	   }
	   else if (this.word_type === 3) {
	   	   number_image = 'haa' + image_url_extender;
	   	   tooltip = 'حرف';
	       }
	   else {
	   	  throw('invalid word type: ' + this.word_type);
	   }
       var css_id = 'sarf_image_' + Variation.prototype.next_image_dom_id;
       Variation.prototype.next_image_dom_id += 1;
       var html = '<img class="sarf_icon" width=16 height=16 id="' + css_id + '" ' +
   									'src="images/' + number_image +	'.png" />';	
       if ( ! (dojo.isIE && dojo.isIE < 8)) {
    	   html += '<span dojoType="dijit.Tooltip" connectId="' + css_id + '">' +
    	   															tooltip + '</span>';
       }
   	   return html;
};
 
 
function WordSet() {
	this.kalima_id = null;
	this.meaning = null;
	this.root = null;
    this.word_type = null;
    this.variations = {};
}

WordSet.prototype.next_image_dom_id = 0;

WordSet.prototype.populate_from_ajax_data = function(data) {
	this.kalima_id = data[0];
	this.word_type = data[1];
    this.meaning = data[2]; 
    this.root = data[3];
    var variations_data = data[4]; 
    for (ix in variations_data) {
	  var variation_data = variations_data[ix];
	  var kalvar_id = variation_data[0];
	  var text = variation_data[1];
	  var number = variation_data[2];
      var tense = variation_data[3];
      var variation = new Variation(this.word_type, kalvar_id, text, number, tense);
      this.variations[kalvar_id] = variation;
    }
};

WordSet.prototype._get_variations_html = function() {
	var html = '<div class="variation_texts">';
	for (ix in this.variations) {
	  var variation = this.variations[ix];
	  html += variation.get_html();
	}
	html += '</div>';
	return html;
};

WordSet.prototype.get_html = function(buttons) {
	if (! buttons) {
		buttons = ['db_button', 'v_button'];
	}
	var html = '<div class="root_section clear_fix" >';
	html += this._get_variations_html();
	var toolbar_html = this._get_buttons_html(buttons);
	
	html += '<div class="root_meaning" style="font-size: 14px">' + html_maker.div(this.meaning) +
									toolbar_html + '</div>';
	html += '</div>';
	return html;
};

WordSet.prototype._get_buttons_html = function(buttons) {
	var html = '';
	for (ix in buttons) {
		var button = buttons[ix];
		if (button == 'v_button') {
			var toolbar_v = this._get_toolbar_image('v_button',
					 'vocab.add_word_set(' + this.kalima_id + ')',
					 'Add to My Vocabulary');
			html += html_maker.div(toolbar_v);
		}
		if (button == 'db_button') {
			var toolbar_db = this._get_toolbar_image('db_button',
					 'root.goto_db(' + this.kalima_id + ')',
					 'View Database Details for Word');
			html += html_maker.div(toolbar_db);
		}
		if (button == 'remove_button') {
			var toolbar_remove = this._get_toolbar_image('crystal_clear_action_button_cancel',
					 'vocab.remove_word_set(' + this.kalima_id + ')',
					 'Remove From My Vocabulary');
			html += html_maker.div(toolbar_remove);
		}
	}
	return html;
};

WordSet.prototype._get_toolbar_image = function(image_name, link, tooltip_text) {
	var dom_id = WordSet.prototype.next_image_dom_id;
	WordSet.prototype.next_image_dom_id += 1;
	var css_id = 'word_set_image_' + dom_id;
	var html = '<img class="sarf_icon toolbar_button clear_fix" width=32 height=32 ' + 
		'id="' + css_id + '" ' + ' onclick="' + link + '"' + ' src="images/' + image_name +	'.png" />';
	html += '<span dojoType="dijit.Tooltip" connectId="' + css_id + '">' + tooltip_text + '</span>'

	return html;
};
   



function doGetCaretPosition (ctrl) {

	var CaretPos = 0;
	// IE Support
	if (document.selection) {

		ctrl.focus ();
		var Sel = document.selection.createRange ();

		Sel.moveStart ('character', -ctrl.value.length);

		CaretPos = Sel.text.length;
	}
	// Firefox support
	else if (ctrl.selectionStart || ctrl.selectionStart == '0')
	   CaretPos = ctrl.selectionStart;

	return (CaretPos);

}


function setCaretPosition(ctrl, pos)
{

	if(ctrl.setSelectionRange)
	{
		ctrl.focus();
		ctrl.setSelectionRange(pos,pos);
	}
	else if (ctrl.createTextRange) {
		var range = ctrl.createTextRange();
		range.collapse(true);
		range.moveEnd('character', pos);
		range.moveStart('character', pos);
		range.select();
	}
}



/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.1 Copyright (C) Paul Johnston 1999 - 2002.
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 */

/*
 * Configurable variables. You may need to tweak these to be compatible with
 * the server-side, but the defaults work in most cases.
 */
var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
var chrsz   = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */

/*
 * These are the functions you'll usually want to call
 * They take string arguments and return either hex or base-64 encoded strings
 */
function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
function b64_md5(s){ return binl2b64(core_md5(str2binl(s), s.length * chrsz));}
function str_md5(s){ return binl2str(core_md5(str2binl(s), s.length * chrsz));}
function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
function str_hmac_md5(key, data) { return binl2str(core_hmac_md5(key, data)); }

/*
 * Perform a simple self-test to see if the VM is working
 */
function md5_vm_test()
{
  return hex_md5("abc") == "900150983cd24fb0d6963f7d28e17f72";
}

/*
 * Calculate the MD5 of an array of little-endian words, and a bit length
 */
function core_md5(x, len)
{
  /* append padding */
  x[len >> 5] |= 0x80 << ((len) % 32);
  x[(((len + 64) >>> 9) << 4) + 14] = len;

  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;

  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;

    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);

    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);

    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);

    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);

    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
  }
  return Array(a, b, c, d);

}

/*
 * These functions implement the four basic operations the algorithm uses.
 */
function md5_cmn(q, a, b, x, s, t)
{
  return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
}
function md5_ff(a, b, c, d, x, s, t)
{
  return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t)
{
  return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t)
{
  return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t)
{
  return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Calculate the HMAC-MD5, of a key and some data
 */
function core_hmac_md5(key, data)
{
  var bkey = str2binl(key);
  if(bkey.length > 16) bkey = core_md5(bkey, key.length * chrsz);

  var ipad = Array(16), opad = Array(16);
  for(var i = 0; i < 16; i++)
  {
    ipad[i] = bkey[i] ^ 0x36363636;
    opad[i] = bkey[i] ^ 0x5C5C5C5C;
  }

  var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
  return core_md5(opad.concat(hash), 512 + 128);
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left.
 */
function bit_rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * Convert a string to an array of little-endian words
 * If chrsz is ASCII, characters >255 have their hi-byte silently ignored.
 */
function str2binl(str)
{
  var bin = Array();
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < str.length * chrsz; i += chrsz)
    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
  return bin;
}

/*
 * Convert an array of little-endian words to a string
 */
function binl2str(bin)
{
  var str = "";
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < bin.length * 32; i += chrsz)
    str += String.fromCharCode((bin[i>>5] >>> (i % 32)) & mask);
  return str;
}

/*
 * Convert an array of little-endian words to a hex string.
 */
function binl2hex(binarray)
{
  var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i++)
  {
    str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
           hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
  }
  return str;
}

/*
 * Convert an array of little-endian words to a base-64 string
 */
function binl2b64(binarray)
{
  var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i += 3)
  {
    var triplet = (((binarray[i   >> 2] >> 8 * ( i   %4)) & 0xFF) << 16)
                | (((binarray[i+1 >> 2] >> 8 * ((i+1)%4)) & 0xFF) << 8 )
                |  ((binarray[i+2 >> 2] >> 8 * ((i+2)%4)) & 0xFF);
    for(var j = 0; j < 4; j++)
    {
      if(i * 8 + j * 6 > binarray.length * 32) str += b64pad;
      else str += tab.charAt((triplet >> 6*(3-j)) & 0x3F);
    }
  }
  return str;
}


/**
*
*  AJAX IFRAME METHOD (AIM)
*  http://www.webtoolkit.info/
*
**/

AIM = {

	frame : function(c) {

		var n = 'f' + Math.floor(Math.random() * 99999);
		var d = document.createElement('DIV');
		d.innerHTML = '<iframe style="display:none" src="about:blank" id="'+n+'" name="'+n+'" onload="AIM.loaded(\''+n+'\')"></iframe>';
		document.body.appendChild(d);

		var i = document.getElementById(n);
		if (c && typeof(c.onComplete) == 'function') {
			i.onComplete = c.onComplete;
		}

		return n;
	},

	form : function(f, name) {
		f.setAttribute('target', name);
	},

	submit : function(f, c) {
		AIM.form(f, AIM.frame(c));
		if (c && typeof(c.onStart) == 'function') {
			return c.onStart();
		} else {
			return true;
		}
	},

	loaded : function(id) {
		var i = document.getElementById(id);
		if (i.contentDocument) {
			var d = i.contentDocument;
		} else if (i.contentWindow) {
			var d = i.contentWindow.document;
		} else {
			var d = window.frames[id].document;
		}
		if (d.location.href == "about:blank") {
			return;
		}

		if (typeof(i.onComplete) == 'function') {
			i.onComplete(d.body.innerHTML);
		}
	}

};

/**
 * Translator Copyright (c) 2008 Ariel Flesler - aflesler(at)gmail(dot)com |
 * http://flesler.blogspot.com Licensed under BSD
 * (http://www.opensource.org/licenses/bsd-license.php) Date: 5/26/2008
 * 
 * @projectDescription JS Class to translate text nodes.
 * @author Ariel Flesler
 * @version 1.0.1
 */

/**
 * The constructor must receive the parsing function, which will get the text as
 * parameter To use it, call the method .traverse() on the starting (root) node.
 * If the parsing is asynchronous (f.e AJAX), set sync to false on the instance.
 * When doing so, the parser function receives an extra argument, which is a
 * function that must be called passing it the parsed text.
 */

function Translator(parser, filter) {
	this.parse = parser; // function that parses the original string
	this.filter = filter; // optional filtering function that receives the
	// node, and returns true/false
}

Translator.prototype = {
	translate : function(old) { // translates a text node
		if (this.sync) {
			this.replace(old, this.parse(old.nodeValue, old));
		}
		else {
			var self = this;
			this.parse(old.nodeValue, function(text) {
				self.replace(old, text);
			});
		}
	},
	makeNode : function(data) {
		if (data && data.split) {// replacing for a string
			data = document.createTextNode(data);
		}
	return data;
	},
	replace : function(old, text) { // Replaces a text node with a new (string) text or another node
		if (text != null && text != old.nodeValue) {
			var parent = old.parentNode;
			if (text.splice) { // Array
				for ( var i = 0, l = text.length - 1; i < l;) {
					var new_node = this.makeNode(text[i++]);
					parent.insertBefore(new_node, old);
				}
				text = this.makeNode(text[l] || ''); // Last
			} else {
				text = this.makeNode(text);
			}
			parent.replaceChild(text, old);
		}
	},
	valid : /\S/, // Used to skip empty text nodes (modify at your own risk)
	sync : true, // If the parsing requires a callback, set to false
	traverse : function(root) { // Goes (recursively) thru the text nodes of the root, translating
		var children = root.childNodes, l = children.length, node;
		while (l--) {
			node = children[l];
			if (node.nodeType == 3) { // Text node
				if (this.valid.test(node.nodeValue)) {// Skip empty text nodes
					this.translate(node);
				} 
			} else if (node.nodeType == 1 && (!this.filter || this.filter(node))) {
				// Element node
				this.traverse(node);
			}	
		}
	}
};


function Hash()
{
	this.length = 0;
	this.items = new Array();
	for (var i = 0; i < arguments.length; i += 2) {
		if (typeof(arguments[i + 1]) != 'undefined') {
			this.items[arguments[i]] = arguments[i + 1];
			this.length++;
		}
	}
   
	this.removeItem = function(in_key)
	{
		var tmp_previous;
		if (typeof(this.items[in_key]) != 'undefined') {
			this.length--;
			var tmp_previous = this.items[in_key];
			delete this.items[in_key];
		}
	   
		return tmp_previous;
	};

	this.getItem = function(in_key) {
		return this.items[in_key];
	};

	this.setItem = function(in_key, in_value)
	{
		var tmp_previous;
		if (typeof(in_value) != 'undefined') {
			if (typeof(this.items[in_key]) == 'undefined') {
				this.length++;
			}
			else {
				tmp_previous = this.items[in_key];
			}

			this.items[in_key] = in_value;
			console.debug('teism are ' + this.items);
		}
	   
		return tmp_previous;
	};

	this.hasItem = function(in_key)
	{
		return typeof(this.items[in_key]) != 'undefined';
	};

	this.clear = function()
	{
		for (var i in this.items) {
			delete this.items[i];
		}

		this.length = 0;
	};
}

/* from http://www.faqts.com/knowledge_base/view.phtml/aid/30209/fid/144 */
remove_array_duplicates = function(array_, customCompare ){
  if ( customCompare ){
      array_.sort(customCompare);
      for (var i=0; i<(array_.length-1); i++)
      {
         if ( !customCompare(array_[i],array_[i+1]) ){
            array_.splice( (i--)+1, 1 );
         }
      }
  } else {
      array_.sort();
      for (var i=0; i<(array_.length-1); i++)
      {
         if (array_[i]==array_[i+1]){
            array_.splice( (i--)+1, 1 );
         }
      }
   }
  return array_;
};





status_ = {
		
  RUNNING: "Running",
  COMPLETED: "Completed",
  FAILED: "Failed",
  
  _styles: {"Running": "status_running",
			"Completed": "status_completed",
			"Failed": "status_failed" },
		
  _current_events: [],
	
  track_event: function (title, dfd) {
	  console.debug('track ' + title);
	  var status_event = new StatusEvent(title, dfd);
	  status_._current_events.push(status_event);
	  dfd.addCallback(function(result) 
			  		  {status_._event_completed(status_event, result); return result;}
	  				  );
	  dfd.addErrback(function(result) 
	  		  {status_._event_failed(status_event, result); return result;}
				  );
	  status_._update_html();
  },
  
  show_error: function (ix) {
	  status_event = status_._current_events[ix];
	  var status_error_name_node = dojo.byId('status_error_name');
	  var status_error_name_message_node = dojo.byId('status_error_message');
	  var show_error_pane_widget = dijit.byId('status_error_pane');
	  status_error_name_node.innerHTML = status_event.result.name;
	  status_error_name_message_node.innerHTML = status_event.result.message;
	  show_error_pane_widget.show();
  },
  
  error_pane_closed: function() {
  },
  
  _event_completed: function (status_event, result) {
	  status_event.state = status_.COMPLETED;
	  status_._update_html();
	  setTimeout(function () {status_._remove_event(status_event);}, 5000);
  },
  
  _event_failed: function (status_event, result) {
	  status_event.state = status_.FAILED;
	  status_event.result = result;
	  status_._update_html();
	  setTimeout(function () {status_._remove_event(status_event);}, 30000);
  },
  
  _remove_event: function (status_event) {
	  var ix = dojo.indexOf(status_._current_events, status_event);
	  delete status_._current_events[ix];
	  status_._update_html();
  },
  
  _get_summary_status_text: function() {
	  var summary_status = '';
	  for (ix in status_._current_events) {
		  status_event = status_._current_events[ix];
		  if (status_event.state === status_.RUNNING) {
			  summary_status = status_event.title + '...';
		  }
	  }
	  return summary_status
  },
  
  _update_html: function() {
	  var html = '';
	  var status_event = null;
	  for (ix in status_._current_events) {
		  status_event = status_._current_events[ix];
		  if (status_event) {
			  html += status_event.get_html();
		  }
	  }
	  var status_node = dojo.byId('status_events');
	  status_node.innerHTML = html;
	  
	  var summary_status_node = dojo.byId('menu_status');
	  if (! summary_status_node) return;
	  summary_status_node.innerHTML = status_._get_summary_status_text();
  }
};

function StatusEvent(title, dfd) {
	this.title = title;
	this.dfd = dfd;
	this.state = status_.RUNNING;
	this.result = null;
}

StatusEvent.prototype.get_html = function() {
	  var title = this.title + '...';
	  var class_ = status_._styles[this.state];
	  var click_handler = '';
	  if (this.state == status_.FAILED) {
		  var ix = dojo.indexOf(status_._current_events, this);
		  click_handler = 'onclick="status_.show_error(' + ix + ')"';
		  title += ' (Click for details)';
	  }
	  return '<div class="' + class_ + '" '+ click_handler + '>' + title  + '</div>';
	};
	
	

/**
 * @author alynch
 */
 
revise = {
		
	test_lines: [],
	
    init: function() {
		login_.register_authentication_change_callback(revise.update_state);
		dojo.connect(window, "onresize", revise.resize);
		revise.resize();
    },
   
    update_state: function() {
    },
    
    _get_sequenced_test_lines: function() {
    	var line_ix = 0;
    	for (word_set_ix in vocab.word_sets) {
    		var word_set = vocab.word_sets[word_set_ix];
    		if (word_set) {
    			var test_line = new TestLine(word_set, line_ix);
    			revise.test_lines[line_ix] = test_line;
    			line_ix += 1;
    		}
        }
    },
    
    start_revise: function() {
    	revise._get_sequenced_test_lines();
    	revise._populate_test();
    },
    
    show: function(line_ix) {
    	console.debug('show line id ' + line_ix);
    	var test_line = revise.test_lines[line_ix];
    	test_line.after_show_clicked();
    },
    
    correct: function(line_ix) {
    	console.debug('correct line id ' + line_ix);
    	var test_line = revise.test_lines[line_ix];
    	test_line.after_correct_clicked();
    	var next_test_line = revise.test_lines[line_ix + 1];
    	next_test_line.wait_for_show();
    },
    
    wrong: function(line_ix) {
    	console.debug('wrong line id ' + line_ix);
    	var test_line = revise.test_lines[line_ix];
    	test_line.after_wrong_clicked();
    	var next_test_line = revise.test_lines[line_ix + 1];
    	next_test_line.wait_for_show();
    },
    
    begin_test: function() {
    	for (test_line_ix in revise.test_lines) {
    		revise.test_lines[test_line_ix].hide_for_test();
    	}
//    	then show the first 'Show' button
    	revise.test_lines[0].wait_for_show();
    },
    
    _populate_test: function() {
    	console.debug('populate test');
    	var html = revise._get_test_lines_html(revise.test_lines);
    	var revision_word_list_node = dojo.byId("revision_word_list");
    	revision_word_list_node.innerHTML = html; 
    	dojo.parser.parse(revision_word_list_node);
    	for (test_line_ix in revise.test_lines) {
    		revise.test_lines[test_line_ix].show_for_revise();
    	}
    },
    
    _get_test_lines_html: function(test_lines) {
    	var html = '<table class="revise_table">';
    	for (test_line_ix in revise.test_lines) {
    		html += test_lines[test_line_ix].get_table_row_html();
    	}
    	html += '</table>';
    	return html;
    },
    
    resize: function() {
    	console.debug('rv org'); 
    	var organise_vocab_node = dojo.byId('revise_organise');
    	console.debug('node is ' + organise_vocab_node); 
    	var parent_height = dojo.byId('navigate_pane').clientHeight;
    	console.debug('height is ' + parent_height);
    	var new_height = (parent_height - 40) + 'px';
    	console.debug('set height to ' + new_height);
    	organise_vocab_node.style.height = new_height;
    	var revise_download_node = dojo.byId('revise_download');
    	revise_download_node.style.height = new_height;
    	var revise_test_node = dojo.byId('revise_test');
    	revise_test_node.style.height = new_height;
    },
    
    download_pdf: function() {
	   console.debug('download pdf');
    }
    
};

function TestLine(word_set, line_ix) {
 	this.word_set = word_set;
 	this.line_ix = line_ix;
 	this.dom_id = TestLine.prototype.next_dom_id;
 	TestLine.prototype.next_dom_id += 1;
 }

TestLine.prototype.next_dom_id = 0;

TestLine.prototype.after_show_clicked = function() {
	//	show the meaning and also the tick/cross buttons
	console.debug('after_show_clicked');
	this._set_button_visible("show", false);
	this._set_button_visible("correct", true);
	this._set_button_visible("wrong", true);
	this._set_meaning_visible(true);
};

TestLine.prototype.wait_for_show = function() {
	//	show the meaning and also the tick/cross buttons
	console.debug('wait_for_show');
	this._set_button_visible("show", true);
	this._set_button_visible("correct", false);
	this._set_button_visible("wrong", false);
	this._set_meaning_visible(false);
};

TestLine.prototype.show_for_revise = function() {
	//	show the test line for the user to revise
	console.debug('show for revise');
	this._set_button_visible("show", false);
	this._set_button_visible("correct", false);
	this._set_button_visible("wrong", false);
	this._set_meaning_visible(true);
};

TestLine.prototype.hide_for_test = function() {
	console.debug('hide_for_test');
	this._set_button_visible("show", false);
	this._set_button_visible("correct", false);
	this._set_button_visible("wrong", false);
	this._set_meaning_visible(false);
};

TestLine.prototype.after_correct_clicked = function() {
	console.debug('after_correct_clicked');
	this._set_button_visible("show", false);
	this._set_button_visible("correct", false);
	this._set_button_visible("wrong", false);
	this._set_meaning_visible(true);
};

TestLine.prototype.after_wrong_clicked = function() {
	console.debug('after_wrong_clicked');
	this._set_button_visible("show", false);
	this._set_button_visible("correct", false);
	this._set_button_visible("wrong", false);
	this._set_meaning_visible(true);
};

TestLine.prototype._set_button_visible = function(button_name, visible) {
	var display = null;
	if (visible) display = "inline";
	else display = "none";
	var full_css_id = "widget_revise_word_" + button_name + "_" + this.dom_id;
	dom_node = dijit.byId(full_css_id).domNode
	dom_node.style.display = display;
};

TestLine.prototype._set_meaning_visible = function(visible) {
	var meaning_node = dojo.byId('revise_word_meaning_' + this.dom_id);
	var display = null;
	if (visible) display = "block";
	else display = "none";
	meaning_node.style.display = display;
};
 
TestLine.prototype.get_table_row_html = function() {
	var html = '<tr><td>';
	for (variation_ix in this.word_set.variations) {
		variation = this.word_set.variations[variation_ix];
		if (html) html += ' ';
		html += "<div id='revise_word_text_" + this.dom_id + "' class='revise_word_text'>" + variation.text + "</div>";
	}
	html += "</td>";
	html += "<td>";
	html += "<div id='revise_word_meaning_" + this.dom_id + "' class='revise_word_meaning'>" + this.word_set.meaning + "</div>";
	html += "</td>";
	html += "<td>";
	html += "<button  id='widget_revise_word_show_" + this.dom_id + "' dojoType='dijit.form.Button' onclick='revise.show(" + this.line_ix + ")' label='Show Answer'></button>";
	html += "<button  id='widget_revise_word_correct_" + this.dom_id + "' dojoType='dijit.form.Button' onclick='revise.correct(" + this.line_ix + ")' label='Correct' iconClass='correct_icon'></button>";
	html += "<button  id='widget_revise_word_wrong_" + this.dom_id + "' dojoType='dijit.form.Button' onclick='revise.wrong(" + this.line_ix + ")' label='Wrong' iconClass='wrong_icon'></button>";
	html += "</td>";
	html += "</tr>";
	return html;
};




/**
 * @author alynch
 */
 
organise_vocab = {
		
	_populated: false,
		
	populate: function() {
		if (! organise_vocab._populated) {
			var html = '<table>';
			if (! vocab.word_sets) {
				return;
			}
			console.debug('ov wordsets ' + vocab.word_sets);
			var column = 0;
			for (ix in vocab.word_sets) {
				if (column == 0) {
				html += '<tr>';
				}
				html += '<td class="organise_vocab_cell">';
				word_set = vocab.word_sets[ix];
				html += rounded.wrap_in_round_corners(
								word_set.get_html(['remove_button']),
								'.', 'black');
				html += '</td>';
				if (column == 2) {
					html += '</tr>';
					column = 0;
				}
				else {
					column += 1;
				}
			}
			html += '</table>';
			var organise_vocab_wordsets_node = dojo.byId('organise_vocab_wordsets');
			organise_vocab_wordsets_node.innerHTML = html;
			dojo.parser.parse(organise_vocab_wordsets_node);
//			organise_vocab._populated = true;
		}
	}
};


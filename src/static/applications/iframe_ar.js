/**
 * @author alynch
 * 
 */

// ' onmouseover="if_ar.mouse_over_central_word('+ ix + ')"' +\
// ' onmouseout="if_ar.mouse_out_central_word('+ ix + ')">' + \

function debug_out(message) {
	try {
		if (console.debug) {
			console.debug(message);
		}
	}
	catch (e) {
	}
}

text_finder = {
		
	ix: 1,
	
//	proxy_site_url: 'localhost:8080',
	proxy_site_url: 'www.arabicreader.net',
	
	document_url: '',
	
	site_url: '',
	
	strip_to_arabic: function(text) {
	    if (! text) {return text;}
		var new_text = '';
		for ( var i = 0; i < text.length; i++) {
			var char_code = text.charCodeAt(i);
			if (char_code >= 0x600 && char_code <= 0x700) {
				if (char_code != 0x61f && char_code != 0x60c && char_code != 0x61B && char_code != 0x66c) {
					new_text += text.charAt(i); 
				}
			}
		}
		return new_text;
	},
	
	is_arabic_word: function(text) {
		var char_0 = text.charCodeAt(0);
		if (char_0 < 0x600 || char_0 > 0x700) {
			return false;
		}
		return true;
	},
	
	get_site_url_from_document_url: function(document_url) {
		var first_slash_ix = document_url.indexOf('/');
		if (first_slash_ix == -1) {
			return document_url;
		}
		var doc_site_url = document_url.slice(0, first_slash_ix);
		return doc_site_url;
	},
	
	redirect_link_to_proxy: function(address) {
		/**
		 * relative links get text_finder.get_url_address prepended to relative
		 * addresses by the browser, so remove that first
		 */
//		debug_out('address prefix is ' + address.slice(0, text_finder.get_url_address.length));
		if (address.slice(0, text_finder.get_url_address.length) == text_finder.get_url_address) {
			address = address.slice(text_finder.get_url_address.length);
		}
		var doc_site_url = text_finder.site_url;
		var base_url = '';
		if (address.slice(0, 1) == '/') {
			base_url = address;
		}
		else if (address.slice(0, 7) == 'http://') {
			doc_site_url = text_finder.get_site_url_from_document_url(address.slice(7));
			if (doc_site_url == text_finder.proxy_site_url) {
				base_url = address.slice(7 + doc_site_url.length);
				doc_site_url = text_finder.site_url;
			}
			else {
				base_url = address.slice(7 + doc_site_url.length);
			}
		}
		else {
			base_url = text_finder.document_directory + '/' + address;
		}
		var url = doc_site_url + base_url;
		var new_address = 'http://' + text_finder.proxy_site_url + '/services/proxy/geturl/' + url;
//		debug_out('link redirected from ' + address + ' to ' + new_address);
		return new_address;
	},
	
	redirect_link_to_original_site: function(address) {
		debug_out('redirect link to original for ' + address);
		debug_out('address prefix is ' + address.slice(0, text_finder.get_url_address.length));
		if (address.slice(0, text_finder.get_url_address.length) == text_finder.get_url_address) {
			address = address.slice(text_finder.get_url_address.length);
		}
		if (address.slice(0, text_finder.site_url.length) == text_finder.site_url) {
			address = address.slice(text_finder.site_url.length);
		}
		debug_out('cut down address is ' + address);
		var new_address = '';
		// redirect the link to the original URL
		if (address.slice(0, 1) == '/') {
			new_address = text_finder.site_url + address;
		}
		else {
			if (address.slice(0, 7) == 'http://') {
				var doc_site_url = text_finder.get_site_url_from_document_url(address.slice(7));
//				debug_out('link site is ' + site_url);
				if (doc_site_url != text_finder.proxy_site_url) {
					return address;
				}
				new_address = address.slice(text_finder.proxy_site_url.length + 7);
//				debug_out('a1 ' + new_address);
				new_address = 'http://' + text_finder.site_url + new_address;
//				debug_out('new address is ' + new_address);
			}
			else {
				new_address = text_finder.document_url + '/' + address;
			}
		}
		return new_address;
	},
	
	get_document_dir_from_document_url: function(document_url) {
		var path = document_url.slice(text_finder.site_url.length);
		var last_slash_index = path.lastIndexOf('/');
		if (last_slash_index == -1) {
			return path;
		}
		var dir = path.slice(0, last_slash_index);
		return dir;
	},

	traverse : function(document_url, node) {
		debug_out('traverse1 ' + document_url + ' ' + node);
		text_finder.get_url_address = 'http://' + text_finder.proxy_site_url + '/services/proxy/geturl/';
		text_finder.document_url = document_url.slice(text_finder.get_url_address.length);
		text_finder.site_url = text_finder.get_site_url_from_document_url(text_finder.document_url);
		text_finder.document_directory = text_finder.get_document_dir_from_document_url(text_finder.document_url);
		debug_out('document dir is ' + text_finder.document_directory);
		debug_out('site url is ' + text_finder.site_url + ' from ' + text_finder.document_url);
		debug_out('traverse ' + text_finder.document_url + ' ' + node);
		function func(text) {
			// good trim implementation
			text = text.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
			text = text.replace('\n', '');
			var data = [];
			var words = text.split(/\s+/);
			for ( var i = 0; i < words.length; i++) {
				var word = words[i];
				if (! word) {continue;}
				if (! text_finder.is_arabic_word(word)) {
					data[i] = word;
					continue;
				}
				word = text_finder.strip_to_arabic(word);
				text_finder.ix += 1;
				var span_node = document.createElement('div');
				span_node.style.display = 'inline';
				span_node.id = "central_word_"+ text_finder.ix;
				var s = "if_ar.central_word_clicked('" + word + "');";
				var f = new Function(s);
				span_node.onclick = f;
				var t = "if_ar.mouse_over_central_word(" + text_finder.ix + ")";
				var g = new Function(t);
				span_node.onmouseover = g;
				var u = "if_ar.mouse_out_central_word(" + text_finder.ix + ")";
				var h = new Function(u);
				span_node.onmouseout = h;
				text_node = document.createTextNode(words[i] + ' ');
				span_node.appendChild(text_node);
				data[i] = span_node;
			}
			return data;
		}
		function filter(node) {
			if (node.tagName.toUpperCase() == 'SCRIPT') {
				return false;
			}
			return true;
		}
		function translate_link(tag, node) {
//			debug_out('translate link ' + node.href);
			if (tag == 'IMG') {
				if (node.src.indexOf('geturl') == -1 || true) {
					var url = text_finder.redirect_link_to_original_site(node.src);
					node.src = url;
				}
			}
			else if (tag == 'A') {
				if (node.href != 'javascript:;' && (node.href.indexOf('mailto:') == -1)) {
					var url = text_finder.redirect_link_to_proxy(node.href);
					node.href = url;
				}
			}
		}
		text_finder.ix = 1;
		spanise = new Translator(func, filter, translate_link);
		spanise.traverse(node);
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

function Translator(parser, filter, translate_link) {
	this.parse = parser; // function that parses the original string
	this.filter = filter; // optional filtering function that receives the
	// node, and returns true/false
	this.translate_link = translate_link;
}

Translator.prototype = {
	translate : function(old) { // translates a text node
		if (this.sync) {
			this.replace(old, this.parse(old.nodeValue));
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
				var tag_name = node.tagName.toUpperCase();
				if (tag_name == 'IMG' || tag_name == 'A') {
					this.translate_link(tag_name, node);
				}
				this.traverse(node);
			}	
		}
	}
};

if_ar = {

	init : function() {
		debug_out('init ar');
		window.parent.central_text.resize_inner_frame();
		// if_ar._set_outer_frame_height();
		// if_ar._show_info_pane();
		text_finder.traverse(document.location.href, document.body);
	},

	_show_info_pane : function() {
		var info_pane_element = document.getElementById('ar_info_pane');
		info_pane_element.innerHTML = 'abdulhaq';
	},

	_set_outer_frame_height : function(outer_frame_node) {
		inner_height = outer_frame_node.contentWindow.document.body.scrollHeight + "px";
		outer_frame_node.style.height = inner_height;
	},

	mouse_over_central_word : function(ix) {
//		debug_out('mouse over');
		var word_element = document.getElementById('central_word_' + ix);
		word_element.className = 'moused_central_word';
	},

	mouse_out_central_word : function(ix) {
//		debug_out('mouse out');
		var word_element = document.getElementById('central_word_' + ix);
		word_element.className = 'normal_central_word';
	},

	central_word_clicked : function(word) {
		debug_out('cwc');
		window.parent.central_text.central_word_clicked(word);
	}

};

function addLoadEvent(func) {
	var oldonload = window.onload;
	debug_out('onLoad is ' + window.onload);
	if (typeof window.onload != 'function') {
		debug_out('replace onload');
		window.onload = func;
	} else {
		window.onload = function() {
			debug_out('onload AR');
			if (oldonload) {
				debug_out('do old onload');
				oldonload();
			}
			debug_out('do new onload');
			func();
		};
	}
}

debug_out('addLoadEvent AR');
addLoadEvent(if_ar.init);

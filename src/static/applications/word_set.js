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
   


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



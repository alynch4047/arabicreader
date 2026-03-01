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
	

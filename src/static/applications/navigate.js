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
  
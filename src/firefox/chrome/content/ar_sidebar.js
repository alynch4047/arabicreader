
var arsb = {
		
	selected_text: '',
		
	set_word: function(text) {
		arsb.selected_text = text;
		var test_lbl =  window.document.getElementById("atest");
		test_lbl.value = text;
		var ar_browser = window.document.getElementById("ar_browser");
		ar_browser.addEventListener("DOMContentLoaded", arsb.pageLoaded, false);
		const nsIWebNavigation = Components.interfaces.nsIWebNavigation;
		ar_browser.webNavigation.loadURI("http://localhost:8080/static/applications/ff_extension.html", 
		          nsIWebNavigation.LOAD_FLAGS_NONE, null, null, null);

	},
	
	pl: function() {
		alert("Loaded page");
	},

	pageLoaded: function(context) {
		var ar_browser = window.document.getElementById("ar_browser");
		var ar_browser_document = ar_browser.contentDocument;
		function sendEventToBrowser(aId, aExtra) {
			//*** aId is id of element
			//*** aExtra is passed as attribute "myextra" of element
			//*** content.document is document of current page
			  var elm = ar_browser_document.getElementById(aId);
			  if (elm && "createEvent" in ar_browser_document) {
			    //*** set myextra atteribute on elm
			    elm.setAttribute("myextra", aExtra);
			    //*** fire myevent on elm
			    var evt = ar_browser_document.createEvent("Events");
			    evt.initEvent("myevent", true, false);
			    elm.dispatchEvent(evt);
			  }
		}
		sendEventToBrowser("my-div-extra", arsb.selected_text);
		var ar_browser_window = ar_browser.contentWindow;
		alert("WJS: " + ar_browser_window.wrappedJSObject.word_meaning.get_meanings_for_word);
	}
		
};
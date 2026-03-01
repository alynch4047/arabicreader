
function myeventListener(event) {
	var elm = event.target;
	var att = elm.getAttribute("onmyevent");
	//*** attribute "myextra" is set in extension code
	var myextra = elm.getAttribute("myextra");
//	alert("AHello from Bme 2 " + att);
	if (elm && att) {
		//*** onmyevent can use above variables because it executed here
		//*** execute (eval) in scope of page's window object
		window.eval(att);
	}
	//*** clean up
	if (elm.hasAttribute("myextra"))
		elm.removeAttribute("myextra");
}
window.addEventListener("myevent", myeventListener, false);

function init_ff_extension() {
	
	html_maker.init();
	  login_.init();

      vocab.init();
      new_definition.init();
      library.init();
      
   	  upload_.init();
   	  main_menu.init();
   	  my_reader.init();
   	  db_navigate.init();
   	  font_manager.init();
   	  revise.init();
      navigate_.init();
	
}
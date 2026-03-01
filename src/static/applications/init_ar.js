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
  
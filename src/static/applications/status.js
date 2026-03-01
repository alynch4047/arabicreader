
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
	
	
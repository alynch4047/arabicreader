

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





test_html_maker = {
	
	start: function() {
		
		html_maker.init();
		
		var html = '';
		row1 = html_maker.tr(html_maker.td('1') + html_maker.td('2'));
		html += html_maker.table(row1);
		console.debug('html is ' + html);
		var test1 = dojo.byId('test1');
		test1.innerHTML = html;
		
		html = html_maker.table(html_maker.make_row(['a', 'b', 'c']));
		console.debug('html is ' + html);
		var test2 = dojo.byId('test2');
		test2.innerHTML = html;
	},
	
};



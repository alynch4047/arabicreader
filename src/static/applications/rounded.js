/**
 * @author alynch
 */

rounded = {

   wrap_in_round_corners: function(content, headline, colour) {
   	
		if (! colour) {
			colour = 'blue';
		}
		
		var class_main = 'rr_box_' + colour;
		var class_outer = 'rr_box_outer_' + colour;
		var class_inner = 'rr_box_inner_' + colour;
		var class_header = 'rr_box_header_' + colour;
	
   	    var outer_html = '<div class="' + class_main + '">' +
	   				       '<div class="' + class_outer + '">' +
	   				         '<div class="' + class_inner + '">' +
	   				           '<div class="' + class_header + '">' + headline + '</div>' +
	   				           '<div class="rr_box_content">' + content + '</div>' +
	   				         '</div>' +  
	   				       '</div>' +
	   				     '</div>'; 
   				 
   	    return outer_html;   
   }
   
};
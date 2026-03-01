

arabic =  {

  // always use caps for hex
  replacement:  { 'x600': 0x600,
//                  'x649': 0x64A,
                  'x6E1': 0x652,
                  'x670': 0x627,
                  'x671': 0x627
  },
  //PDF pop directional format
  skip: { 'x202c': 1
  },
  
  is_arabic_word: function(text) {
		var char_0 = text.charCodeAt(0);
		if (char_0 < 0x600 || char_0 > 0x700) {
			return false;
		}
		return true;
  },

  normalise_arabic: function (text) {
    // remove all 0x0A s
  	text = text.replace('\n', '');
  	var normalised_text = '';
  	var chrs = text.split('');
  	for (chr_ix in chrs) {
  		var chr = chrs[chr_ix];
  		// add hexadecimal of charcode to 'x'
  		var chr_code_s = 'x' + chr.charCodeAt(0).toString(16).toUpperCase();
  		if (chr_code_s in this.replacement) {
  			normalised_text = normalised_text + 
  					String.fromCharCode(this.replacement[chr_code_s]);
  		}
  		else if (chr_code_s > 0xFB00 && chr_code_s < 0xFF00) { 
  			console.debug('lost presentation character code ' + chr + '!');
  		}
  		else if (chr_code_s in this.skip) { 
  			console.debug('skip ' + chr + '!');
  		}
  		else {
  			normalised_text = normalised_text + chr;
  		}
  	}
 	return normalised_text;
  }
};
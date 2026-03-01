/**
 * @author alynch
 */
 
organise_vocab = {
		
	_populated: false,
		
	populate: function() {
		if (! organise_vocab._populated) {
			var html = '<table>';
			if (! vocab.word_sets) {
				return;
			}
			console.debug('ov wordsets ' + vocab.word_sets);
			var column = 0;
			for (ix in vocab.word_sets) {
				if (column == 0) {
				html += '<tr>';
				}
				html += '<td class="organise_vocab_cell">';
				word_set = vocab.word_sets[ix];
				html += rounded.wrap_in_round_corners(
								word_set.get_html(['remove_button']),
								'.', 'black');
				html += '</td>';
				if (column == 2) {
					html += '</tr>';
					column = 0;
				}
				else {
					column += 1;
				}
			}
			html += '</table>';
			var organise_vocab_wordsets_node = dojo.byId('organise_vocab_wordsets');
			organise_vocab_wordsets_node.innerHTML = html;
			dojo.parser.parse(organise_vocab_wordsets_node);
//			organise_vocab._populated = true;
		}
	}
};


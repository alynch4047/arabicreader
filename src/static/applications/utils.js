function Hash()
{
	this.length = 0;
	this.items = new Array();
	for (var i = 0; i < arguments.length; i += 2) {
		if (typeof(arguments[i + 1]) != 'undefined') {
			this.items[arguments[i]] = arguments[i + 1];
			this.length++;
		}
	}
   
	this.removeItem = function(in_key)
	{
		var tmp_previous;
		if (typeof(this.items[in_key]) != 'undefined') {
			this.length--;
			var tmp_previous = this.items[in_key];
			delete this.items[in_key];
		}
	   
		return tmp_previous;
	};

	this.getItem = function(in_key) {
		return this.items[in_key];
	};

	this.setItem = function(in_key, in_value)
	{
		var tmp_previous;
		if (typeof(in_value) != 'undefined') {
			if (typeof(this.items[in_key]) == 'undefined') {
				this.length++;
			}
			else {
				tmp_previous = this.items[in_key];
			}

			this.items[in_key] = in_value;
			console.debug('teism are ' + this.items);
		}
	   
		return tmp_previous;
	};

	this.hasItem = function(in_key)
	{
		return typeof(this.items[in_key]) != 'undefined';
	};

	this.clear = function()
	{
		for (var i in this.items) {
			delete this.items[i];
		}

		this.length = 0;
	};
}

/* from http://www.faqts.com/knowledge_base/view.phtml/aid/30209/fid/144 */
remove_array_duplicates = function(array_, customCompare ){
  if ( customCompare ){
      array_.sort(customCompare);
      for (var i=0; i<(array_.length-1); i++)
      {
         if ( !customCompare(array_[i],array_[i+1]) ){
            array_.splice( (i--)+1, 1 );
         }
      }
  } else {
      array_.sort();
      for (var i=0; i<(array_.length-1); i++)
      {
         if (array_[i]==array_[i+1]){
            array_.splice( (i--)+1, 1 );
         }
      }
   }
  return array_;
};



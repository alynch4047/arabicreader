var linkTargetFinder = function () {
	var prefManager = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
	return {
		init : function () {
			gBrowser.addEventListener("load", function () {
				var autoRun = prefManager.getBoolPref("extensions.arext.autorun");
				if (autoRun) {
					linkTargetFinder.run();
				}
			}, false);
		},

		run : function () {
			
			var selectedText = content.getSelection().toString();
			var sidebarWindow = document.getElementById("sidebar").contentWindow;
			
			if (sidebarWindow.location.href == "chrome://arext/content/arsidebar.xul") {
				sidebarWindow.arsb.set_word(selectedText);
			} 


		}
	};
}();
window.addEventListener("load", linkTargetFinder.init, false);

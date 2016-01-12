"use strict";

var codeMangler = codeMangler || {};

codeMangler.AppRouter = Backbone.Router.extend({
	routes : {
		"*default": "home"
	},

	home: function() {
		if (!this.homeView) {
        this.homeView = new codeMangler.Home();
    }
    $('#content').html(this.homeView.render().el);
	}
});

codeMangler.utils.loadTemplates(['Home'], function() {
	codeMangler.app = new codeMangler.AppRouter();
	Backbone.history.start();
});

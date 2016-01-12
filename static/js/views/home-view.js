"use strict";


var codeMangler =  codeMangler || {};

codeMangler.Home = Backbone.View.extend({

  /** Render the View */
  render: function () {
    // set the view element ($el) HTML content using its template
    this.$el.html(this.template());
    return this;    // support method chaining
  }
});
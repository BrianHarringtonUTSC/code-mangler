$(function() {
  $('#answerQuestion').click(function(e) {
    $.ajax({
      url: '/question/' + e.target.value,
      type: 'POST',
      data: {answer: $('#answerText').val()},
      success: function(response) {
        console.log(response);
      },
    });
  });
});
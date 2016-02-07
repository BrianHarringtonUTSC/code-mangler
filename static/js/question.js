$(function() {
    $('#answerQuestion').click(function(e) {
        $.ajax({
            url: '/question/' + e.target.value,
            type: 'POST',
            contentType: 'application/json',
            data: {'answer': JSON.stringify(getLineOrder())},
            success: function(response) {
                $('#result').html(response);
            },
        });
    });

   $('#lines').sortable({containment: "parent"});
   $('#lines').disableSelection();
});
function getAnswer() {
    var answers = $('#lines').sortable('toArray', {attribute: 'answerLine'});
    var result = [];
    for (var i = 0; i < answers.length; i++) {
        if (answers[i]) {
            result.push(parseInt(answers[i]));
        }
    }
    return result;
}

function getLineOrder() {
    var lineOrders = $('#lines').sortable('toArray', {attribute: 'lineNum'});
    var res = [];
    for (var i = 0; i < lineOrders.length; i++) {
        if (lineOrders[i]) {
            res.push(parseInt(lineOrders[i]));
        }
    }
    return res;
}

$(function() {
    $('#answerQuestion').click(function(e) {
        $.ajax({
            url: '/question/' + e.target.value,
            type: 'POST',
            data: {'answer': JSON.stringify(getLineOrder())},
            success: function(response) {
                $('#result').html(response);
            },
        });
    });

   $('#lines').sortable({containment: "parent"});
   $('#lines').disableSelection();
});

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

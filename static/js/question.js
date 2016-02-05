$(function() {
    $('#answerQuestion').click(function(e) {
        var lineOrders = $('#lines').sortable('toArray', {attribute: 'lineNum'});

        var ans = [];
        for (var i = 0; i < lineOrders.length; i++) {
            if (lineOrders[i]) {
                ans.push(parseInt(lineOrders[i]));
            }
        }
        console.log();

        $.ajax({
            url: '/question/' + e.target.value,
            type: 'POST',
            data: {'answer': JSON.stringify(ans)},
            success: function(response) {
                $('#result').html(response);
            },
        });
    });

   $('#lines').sortable({containment: "parent"});
   $('#lines').disableSelection();
});

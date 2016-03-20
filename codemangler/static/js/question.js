const INDENTATION_AMOUNT = 40; // in px

$(function () {
    $('#answer-question').click(sendAnswer);
    $('.right-arrow').click(addIndentation);
    $('.left-arrow').click(removeIndentation);
    $('#lines').sortable({containment: "parent"});
    $('#lines').disableSelection();
});

function getLineOrder() {
    var lineOrder = [];
    $('.line').each(function (index, line) {
        var lineNum = $(line).attr('line-num');
        lineOrder.push(parseInt(lineNum));
    });
    return lineOrder;
}

function getIndentations() {
    var indentations = [];
    $('.text').each(function (index, text) {
        var indentation = parseInt($(text).css('margin-left'));
        indentations.push(parseInt(indentation / INDENTATION_AMOUNT));
    });
    return indentations;
}

function sendAnswer(e) {
    $.ajax({
        url: '/question/' + e.target.value,
        type: 'POST',
        data: {'order': JSON.stringify(getLineOrder()), 'indentation': JSON.stringify(getIndentations())},
        success: function (response) {
            $('#result').html(response);
        },
    });
}

function changeIndentation(e, value) {
    var code = $(e.target).siblings('.code')
    var text = code.find('.text');
    var maxWidth = code.width() - text.width();
    var oldIndentation = parseInt(text.css('margin-left'));
    var newIndentation = oldIndentation + value;
    if (newIndentation >= 0 && newIndentation < maxWidth) {
        text.css('margin-left', newIndentation);
    }
}

function addIndentation(e) {
    changeIndentation(e, INDENTATION_AMOUNT);
}

function removeIndentation(e) {
    changeIndentation(e, -INDENTATION_AMOUNT);
}


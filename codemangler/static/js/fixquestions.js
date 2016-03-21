/**
 * Created by Tanjid Islam on 21/03/2016.
 */
var maxheight = 0;
var maxwidth = 0;

$('div div.col-ques').each(function () {
    maxheight = ($(this).height() > maxheight ? $(this).height() : maxheight);
    maxwidth = ($(this).width() > maxwidth ? $(this).width() : maxwidth);
});

$('div div.col-ques').height(maxheight);
$('div div.col-ques').width(maxwidth);
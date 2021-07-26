var i
var j
function pairs(num, size) {
    $.getJSON(num + ".json")
        .done(function (data) {
            var urls = data;
            // Randomly sample without replacement. https://stackoverflow.com/a/12987776.
            var indices = [];
            for (var i=0;i<=urls.length-1;i++) { indices.push(i) }
            function sample() {
                var randomIndex = Math.floor(Math.random()*indices.length);
                return indices.splice(randomIndex, 1)[0];
            }
            for (var n=1;n<=size;n++) { 
                i = sample();
                j = sample();
                var uid_i = urls[i].split("/")[5].split("_")[0]
                var uid_j = urls[j].split("/")[5].split("_")[0]
                
                $('body').append('<h1> Pair ' + n + ": " + uid_i + '_' + uid_j + '</h1>');
                $('body').append('<div class="main_block"><div class="inner_block"><img src="'+urls[i]+'"></div><div class="inner_block"><img src="'+urls[j]+'"></div></div>');
                $('body').append('<hr>')
            }
        });
    }
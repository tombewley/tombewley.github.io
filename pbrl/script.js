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
            for (var i=1;i<=size;i++) { 
                var idx = sample();
                var uid = urls[idx].split("/")[5].split("_")[0]

                document.write('<h1> Pair ' + i + ": " + uid + '</h1>')

                document.write('<img src="' + urls[idx] + '" style="width:500px">')
                // document.write("<p>" + urls[idx] + "</p>")

            }
        });
    }
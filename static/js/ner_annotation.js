$(function(){
    var annotate_button = function(x){
        x.click(function(){
            var selection = window.getSelection();
            if(selection.getRangeAt) {
                var range = selection.getRangeAt(0);
                var newnode = document.createElement("span");
                newnode.setAttribute("class", $(this).attr("id"));
                range.surroundContents(newnode);
            }
        });
    }
    
    var submit_parse = function(x){
        x.click(function(){
            var max_step_num = $("#max_step").text();
            var results = []
            for(var i=0; i<max_step_num; i++) {
                var annotation = $("#sentence_" + i).children("span");
                var sentence = $("#sentence_" + i).text().trim();
                var result = {"sentence" : sentence, "annotation" : []}
                for(var j=0; j<annotation.length; j++) {
                    var annotation_word = $(annotation[j]).text();
                    var annotated_class = $(annotation[j]).attr("class");
                    result["annotation"].push(annotation_word);
                }
                results.push(result);
            }
            $("#results").val(JSON.stringify(results));
        });
    }

    annotate_button($("#action"));
    submit_parse($("#submit"));

    $(".jump").each(function(){
        $(this).on('click', function(){
            var start_time = $(this).attr("class").split("_")[1];
            var video_url = $("#yc_video").attr("src").split("?")[0];
            var jumped_url = video_url + "?start=" + start_time;
            $("#yc_video").attr("src", jumped_url);
        });
    });
});

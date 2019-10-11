var questionSelector = ".question-text";
var sgaURI = "https://quizlet.shitchell.com/search?q="
var queryWordCount = 15;
var queryWordStart = 4;

function sgaSearch(node) {
	var words = node.innerText.replace("\n", " ").split(" ");
	var wordStart = 0;
	var wordEnd = 0;
	if (words.length > (queryWordCount + queryWordStart)) {
		wordStart = queryWordStart;
		wordEnd = queryWordStart + queryWordCount;
	} else if (words.length >= queryWordCount){
		wordStart = words.length - queryWordCount;
		wordEnd = words.length - 1;
	} else {
		wordStart = 0;
		wordEnd = words.length - 1;
	}
	var query = words.slice(wordStart, wordEnd + 1).join(" ");
    $.ajax({
        url: sgaURI + encodeURIComponent(query),
        dataType: "json"
    }).done(function(data) {
        buildLinks(data, node);
    });
}

function buildLink(uri, linkText, answer) {
    a = document.createElement("a");
    a.href = uri;
    a.innerText = linkText;
    a.style = "color: inherit; margin-right: 1em;";
    a.className += "sga-tooltip";
    a.setAttribute("data-definition", answer);
    return a;
}

function buildLinks(data, node) {
    div = $('<div class="sga-links">');
    for (var i = 0; i < data.results.length; i++) {
        result = data.results[i];
        link = buildLink(result.ref, i + 1, result.definition);
        $(div).append(link);
    }
    console.log("inserting", div, "after", node);
    $(node).after(div);
}

$(document).ready(function() {
	// Create the answer box to display answers
	var answerBox = document.createElement("div");
	answerBox.style = "position: fixed; bottom: 0; left: 0; right: 0; height: 100px; overflow: auto; padding: 1em; background-color: #FFF; box-shadow: 0 3px 6px rgba(0, 0, 0, 0.5); display: none; color: #000;";
	answerBox.setAttribute("id", "sga-answer-box");
	$("body").append(answerBox);

	// Set all links to display their answer on hover
	$(document).on("mouseenter", ".sga-tooltip", function() {
		console.log("hovering", answerBox);
		answerBox.style.display = "initial";
		answerBox.innerText = this.getAttribute("data-definition");
	});
	$(document).on("mouseleave", ".sga-tooltip", function() {
		answerBox.style.display = "none";
		answerBox.innerText = "";
	})
	
    $(questionSelector).each(function(i, el) {
        console.log("Analyzing node", el);
        sgaSearch(el);
    });
});
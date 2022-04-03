var lemma_search_input = document.getElementById("lemma_search_input")
lemma_search_input.addEventListener("mouseover", function() {
    lemma_search_input.focus();
    lemma_search_input.select();
});


lemma_search_input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("search_word_btn").click();
    }
});


function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        alert("load");
        // document.getElementById("demo").innerHTML = this.responseText;
    }
    xhttp.open("GET", "ajax_info.txt", true);
    xhttp.send();
}


function search_word() {
    const form = document.createElement("form");
    form.method = "post";
    form.action = "../../show_word_info/";
    var data = {
        "word": document.getElementById("lemma_search_input").value,
        "csrfmiddlewaretoken": csrf_token
    };
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            const hiddenField = document.createElement("input");
            hiddenField.type = "hidden";
            hiddenField.name = key;
            hiddenField.value = data[key];
            form.appendChild(hiddenField);
        }
    }
    document.body.appendChild(form);
    form.submit();
}

lemma_search_input.focus();

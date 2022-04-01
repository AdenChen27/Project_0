

function set_blank(blank_id, value) {
    document.getElementById(`blank_word_${blank_id}`).innerHTML = value;
}


for (const blank_id in ans) {
    // blanks
    var blank = document.getElementById(`blank_${blank_id}`);
    var blank_num = document.createElement("span");
    var blank_word = document.createElement("span");
    
    blank_word.id = `blank_word_${blank_id}`;

    blank.appendChild(blank_num);
    blank.appendChild(blank_word);

    blank.classList.add("blank");
    blank_num.classList.add("blank_num");
    blank_word.classList.add("blank_word");

    blank_word.innerHTML = "&nbsp;".repeat(10);
    blank_num.innerHTML = ans[blank_id]["index"] + " ";

}



// mark a `blank_word` correct/wrong
function mark(blank_word, correct) {
    if (blank_word.classList.contains("ans-correct")) {
        blank_word.classList.remove("ans-correct");
    } else if (blank_word.classList.contains("ans-wrong")) {
        blank_word.classList.remove("ans-wrong");
    }

    if (correct) {
        blank_word.classList.add("ans-correct");
    } else {
        blank_word.classList.add("ans-wrong");
    }
}


function check() {
    for (const blank_id in ans) {
        var blank_word = document.getElementById(`blank_word_${blank_id}`);
        mark(
            blank_word,
            blank_word.innerHTML == ans[blank_id]["name"]
        );
    }
}


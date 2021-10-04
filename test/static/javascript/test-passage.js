var count_down_display = document.getElementById("count_down_display"), 
    time = 0, 
    counter = -1, 
    selected_words = new Set([]), 
    word_audio_loded = new Set(),
    hint_clipboard_word_id = -1, 
    hint_clipboard_word_name, 
    chosen_count = {}, 
    chosen_word = {};//blank_id -> word_id


function get_chosen_cnt(word_id, add=0) {
    if (chosen_count[word_id]) {
        chosen_count[word_id] += add;
    } else {
        chosen_count[word_id] = add;
    }
    return chosen_count[word_id];
}


function click_hint(word_id, word_name) {
    if (hint_clipboard_word_id != -1) {
        var pre_hint = document.getElementById("hint_" + hint_clipboard_word_id);
        pre_hint.style.backgroundColor = `rgb(30, 144, 255, ${get_chosen_cnt(hint_clipboard_word_id)/10})`;
        pre_hint.style.borderColor = "#FFF";
    }
    var hint = document.getElementById("hint_" + word_id);
    hint.style.borderColor = "rgb(30, 144, 255)";
    hint_clipboard_word_id = word_id;
    hint_clipboard_word_name = word_name;
}


function click_blank(blank_id) {
    var blank = document.getElementById("blank_" + blank_id);
    if (blank.innerHTML != "_____") {
        blank.innerHTML = "_____";
        var word_id = chosen_word[blank_id], 
            hint = document.getElementById("hint_" + word_id);
        hint.style.backgroundColor = `rgb(30, 144, 255, ${get_chosen_cnt(word_id, -1)/10})`;
        chosen_word[blank_id] = null;
    }
    if (hint_clipboard_word_id == -1) {
        return ;
    }
    blank.innerHTML = hint_clipboard_word_name;
    var hint = document.getElementById("hint_" + hint_clipboard_word_id);
    hint.style.backgroundColor = `rgb(30, 144, 255, ${get_chosen_cnt(hint_clipboard_word_id, 1)/10})`;
    chosen_word[blank_id] = hint_clipboard_word_id;
}


function play_audio(word_id, word_name) {
    if (word_audio_loded.has(word_id)) {
        audio = document.getElementById(`word_audio_${word_id}`).play();
    } else {
        var words = new SpeechSynthesisUtterance(word_name);
        window.speechSynthesis.speak(words);
    }
}


function check() {
    for (blank_id in chosen_word) {
        if (chosen_word[blank_id] == ans[parseInt(blank_id)]) {
            document.getElementById("blank_" + blank_id).style.color = "rgb(27, 176, 60)";
        } else {
            document.getElementById("blank_" + blank_id).style.color = "rgb(234, 27, 70)";
        }
    }
}


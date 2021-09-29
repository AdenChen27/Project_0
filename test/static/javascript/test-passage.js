var count_down_display = document.getElementById("count_down_display"), 
    time = 0, 
    counter = -1, 
    selected_words = new Set([]), 
    word_audio_loded = new Set(),
    hint_clipboard_word_id = -1, 
    hint_clipboard_word_name, 
    chosen_count = {}
    chosen_word = {};//blank_id -> word_id


function start_timer() {
    if (counter == -1) {
        counter = setInterval(function () {
            time += 1;
            time_m = Math.floor(time/60);
            time_s = time % 60;
            display_text = time_s + "s";
            if (time_m != 0)
            {
                display_text = time_m + "m" + display_text;
            }

            count_down_display.innerHTML = display_text;
        }, 1000);
    }
}

function stop_timer() {
    if (counter != -1) {
        clearInterval(counter);
        counter = -1;
    }
}


function choose_word(word_id)
{
    word_block = document.getElementById("word_" + word_id);
    if (word_block == null) {
        return -1;
    }
    if (selected_words.has(word_id)) {
        selected_words.delete(word_id);
        word_block.style.backgroundColor = "#FFFFFF";
        word_block.style.borderBottomStyle = "hidden";
    } else {
        selected_words.add(word_id)
        word_block.style.backgroundColor = "#FCFBB0";
        word_block.style.borderBottomColor = "#808080";
        word_block.style.borderBottomStyle = "solid";
    }
}


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
    }
    var hint = document.getElementById("hint_" + word_id);
    hint.style.backgroundColor = "rgb(30, 144, 255)";
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
    hint_clipboard_word_id = -1;
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


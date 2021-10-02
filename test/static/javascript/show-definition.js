var word_audio_loded = new Set();


function create_div(class_name, parent, expend=null) {
    var name = "div";
    if (expend && expend["name"]) {
        name = expend["name"];
    }
    var new_element = document.createElement(name);
    new_element.className = class_name;

    if (expend) {
        if (expend["text"]) {
            new_element.innerText = expend["text"];
        }
        if (expend["id"]) {
            new_element.id = expend["id"];
        }
    }
    if (parent) {
        parent.appendChild(new_element);
    }
    return new_element;
}

function click_event(element_id) {
    var element = document.getElementById(element_id);
    if (element.classList.contains("text-hide")) {
        element.classList.remove("text-hide");
    } else {
        element.classList.add("text-hide");
    }
}


function element_hide_control(element_id, show) {
    var element = document.getElementById(element_id);
    if (show == true) {
        if (element.classList.contains("text-hide")) {
            element.classList.remove("text-hide");
        }
    } else {
        if (!element.classList.contains("text-hide")) {
            element.classList.add("text-hide");
        }
    }
}


function flip_all(btn_id, element_suffix) {
    const button = document.getElementById(btn_id);
    var show;
    if (button.innerText.includes("Hide")) {
        show = false;
        button.innerText = button.innerText.replace("Hide", "Show");
    } else {
        show = true;
        button.innerText = button.innerText.replace("Show", "Hide");
    }
    for (var i in lemmas_id) {
        element_hide_control(element_suffix + lemmas_id[i], show);
    }
}



function change_defs_show_state(btn_id) {
    const button = document.getElementById(btn_id);
    var show;
    // 0 -> show all defs
    // 1 -> show only def_en
    // 2 -> show only def_zh
    if (button.innerHTML.includes("English")) {
        show = 1;
        button.innerHTML = "Show Chinese Definition Only";
    } else if (button.innerHTML.includes("Chinese")) {
        show = 2;
        button.innerHTML = "Show Both Definitions";
    } else {
        show = 0;
        button.innerHTML = "Show English Definition Only";
    }
    for (var i in lemmas_id) {
        lem_id = lemmas_id[i];
        if (show == 0) {
            document.getElementById(`def_en_${lem_id}`).style.display = "flex";
            document.getElementById(`def_zh_${lem_id}`).style.display = "flex";
        } else if (show == 1) {
            document.getElementById(`def_en_${lem_id}`).style.display = "flex";
            document.getElementById(`def_zh_${lem_id}`).style.display = "none";
        } else {
            document.getElementById(`def_en_${lem_id}`).style.display = "none";
            document.getElementById(`def_zh_${lem_id}`).style.display = "flex";
        }
    }
}


function export_word_to_str(format, word_id) {
    const e_word_name = document.getElementById(`word_name_${word_id}`);
    const e_def_en = document.getElementById(`def_en_${word_id}`);
    const e_def_zh = document.getElementById(`def_zh_${word_id}`);
    var export_str = "";
    for (var i in format) {
        if (format[i] == 'w') {
            export_str += e_word_name.innerText;
        } else if (format[i] == 'E') {
            export_str += e_def_en.innerText.replace(/\n/g, ';');
        } else if (format[i] == 'Z') {
            export_str += e_def_zh.innerText.replace(/\n/g, ';');
        } else if (format[i] == 'n') {
            export_str += '\n';
        } else if (format[i] == 't') {
            export_str += '\t';
        } else {
            export_str += format[i];
        }
    }
    return export_str;
}


function export_words() {
    const format = document.getElementById("export_option").value;
    // string to indicate export format
    // 'w' for word; 
    // 'E' for English definition
    // 'Z' for Chinese definition
    // 't' for '\t'; 'n' for '\n'
    // else: copy
    document.getElementById("export_copy_textarea_block").style.display = "block";
    if (format == "null")
    {
        alert("Please Select Export Format.");
        return;
    }

    const textarea = document.getElementById("export_copy_textarea");
    var export_text = "";
    for (var i in lemmas_id) {
        export_text += export_word_to_str(format, lemmas_id[i]);
    }
    textarea.value = export_text;
}


function shuffel() {
    var def_rows = document.getElementsByName("def-row");
    for (const i in def_rows) {
        if (def_rows[i].style) {
            def_rows[i].style.order = Math.floor(Math.random() * 100);
        }
    }
}


function play_audio(word_id, word_name) {
    if (word_audio_loded.has(word_id)) {
        audio = document.getElementById(`word_audio_${word_id}`).play();
    } else {
        var words = new SpeechSynthesisUtterance(word_name);
        window.speechSynthesis.speak(words);
    }
}


function next() {
    const form = document.createElement("form");
    form.method = "post";
    form.action = "../submit_selected_words/";
    var data = {
        "p_id": p_id, 
        "lemma_id": lemmas_id, 
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


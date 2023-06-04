var selected_words = new Set([]);
const WORD_PER_ROW = 6;


function word_reverse_sel(word) {
    // word: html tag or word_id
    var word_id, word_e;
    if (Number.isInteger(word)) {
        word_id = word;
    } else {
        word_id = word.id;
    }
    word_e = document.getElementById(word_id);
    if (selected_words.has(word_id)) {
        selected_words.delete(word_id);
        word_e.classList.remove("selected");
    } else {
        selected_words.add(word_id)
        word_e.classList.add("selected");
    }
}

// (un)select word_e
// sel: true/false
function word_set_sel(word_e, sel) {
    var word_id = word_e.id;
    if (sel && !selected_words.has(word_id)) {
        // select word
        selected_words.add(word_id)
        word_e.classList.add("selected");
    } else if (!sel && selected_words.has(word_id)) {
        // unselect word
        selected_words.delete(word_id);
        word_e.classList.remove("selected");
    }
}

function onclick_listener(event) {
    word_reverse_sel(event.target);
}

// mouseover + left button down -> select
// mouseover + left button down + alt/option -> unselect
function mouseover_listener(event) {
    if (event.buttons == 1) {
        word_set_sel(event.target, !event.altKey);
    }
}


function submit() {
    const form = document.createElement("form");
    form.method = "post";
    form.action = "show_definition/";
    var data = {
        "p_id": p_id,
        "lemma_id": Array.from(selected_words),
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

var word_list = [];
// [[word_element, word_object]..]


function filter_select() {
    var value = document.getElementById("lem_rank_filter").value / 100;
    var threshold = value*word_list.length;
    for (var i in word_list) {
        var word = word_list[i][1];
        var freq = word["freq"];
        if (i < threshold && !selected_words.has(word["id"])) {
            word_reverse_sel(Number(word["id"]));
        } else if (i >= threshold && selected_words.has(word["id"])) {
            word_reverse_sel(Number(word["id"]));
        }
    }
}


function create_div(class_name, parent, expend = null) {
    new_div = document.createElement("div");
    new_div.className = class_name;

    if (expend) {
        if (expend["text"]) {
            new_div.innerText = expend["text"];
        }
        if (expend["id"]) {
            new_div.id = expend["id"];
        }
    }
    if (parent) {
        parent.appendChild(new_div)
    }
    return new_div;
}




for (var i in pre_word_list) {
    if (/[A-Z]/.test(pre_word_list[i]["name"])) {
        pre_word_list[i]["freq"] = 0;
    }
}


function main() {
    pre_word_list.sort((a, b) => {
        return a["freq"] - b["freq"];
    });

    var word_holder = document.getElementById("word_holder"),
        cur_row_div,
        word_n = 0;

    for (var word_i in pre_word_list) {
        var word = pre_word_list[word_i];
        if (word["name"].length <= 1) {
            continue;
        }
        if (word_n % WORD_PER_ROW == 0) {
            cur_row_div = create_div("row", word_holder, {
                "id": "word_row_" + Math.floor(word_n / WORD_PER_ROW),
            });
        }
        var word_div = create_div("col-2", cur_row_div);
        var new_word = create_div("sel-word-block noselect", word_div, {
            // "id": "word_" + word["id"],
            "id": word["id"],
            "text": word["name"],
        });
        // new_word.setAttribute("onclick", "choose_word(" + word["id"] + ")");
        new_word.addEventListener("click", onclick_listener);
        new_word.addEventListener("mouseout", mouseover_listener);
        word_list.push([new_word, word]);
        word_n += 1;
    }

    document.getElementById("lem_rank_filter").value = 0;
    filter_select();
}

main();


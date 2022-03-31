
function shuffle(array) {
    var cur_i = array.length,
        rand_i;
    while (cur_i) {
        rand_i = Math.floor(Math.random() * cur_i);
        cur_i--;
        [array[cur_i], array[rand_i]] = [array[rand_i], array[cur_i]];
    }

    return array;
}


function check() {
    for (blank_id in ans) {
        var blank = document.getElementById("blank_" + blank_id)
        if (blank.value) {
            if (blank.value.toLowerCase() == ans[parseInt(blank_id)]["name"].toLowerCase()) {
                blank.style.color = "rgb(27, 176, 60)";
            } else {
                blank.style.color = "rgb(234, 27, 70)";
            }
        }
    }
}


function main() {
    for (blank_id in choices) {
        var blank = document.getElementById("blank_" + blank_id)
        var cur_choices = shuffle(choices[blank_id]);
        for (i in cur_choices) {
            var opt = document.createElement("option");
            opt.value = cur_choices[i];
            opt.innerHTML = cur_choices[i];
            blank.appendChild(opt);
        }
    }
}


main();


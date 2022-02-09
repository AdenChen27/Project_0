
function check() {
    for (blank_id in ans) {
        var blank = document.getElementById("blank_" + blank_id)
        if (blank.value)
        {
            console.log(blank.value, ans[parseInt(blank_id)]["name"])
            if (blank.value == ans[parseInt(blank_id)]["name"]) {
                blank.style.color = "rgb(27, 176, 60)";
            } else {
                blank.style.color = "rgb(234, 27, 70)";
            }
        }
    }
}


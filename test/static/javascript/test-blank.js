
function check() {
    for (blank_id in ans) {
        var blank = document.getElementById("blank_" + blank_id)
        if (blank.value)
        {
            if (blank.value.toLowerCase() == ans[parseInt(blank_id)]["name"].toLowerCase()) {
                blank.style.color = "rgb(27, 176, 60)";
            } else {
                blank.style.color = "rgb(234, 27, 70)";
            }
        }
    }
}


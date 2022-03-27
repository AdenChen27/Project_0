function set_lang(lang) {
    str="/i18n/setlang/";
    myform = document.getElementById('testform');
    myform.value = lang;
    myform.method = "POST";
    myform.action = str;
    document.getElementById("language").value = lang;
    myform.submit();
}

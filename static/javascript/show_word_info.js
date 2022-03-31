function play_audio(word_id, word_name) {
    if (audio_loaded) {
        audio = document.getElementById(`word_audio_${word_id}`).play();
    } else {
        var words = new SpeechSynthesisUtterance(word_name);
        window.speechSynthesis.speak(words);
    }
}



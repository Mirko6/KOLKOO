const text_is_hate_speech = (text) => {
    let url = `http://127.0.0.1:5001/api/v1/get-sentiment-for-text?text=${encodeURIComponent(text)}`;
    let response = await fetch(url);
    if (response.hate) return true;
    return false;
}

document.addEventListener('DOMContentLoaded', (event) => {
    let inputs = document.getElementsByTagName('input');
    for (let input of inputs) {
        input.addEventListener('onChange', (event) => {
            let value = input.value;
            let is_hate = text_is_hate_speech(value);
            if (is_hate) {
                alert('Hejtyyyy ty kaaar');
            }
        })
    }
});

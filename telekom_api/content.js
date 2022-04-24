async function text_is_hate_speech(text) {
    let url = `http://127.0.0.1:5001/api/v1/get-sentiment-for-text?text=${encodeURIComponent(text)}`;
    let response = await fetch(url);
    return response.json();
}

if(document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded',afterDOMLoaded);
} else {
    afterDOMLoaded();
}

function afterDOMLoaded(){
    setTimeout(function(){
        let inputs = document.getElementsByTagName('input');
        for (let input of inputs) {
            input.onchange = async function () {
                let value = input.value;
                text_is_hate_speech(value)
                    .then(returned => {if (returned.hate) {alert('POZOR! Pises nieco zle.');}});
            }
        }
    }, 1000);
}

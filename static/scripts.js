function openPopup(url) {
    window.open(url, "popupWindow", "width=1024,height=768");
}

function selectValue(fieldId, value) {
    window.opener.document.getElementById(fieldId).value = value;
    window.close();
}

function wipeForm() {
    const form = document.getElementById('myForm');
    form.querySelectorAll('input, textarea, select').forEach(el => {
        if (el.type !== 'submit' && el.type !== 'button' && el.type !== 'hidden') {
            el.value = '';
        }
    });
}

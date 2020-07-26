let inputs = document.querySelectorAll("input[type='file']");

function set_label_filename(e, is_change) {
    if (is_change) {
        e = e.srcElement;
    }
    if (e.files.length > 0) {
        let filename = e.files[0].name;
        e.labels[0].textContent = filename;
    }
}

inputs.forEach(e => {
    set_label_filename(e, false);
});
Array.prototype.forEach.call(inputs, input => {
    input.addEventListener('change', e => {
        set_label_filename(e, true);
    });
});

'use strict';

function only_number(evt) {
    var charCode = evt.which ? evt.which : Event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57)){
        return false
    }
    return true;
}

function currentDate() {
    document.getElementById('patient-dob').value = new Date().toISOString().substring(0, 10);
}
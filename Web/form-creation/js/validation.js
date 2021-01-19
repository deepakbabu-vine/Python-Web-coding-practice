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

function calculateAge() {
    var curDate = new Date().toISOString().substring(0,10);
    var specifiedDate = document.getElementById('patient-dob').value
    var formattedCurDate = new Date(curDate);
    var formattedSpecifiedDate = new Date(specifiedDate);
    const milliSeconds = Math.ceil(formattedCurDate - formattedSpecifiedDate)
    var totaldays = Math.ceil(milliSeconds/(1000 * 60 * 60 * 24));
    var year = Math.floor(totaldays/365);
    if (year) {
        totaldays = totaldays - (year * 365);
    }
    var month = Math.floor(totaldays/30);
    if (month) {
        totaldays = totaldays - (month * 30);
    }
    document.getElementById('patient-age-year').value = year;
    document.getElementById('patient-age-month').value = month;
    document.getElementById('patient-age-date').value = totaldays;
}
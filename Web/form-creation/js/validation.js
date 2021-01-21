'use strict';

function initializeForm() {
    currentDate();
    getPreviousFormData();
}

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
    var toggle_error_message = document.getElementById("invalid-date");
    var toggle_popup_arrow = document.getElementById("popup-arrow");
    var curDate = new Date().toISOString().substring(0,10);
    var specifiedDate = document.getElementById('patient-dob').value
    var formattedCurDate = new Date(curDate);
    var formattedSpecifiedDate = new Date(specifiedDate);
    var milliSeconds = Math.ceil(formattedCurDate - formattedSpecifiedDate)
    var totaldays = Math.ceil(milliSeconds/(1000 * 60 * 60 * 24));
    var year = Math.floor(totaldays/365);
    if (year) {
        totaldays = totaldays - (year * 365);
    }
    var month = Math.floor(totaldays/30);
    if (month) {
        totaldays = totaldays - (month * 30);
    }

    if ( year<0 || month<0 || totaldays<0){
        document.getElementById('patient-age-year').value = '-';
        document.getElementById('patient-age-month').value = '-';
        document.getElementById('patient-age-date').value = '-';
        toggle_error_message.style.display = "inline";
        toggle_popup_arrow.style.display = "inline";
    }
    else{
    document.getElementById('patient-age-year').value = year;
    document.getElementById('patient-age-month').value = month;
    document.getElementById('patient-age-date').value = totaldays;
    toggle_error_message.style.display = "none";
    toggle_popup_arrow.style.display = "none";
    }
}

function checkRemainingCharacters(currentInputElement) {
    var maxLimit = 50;
    var nameCounter = document.getElementById('name-counter'); 
    var surnameCounter = document.getElementById('surname-counter'); 
    if(currentInputElement == "name") {
        var remainingCharacters = 50-(document.getElementById('patient-name').value.length);
        nameCounter.innerHTML  = remainingCharacters + "chars. remaining";
    }
    if(currentInputElement == "surname") {
        var remainingCharacters = 50-(document.getElementById('patient-surname').value.length);
        surnameCounter.innerHTML  = remainingCharacters + "chars. remaining";
    }
}

function saveToJson() {
    const urlString = window.location.href;
    var url =  new URL(urlString);
    let student = {
        Prefix: url.searchParams.get("prefix"),
        Patient_Name: url.searchParams.get("patient-name"),
        Patient_surname: url.searchParams.get("patient-surname"),
        Patient_dob: url.searchParams.get("patient-dob"),
        Patient_marital_status: url.searchParams.get("patient-marital-status"),
        patient_gender: url.searchParams.get("patient-gender"),
        Basic_details_of_patient: url.searchParams.get("basic-details-of-patient")
    };
    let data = JSON.stringify(student);  
    console.log(data);
    if(!localStorage.getItem('form-data') == null){
        localStorage.removeItem('form-data');
    }
    localStorage.setItem('form-data', data);
}

function getPreviousFormData() {
    if(localStorage.getItem('form-data') !== null){
        var jsonDataFromLocalStorage = JSON.parse(localStorage.getItem('form-data'));
        document.getElementById('prefix').value = jsonDataFromLocalStorage.Prefix;
        document.getElementById('patient-name').value = jsonDataFromLocalStorage.Patient_Name;
        document.getElementById('patient-surname').value = jsonDataFromLocalStorage.Patient_surname;
        document.getElementById('patient-dob').value = jsonDataFromLocalStorage.Patient_dob;
        document.getElementById('patient-marital-status').value = jsonDataFromLocalStorage.Patient_marital_status;
        document.getElementById('patient-gender').value = jsonDataFromLocalStorage.patient_gender;
        document.getElementById('basic-details-of-patient').value = jsonDataFromLocalStorage.Basic_details_of_patient;
    }
}
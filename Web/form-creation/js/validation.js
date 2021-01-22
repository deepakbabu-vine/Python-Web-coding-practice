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
    SaveCurrentChangesToJson();
}

function checkRemainingCharacters(currentInputElement) {
    var maxLimit = 50;
    var nameCounter = document.getElementById('name-counter'); 
    var surnameCounter = document.getElementById('surname-counter'); 
    if(currentInputElement == "name") {
        var remainingCharacters = 50-(document.getElementById('patient-name').value.length);
        nameCounter.innerHTML  = remainingCharacters + "chars. remaining";
        SaveCurrentChangesToJson();
    }
    if(currentInputElement == "surname") {
        var remainingCharacters = 50-(document.getElementById('patient-surname').value.length);
        surnameCounter.innerHTML  = remainingCharacters + "chars. remaining";
        SaveCurrentChangesToJson();
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
        Patient_gender: url.searchParams.get("patient-gender"),
        Download_form_data: url.searchParams.get("download-form-data")
    };
    let data = JSON.stringify(student);  
    console.log(data);
    if(!localStorage.getItem('form-data') == null){
        localStorage.removeItem('form-data');
    }
    localStorage.setItem('form-data', data);
    if(url.searchParams.get("download-form-data")) {
        var Prefix = url.searchParams.get("prefix");
        var Patient_Name = url.searchParams.get("patient-name");
        var Patient_surname = url.searchParams.get("patient-surname");
        var Patient_dob = url.searchParams.get("patient-dob");
        var Patient_marital_status =  url.searchParams.get("patient-marital-status");
        var Patient_gender = url.searchParams.get("patient-gender");
        let data = 
        '\r Prefix: ' + Prefix + ' \r\n ' + 
        'Patient Name: ' + Patient_Name + ' \r\n ' + 
        'Patient Surname: ' + Patient_surname + ' \r\n ' + 
        'Patient DOB: ' + Patient_dob + ' \r\n ' + 
        'Patient marital status: ' + Patient_marital_status + ' \r\n ' + 
        'Patient_gender: ' + Patient_gender;  
        const textToBLOB = new Blob([data], { type: 'text/plain' });
        const fileName = 'formData.txt';	 
        let downloadLink = document.createElement("a");
        downloadLink.download = fileName;
        if (window.webkitURL != null) {
            downloadLink.href = window.webkitURL.createObjectURL(textToBLOB);
        }
        else {
            downloadLink.href = window.URL.createObjectURL(textToBLOB);
            downloadLink.style.display = "none";
            document.body.appendChild(downloadLink);
        }
        downloadLink.click(); 
    }
}

function getPreviousFormData() {
    if(localStorage.getItem('form-data') !== null){
        var jsonDataFromLocalStorage = JSON.parse(localStorage.getItem('form-data'));
        document.getElementById('prefix').value = jsonDataFromLocalStorage.Prefix;
        document.getElementById('patient-name').value = jsonDataFromLocalStorage.Patient_Name;
        if(jsonDataFromLocalStorage.Patient_Name.length > 0){
            document.getElementById('name-counter').innerHTML = (50 - jsonDataFromLocalStorage.Patient_Name.length) + "chars. remaining";
        } 
        document.getElementById('patient-surname').value = jsonDataFromLocalStorage.Patient_surname;
        if(jsonDataFromLocalStorage.Patient_surname.length > 0){
            document.getElementById('surname-counter').innerHTML = (50 - jsonDataFromLocalStorage.Patient_surname.length) + "chars. remaining";
        }
        document.getElementById('patient-dob').value = jsonDataFromLocalStorage.Patient_dob;
        document.getElementById('patient-marital-status').value = jsonDataFromLocalStorage.Patient_marital_status;
        document.getElementById('patient-gender').value = jsonDataFromLocalStorage.patient_gender;
        document.getElementById('download-form-data').checked = jsonDataFromLocalStorage.Download_form_data;
    }
}

function SaveCurrentChangesToJson() {
    var currentData = {
        Prefix: document.getElementById("prefix").value,
        Patient_Name: document.getElementById("patient-name").value,
        Patient_surname: document.getElementById("patient-surname").value,
        Patient_dob: document.getElementById("patient-dob").value,
        Patient_marital_status: document.getElementById("patient-marital-status").value,
        Patient_gender: document.getElementById("patient-gender").value,
        Download_form_data: document.getElementById("download-form-data").value

    }
    var JsonData = JSON.stringify(currentData);
    console.log(currentData);
    if(localStorage.getItem('form-data') !== null){
        localStorage.removeItem('form-data');
    }
    localStorage.setItem('form-data', JsonData);
}

function removeJsonData() {
    if(localStorage.getItem('form-data') !== null){
        localStorage.removeItem('form-data');
    }
}
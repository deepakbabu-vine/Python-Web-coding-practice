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

function addNewRow() {

    var contactInfoTable = document.getElementById('contact-info');
    var currentIndex = contactInfoTable.rows.length;
    if (currentIndex > 5) {
        alert("Max limit of 5 rows reached!");
        return;
    }
    var currentRow = contactInfoTable.insertRow(-1);
    var serialNumber = document.createElement('text');
    serialNumber.id = "sl"+currentIndex;
    serialNumber.innerHTML = parseInt(currentIndex); 
    var relationship = document.createElement('select');
    relationship.id = "relationship" + currentIndex;
    relationship.value = "relationship" + currentIndex;
    var array = ["Father", "Mother", "Son", "Daughter", "Others"];
    for (var i = 0; i < array.length; i++) {
        var option = document.createElement("option");
        option.value = array[i];
        option.text = array[i];
        relationship.appendChild(option);
    }
    var contactName = document.createElement('input');
    contactName.id = "contact" + currentIndex;
    var mobileNumber = document.createElement('input');
    mobileNumber.id = "mobile" + currentIndex;
    var deleteIcon = document.createElement("h5");
    deleteIcon.setAttribute('id', currentIndex);
    deleteIcon.innerHTML = '<i class="fa fa-trash"></i>';
    deleteIcon.setAttribute('onclick',"deleteCurrentRow('" + deleteIcon.id + "')");
    var currentCell = currentRow.insertCell(-1);
    currentCell.appendChild(serialNumber);
    currentCell = currentRow.insertCell(-1);
    currentCell.appendChild(relationship);
    currentCell = currentRow.insertCell(-1);
    currentCell.appendChild(contactName);
    currentCell = currentRow.insertCell(-1);
    currentCell.appendChild(mobileNumber);
    currentCell = currentRow.insertCell(-1);
    currentCell.appendChild(deleteIcon);
}

function deleteCurrentRow(deleteButtonId) {
    try{
        document.getElementById('contact-info').deleteRow(deleteButtonId);
    }
    catch(exception){
        console.error("Exception Occurred: " + exception.stack);
    }
    var Table = document.getElementById('contact-info');
    var rows = Table.rows.length;
    deleteButtonId++;
    for(var i = deleteButtonId ; i <= rows ; i++) {
        console.log("Next:"+i);
        var editIdForDeleteButton = document.getElementById(i);
        editIdForDeleteButton.id = parseInt(i) - 1;
        editIdForDeleteButton.setAttribute('onclick',"deleteCurrentRow('" + editIdForDeleteButton.id + "')");

    }
}

function resetRow() {
    var contactTable = document.getElementById('contact-info');
    var totalRow = contactTable.rows.length - 1;
    for (var i = 1 ; i <= totalRow ; i++) {
        try{
            contactTable.deleteRow(i);
        }
        catch(e) {
            resetRow(); //Recursive function is used before rows count changes everytime, so deleted only odd/even rows.
        }
    }
    if(contactTable.rows.length <= 1) {
        addNewRow();
    }
}

function saveTableData() {
    var n,m;
    var tableData = "Relationship,Name,mobile\n";
    var table = document.getElementById('contact-info');
    for (var r = 1, n = table.rows.length; r < n; r++) {
        for (var c = 1, m = table.rows[r].cells.length; c < m - 1; c++) {
            if(c == 1){
                var selectedOptionElement = table.rows[r].cells[c].querySelector("select");
                var optionSelected = selectedOptionElement.options[selectedOptionElement.selectedIndex];
                tableData = tableData + optionSelected.value + ",";
            }    
            else {
                tableData = tableData + table.rows[r].cells[c].firstChild.value + ","; 
            }
        }
        tableData = tableData.slice(0, -1);
        tableData = tableData + "\n";
    }
    tableData = tableData.trim();
    var SplitDataRowWise = tableData.split(/\r\n|\n/);
    var tableHeader = SplitDataRowWise[0].split(",");
    var tableResult =[];

    for (var i = 1; i < SplitDataRowWise.length; i++) {
      var cellValue = SplitDataRowWise[i].split(',');
      var tempObject = {};
      for ( var j=0; j < tableHeader.length; j++ ){
        tempObject[tableHeader[j]] = cellValue[j];
      }
      tableResult.push(tempObject);
    }
   var tableJsonData = JSON.stringify(tableResult, null, 2);
   if(localStorage.getItem('table-data') !== null){
    localStorage.removeItem('table-data');
    }
    localStorage.setItem('table-data', tableJsonData);
}

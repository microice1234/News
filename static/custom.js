$('#datepicker').datepicker({
      uiLibrary: 'bootstrap4'
});

$(document).ready(function(){
    $(".ovrclose").hover(function(){
        $("#panel").slideDown();
    });
});
$(document).ready(function(){
    $("#panel").mouseleave(function(){
        $("#panel").slideUp();
    });
});

$(document).ready(function(){
    $("#panel").click(function(){
        $("#panel").slideUp();
    });
});

jQuery(function($){
    	$( '.menu-btn' ).click(function(){
        $('.responsive-menu').toggleClass('expand')
    })
})


function validation() {

    var firstn = document.getElementById('exampleInputFirstName1').value;
    var lastn = document.getElementById('exampleInputLastName1').value;
    var password = document.getElementById('exampleInputPassword1').value;
    var confpwd = document.getElementById('exampleConfirmPassword1').value;
    var contactNo = document.getElementById('exampleContactNo1').value;
    var emailID = document.getElementById('exampleInputEmail1').value;

    if (firstn == "") {
      document.getElementById('firstNameHelp').innerHTML = " * Enter something";
      return false;
    }

    if (!isNaN(firstn)) {
      document.getElementById('firstNameHelp').innerHTML = " ** only characters allowed";
      return false;
    }

    if (firstn.length <= 2) {
      document.getElementById('firstNameHelp').innerHTML = " *Field size too low";
      return false;
    }

    if (lastn == "") {
      document.getElementById('lastNameHelp').innerHTML = " ** Cannot be empty";
      return false;
    }

    if (!isNaN(lastn)) {
      document.getElementById('lastNameHelp').innerHTML = " ** Only characters allowed";
      return false;
    }

    if (password == "") {
      document.getElementById('passwordHelp').innerHTML = " ** Password field cannot be empty";
      return false;
    }
    if ((password.length <= 8) || (password.length > 20)) {
      document.getElementById('passwordHelp').innerHTML = " ** The password must contain 8-20 characters";
      return false;
    }
    if (password.search(/[a-z]/i) < 0) {
      document.getElementById('passwordHelp').innerHTML = " ** Passwords must contain atleast one character";
      return false;
    }

    if (password.search(/[0-9]/) < 0) {
      document.getElementById('passwordHelp').innerHTML = " ** Passwords must contain atleast one digit";
      return false;
    }

    if (password.search(/[!@#$%^&*]/) < 0) {
      document.getElementById('passwordHelp').innerHTML = " ** Passwords must contain atleast one special character";
      return false;
    }


    if (password != confpwd) {
      document.getElementById('passwordHelp').innerHTML = " ** Password in both fields does not match";
      return false;
    }

    if (confpwd == "") {
      document.getElementById('passwordHelp').innerHTML = " ** Please fill the confirm password field";
      return false;
    }

    if (emailID == "") {
      document.getElementById('emailHelp').innerHTML = " ** Field cannot be empty";
      return false;
    }
    if (emailID.indexOf('@') <= 0) {
      document.getElementById('emailHelp').innerHTML = " ** Entered email ID invalid";
      return false;
    }

    if (emailID.charAt(emailID.length - 4) != '.') {
      document.getElementById('emailHelp').innerHTML = " ** Entered email ID invalid";
      return false;
    }
    if (contactNo == "") {
      document.getElementById('contactNoHelp').innerHTML = " ** Please fill the contact Number field";
      return false;
    }

    if (contactNo.length != 10) {
      document.getElementById('contactNoHelp').innerHTML = " ** Contact Number must contain 10 digits only";
      return false;
    }
}

function resetVal() {
	document.getElementById("myForm").reset();
}

function editEnable(id) {
    var x = document.getElementById(id);
    if (x.contentEditable == "true") {
        x.contentEditable = "false";
    } else {
        x.contentEditable = "true";
        x.focus();
    }
}

function validateProfile() {
    var password = document.getElementById('editPassword').value;

    if (password == "") {
      document.getElementById('passwordHelp1').innerHTML = " ** Password field cannot be empty";
      return false;
    }
    if ((password.length <= 8) || (password.length > 20)) {
      document.getElementById('passwordHelp1').innerHTML = " ** The password must contain 8-20 characters";
      return false;
    }
    if (password.search(/[a-z]/i) < 0) {
      document.getElementById('passwordHelp1').innerHTML = " ** Passwords must contain atleast one character";
      return false;
    }

    if (password.search(/[0-9]/) < 0) {
      document.getElementById('passwordHelp1').innerHTML = " ** Passwords must contain atleast one digit";
      return false;
    }

    if (password.search(/[!@#$%^&*]/) < 0) {
      document.getElementById('passwordHelp1').innerHTML = " ** Passwords must contain atleast one special character";
      return false;
    }
}
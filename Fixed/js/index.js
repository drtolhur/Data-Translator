$('#clear').click(function() {
  var ori_fld = $('#original')
  ori_fld.val('');
  $('#converted').val('').css({'background-color': 'white'});
  ori_fld.css({'background-color': 'white'}).focus();
})

$('#original').keyup(function(event) {
    if (event.keyCode == 13) {
      $('#convert').click();
    }
})

function invalidData(from, data) {
  var con_fld = $('#converted');
  if (from == 'bin' && data.match(/[^0-1*]$/i)) {
    con_fld.val("Invalid binary input").css({'color': 'white', 'background-color': '#d80000'});
    return true;
  } else if (from == 'hex' && data.match(/[^0-9A-Fa-f*]/i)) {
    con_fld.val("Invalid hex input").css({'color': 'white', 'background-color': '#d80000'});
    return true;
  } else if (from == 'dec' && data.match(/[^0-9*]/i)) {
    con_fld.val("Invalid decimal input").css({'color': 'white', 'background-color': '#d80000'});
    return true;
  } else {
    return false;
  }
}

$('#convert').click(function() {
  var ori_fld = $('#original');
  var con_fld = $('#converted');
  var data = $('#original').val();
  var from = $('#from').val();
  var to = $('#to').val();
  
  con_fld.val("").css({'color': 'black', 'background-color': 'white'});
  
  if (data == "" || (ori_fld.val() == "Enter data to convert" && ori_fld.style.backgroundColor == '#FF0')) {
    ori_fld.val("Enter data to convert").css({'background-color': '#FF0'});
    return;
  } else if (invalidData(from, data)) {
    ori_fld.focus();
    return;
  } else if (to == 'inv' && from != 'bin') {
    con_fld.val("Can only invert binary").css({'color': 'white', 'background-color': '#d80000'});
    ori_fld.focus();
    return;
  } else if (from == to) {
    con_fld.val(data);
    ori_fld.focus();
    return;
  }

  if (from == 'bin') {
    if (to == 'hex') {
      data = Number(parseInt(data, 2)).toString(16).toUpperCase();
    } else if (to == 'dec') {
      data = Number(parseInt(data, 2)).toString(10).toUpperCase();
    } else if (to == 'asc') {
      if (Number(parseInt(data, 2)) < 32) {
        con_fld.val("(Non-printable character)");
        ori_fld.focus();
        return;
      } else {
        data = String.fromCharCode(Number(parseInt(data, 2)).toString(10));
      }
    } else if (to == 'inv') {
      data = data.replace(/0/g, 'x');
      data = data.replace(/1/g, '0');
      data = data.replace(/x/g, '1');
    }
  } else if (from == 'hex') {
    if (to == 'bin') {
      data = Number(parseInt(data, 16)).toString(2).toUpperCase();
    } else if (to == 'dec') {
      data = Number(parseInt(data, 16)).toString(10).toUpperCase();
    } else if (to == 'asc') {
      if (Number(parseInt(data, 16)) < 32) {
        con_fld.val("(Non-printable character)");
        ori_fld.focus();
        return;
      } else {
        data = String.fromCharCode(Number(parseInt(data, 16)).toString(10));
      }
    }
  } else if (from == 'dec') {
    if (to == 'bin') {
      data = Number(data).toString(2).toUpperCase();
    } else if (to == 'hex') {
      data = Number(data).toString(16).toUpperCase();
    } else if (to == 'asc') {
      if (data < 32) {
        con_fld.val("(Non-printable character)");
        ori_fld.focus();
        return;
      } else {
        data = String.fromCharCode(data);
      }
    }
  } else if (from == 'asc') {
    var tmp = data;
    data = ""
      
    if (to == 'bin') {
      for (i = 0; i < tmp.length; i++) {
        data = data + tmp.charCodeAt(i).toString(2);
      }
    } else if (to == 'hex') {
      for (i = 0; i < tmp.length; i++) {
        data = data + tmp.charCodeAt(i).toString(16);
      }
    } else if (to == 'dec') {
      for (i = 0; i < tmp.length; i++) {
        data = data + tmp.charCodeAt(i);
      }
    }
  } else {
    con_fld.val("Error").css({'background-color': '#ea8787'});
    ori_fld.focus();
    return;
  }

  con_fld.val(data);
  ori_fld.focus();
})

$('#swap').click(function() {
  var from_sel = $('#from');
  var to_sel   = $('#to');
  var from     = from_sel.val();
  var to       = to_sel.val();

  if (to == 'inv') {
    to = 'bin';
  }

  from_sel.val(to);
  to_sel.val(from);
})
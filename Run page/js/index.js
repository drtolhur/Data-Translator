$('#convert').click(function() {
  var ori_fld  = $('#text');
  var from_sel = $('#from');
  var to_sel   = $('#con');
  var con_fld  = $('#converted');
  var data     = ori_fld.val();
  var from     = from_sel.val();
  var to       = to_sel.val();
  
  if (data == "") {
    ori_fld.val("Enter data to convert").css({'background-color': '#FF0'});
    return;
  }

  if (from == 'bin') {
    if (data.replace(/0/g, '').replace(/1/g, '').length > 0) {
      con_fld.val('Invalid binary input');
      return;
    }

    if (to == 'hex') {
      data = Number(parseInt(data, 2)).toString(16).toUpperCase();
    }

    if (to == 'dec') {
      data = Number(parseInt(data, 2)).toString(10).toUpperCase();
    }

    if (to == 'asc') {
      data = String.fromCharCode(Number(parseInt(data, 2)).toString(10));
    }

    if (to == 'inv') {
      data = data.replace(/0/g, 'x');
      data = data.replace(/1/g, '0');
      data = data.replace(/x/g, '1');
    }
  } else if (from == 'hex') {
    if (to == 'bin') {
      data = Number(parseInt(data, 16)).toString(2).toUpperCase();
    }

    if (to == 'dec') {
      data = Number(parseInt(data, 16)).toString(10).toUpperCase();
    }

    if (to == 'asc') {
      data = String.fromCharCode(Number(parseInt(data, 16)).toString(10));
    }
  } else if (from == 'dec') {
    if (to == 'bin') {
      data = Number(data).toString(2).toUpperCase();
    }

    if (to == 'hex') {
      data = Number(data).toString(16).toUpperCase();
    }

    if (to == 'asc') {
      data = String.fromCharCode(data);
    }
  } else if (from == 'asc') {
    if (to == 'bin') {
      data = data.charCodeAt().toString(2);
    }

    if (to == 'hex') {
      data = data.charCodeAt().toString(16);
    }

    if (to == 'dec') {
      var tmp = data;
      data = ""
      for (i = 0; i < tmp.length; i++) {
        data = data + tmp.charCodeAt(i);
      }
    }
  } else {
    con_fld.val("Error");
    con_fld.css({'background-color': 'red'});
    return;
  }

  con_fld.val(data);
})

$('#swap').click(function() {
  var from_sel = $('#from');
  var to_sel   = $('#con');
  var from     = from_sel.val();
  var to       = to_sel.val();
  var con_fld  = $('#converted');

  from_sel.val(to);
  to_sel.val(from);
  $('#text').val(con_fld.val());
  con_fld.val('');
})

$('#clear').click(function() {
  $('#text').val('');
  $('#converted').val('');
})
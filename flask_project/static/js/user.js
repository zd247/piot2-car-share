$(document).ready(function ($) {
  //TODO change these table header
  var tbl = "";
  tbl += '<table class="table table-hover table-bordered m-auto" id="myTable">';

  tbl += "<thead>";
  tbl += "<tr>";
  for (i of user_header) {
    tbl +=
      "<th class='bg-warning' style='position: sticky; top: 0;'>" + i + "</th>";
  }
  tbl += "<th class='bg-warning' style='position: sticky; top: 0;'></th>";
  tbl += "</tr>";
  tbl += "</thead>";

  tbl += "<tbody>";
  var row_id = -1;

  $.each(user_data, function (index, val) {
    //TODO change all the elements with id and values when apply
    row_id += 1;
    tbl += '<tr row_id="' + row_id + '">';
    for (i of user_key) {
      tbl +=
        '<td ><div class="row_data" col_name="' +
        i +
        '">' +
        val[i] +
        "</div></td>";
    }

    tbl += "<td style='width: 15%'>";

    tbl +=
      '<span class="btn_edit" > <a href="#" class="btn btn-link " row_id="' +
      row_id +
      '" > Edit</a> | </span>';
    tbl +=
      '<span class="btn_delete" > <a href="#" class="btn btn-link " row_id="' +
      row_id +
      '" > Delete</a> | </span>';

    tbl +=
      '<span class="btn_save"> <a href="#" class="btn btn-link"  row_id="' +
      row_id +
      '"> Save</a> | </span>';
    tbl +=
      '<span class="btn_cancel"> <a href="#" class="btn btn-link" row_id="' +
      row_id +
      '"> Cancel</a> | </span>';

    tbl += "</td>";

    tbl += "</tr>";
  });

  tbl += "</tbody>";

  tbl += "<tfoot>";
  tbl += "<tr>";
  for (i of user_header) {
    tbl +=
      "<th>" + i + "</th>";
  }
  tbl += "</tr>";
  tbl += "</tfoot>";

  tbl += "</table>";

  $(document).find(".tbl_user_data").html(tbl);
  $(document).on("click", ".btn_save_all", function (event) {
    event.preventDefault();
    $.post("/admin/user", { user_data: JSON.stringify(user_data) });
    location.reload(false);
  });

  $(document).on("click", ".btn_add", function (event) {
    event.preventDefault();
    row_id += 1;

    temp = {};
    new_row = "";
    new_row += '<tr row_id="' + row_id + '">';

    for (i of user_key) {
      temp[i] = "";
      new_row +=
        '<td ><div class="row_data" col_name="' +
        i +
        '">' +
        temp[i] +
        "</div></td>";
    }
    new_row += "<td style='width: 15%'>";

    new_row +=
      '<span class="btn_edit" > <a href="#" class="btn btn-link " row_id="' +
      row_id +
      '" > Edit</a> | </span>';
    new_row +=
      '<span class="btn_delete" > <a href="#" class="btn btn-link " row_id="' +
      row_id +
      '" > Delete</a> | </span>';

    new_row +=
      '<span class="btn_save"> <a href="#" class="btn btn-link"  row_id="' +
      row_id +
      '"> Save</a> | </span>';
    new_row +=
      '<span class="btn_cancel"> <a href="#" class="btn btn-link" row_id="' +
      row_id +
      '"> Cancel</a> | </span>';

    new_row += "</td>";

    new_row += "</tr>";
    $("#myTable > tbody:last-child").append("<tr>" + new_row + "</tr>");
    $(document).find(".btn_save").hide();
    $(document).find(".btn_cancel").hide();
    user_data.push(temp);
  });

  $(document).find(".btn_save").hide();
  $(document).find(".btn_cancel").hide();

  $(document).on("click", ".btn_edit", function (event) {
    event.preventDefault();
    var tbl_row = $(this).closest("tr");

    var row_id = tbl_row.attr("row_id");

    tbl_row.find(".btn_save").show();
    tbl_row.find(".btn_cancel").show();

    $(".btn_save_all").hide();
    $(".btn_add").hide();
    tbl_row.find(".btn_edit").hide();
    tbl_row.find(".btn_delete").hide();

    tbl_row
      .find(".row_data")
      .attr("contenteditable", "true")
      .attr("edit_type", "button")
      .addClass("bg-warning")
      .css("padding", "3px");

    tbl_row.find(".row_data").each(function (index, val) {
      $(this).attr("original_entry", $(this).html());
    });
  });

  $(document).on("click", ".btn_delete", function (event) {
    event.preventDefault();
    var tbl_row = $(this).closest("tr").remove();

    var row_id = tbl_row.attr("row_id");

    user_data.pop(row_id);
    console.log(user_data);
  });

  $(document).on("click", ".btn_cancel", function (event) {
    event.preventDefault();

    var tbl_row = $(this).closest("tr");

    var row_id = tbl_row.attr("row_id");

    tbl_row.find(".btn_save").hide();
    tbl_row.find(".btn_cancel").hide();

    $(".btn_save_all").show();
    $(".btn_add").show();
    tbl_row.find(".btn_edit").show();
    tbl_row.find(".btn_delete").show();

    tbl_row
      .find(".row_data")
      .attr("edit_type", "click")
      .removeClass("bg-warning")
      .css("padding", "");

    tbl_row.find(".row_data").each(function (index, val) {
      $(this).html($(this).attr("original_entry"));
    });
  });

  $(document).on("click", ".btn_save", function (event) {
    event.preventDefault();
    var tbl_row = $(this).closest("tr");

    var row_id = tbl_row.attr("row_id");

    tbl_row.find(".btn_save").hide();
    tbl_row.find(".btn_cancel").hide();

    $(".btn_save_all").show();
    $(".btn_add").show();
    tbl_row.find(".btn_edit").show();
    tbl_row.find(".btn_delete").show();

    tbl_row
      .find(".row_data")
      .attr("edit_type", "click")
      .removeClass("bg-warning")
      .css("padding", "");

    var arr = {};
    tbl_row.find(".row_data").each(function (index, val) {
      var col_name = $(this).attr("col_name");
      var col_val = $(this).html();
      arr[col_name] = col_val;
    });

    $.extend(arr, { row_id: row_id });

    user_data[row_id] = arr;
  });
});

$(document).ready(function () {
  $("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    
    $(".tbl_user_data tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

var index = 0;
$(document).ready(function () {
  $("#myTable tfoot th").each(function () {
    var title = $("#myTable thead th").eq($(this).index()).text();
    $(this).html(
      '<input type="text" size="15" id="input_' +
        index +
        '" onkeyup="myFunction(' +
        index +
        ')" placeholder="Search ' +
        title.toLowerCase() +
        '" />'
    );
    index++;
  });
});

function myFunction(index) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("input_" + index.toString());
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  console.log(filter);

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[index];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
$(document).ready(function () {
  $("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#myTable tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

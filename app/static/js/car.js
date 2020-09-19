$(document).ready(function ($) {
  //TODO change these table header
  var tbl = "";
  tbl += '<table class="table table-hover" id="my_table">';

  tbl += "<thead>";
  tbl += "<tr>";
  for (i of car_header) {
    tbl +=
      "<th class='bg-warning' style='position: sticky; top: 0;'>" + i + "</th>";
  }
  tbl += "<th class='bg-warning' style='position: sticky; top: 0;'></th>";
  tbl += "</tr>";
  tbl += "</thead>";

  tbl += "<tbody>";
  var row_id = -1;

  $.each(car_data, function (index, val) {
    //TODO change all the elements with id and values when apply
    row_id += 1;
    tbl += '<tr row_id="' + row_id + '">';
    for (i of car_key) {
      tbl +=
        '<td ><div class="row_data" col_name="' +
        i +
        '">' +
        val[i] +
        "</div></td>";
    }

    tbl += "<td style='width: 15%'>";

    tbl +=
      '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal" class"open_form">' +
      '<i class="fas fa-flag"></i></button>';
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

  tbl += "</table>";

  $(document).find(".tbl_car_data").html(tbl);
  $(document).on("click", ".btn_save_all", function (event) {
    event.preventDefault();
    $.post("/admin/car", { car_data: JSON.stringify(car_data) });
    location.reload(false);
  });

  $(document).on("click", "#submit_button", function (event) {
    report_message = $("#report_area").val();
    if (report_message != "") alert(report_message);
  });

  $(document).on("click", ".btn_add", function (event) {
    event.preventDefault();
    row_id += 1;

    temp = {};
    car_data.push(temp);
    new_row = "";
    new_row += '<tr row_id="' + row_id + '">';

    for (i of car_key) {
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
      '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal" class"open_form">' +
      '<i class="fas fa-flag"></i></button>';
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
    $("#my_table > tbody:last-child").append("<tr>" + new_row + "</tr>");
    $(document).find(".btn_save").hide();
    $(document).find(".btn_cancel").hide();
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

    car_data.pop(row_id);
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

    car_data[row_id] = arr;
  });
});

$(document).ready(function () {
  $("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".tbl_car_data tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

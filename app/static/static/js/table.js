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

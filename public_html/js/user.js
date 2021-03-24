
async function load(id){
  var r=await fetch("/api/accesses");
  var accesses=await r.json();
  $('#access_id').append('<option value="-1"></option>');
  for(var i in accesses){
    $('#access_id').append('<option value="' + accesses[i][0] + '">' + accesses[i][1] + '</option>');
  }

  var r=await fetch("/api/user/" + id);
  var json=await r.json();
console.log(json);

  $('#email').val(json["email"]);
  $('#name').val(json["Name"]);
  $('#access_id').val(json["access_id"]);

}

const params = new URLSearchParams(window.location.search);
load(params.get("id"));


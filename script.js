function onSubmit() {
  var source = document.getElementById('sourceInput').value
  var dest = document.getElementById('destInput').value

  console.log(source)
  console.log(dest)
  var dataDisplay = document.getElementById('data-display')

  $.get("http://127.0.0.1:5000/?source=" + source + "&dest=" + dest, function (data) {
    $(".result").html(data)
    console.log(data)
    var dataHeader = document.getElementById('data-display-header')
    dataHeader.innerHTML = "Routes from " + source + " to " + dest

    var dataDisplay = document.getElementById('data-display')
    dataDisplay.innerHTML =  " "

    for (var x = 0; x < data.length; x++) {


      dataDisplay.innerHTML = dataDisplay.innerHTML + `<div class="col-6 route">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Route ${x + 1}</h5>
          <p class="card-text">
            <ul class="list-group">
              <li class="list-group-item">Time: ${data[x].time}</li>
              <li class="list-group-item">Distance: ${data[x].distance}</li>
              <li class="list-group-item">Route: ${data[x].route}</li>
              <!-- <li class="list-group-item">Description: ${data[x].description}</li>-->

            </ul>
          </p>
        </div>
      </div>
    </div>`
    }

  });

  function newFunction() {
    return "span";
  }
}

document.forms[0].addEventListener('submit', function(e){
  //e.preventDefault();
  data = {
    username: document.querySelector('input.username').value,
    password: document.querySelector('input.password').value
  }
  e.preventDefault();
  fetch('/login',{
    method: 'POST',
    //body: JSON.stringify(data),
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(
    res=>res.json()).then(
      d=>{
        if (d.status === 401){
          alert("Something went wrong");
        }
        else if(d.status === 201){
          location.href = "/dashboard"
        }
     })
})
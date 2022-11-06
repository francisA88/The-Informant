
const form = document.forms[0];
form.addEventListener('submit', function(e){
  const data = {
    fullname: document.querySelector('input.fullname').value,
    username: document.querySelector("input.username").value,
    email: document.querySelector('input.email').value,
    password: document.querySelector('input.password').value
  };
  e.preventDefault();
  fetch('/signup',{
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
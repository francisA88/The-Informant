document.forms[0].addEventListener('submit', function(e){
  e.preventDefault();
  data = {
    title: this.children[0].value,
    content: this.children[1].value
  }
  fetch(this.action, {
    method: "POST",
    header: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(res=>res.json()).then(data=>{
    if (data.status === 201){
      location.href = "/dashboard"
    }
    else{
      alert('something went wrong')
    }
  })
})
document.forms[0].addEventListener('submit', function(e){
  e.preventDefault();
  data = {
    title: document.querySelector('input.title').value,
    content: document.querySelector('#content').value
  }
 /* alert(data.title)
  alert(data.content)*/
  fetch(this.action, {
    method: "POST",
    headers: {
    	'Content-Type': 'application/json'
    	},
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
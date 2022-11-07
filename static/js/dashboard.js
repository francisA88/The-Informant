const delBtn = document.querySelectorAll(".delete");
delBtn.forEach((el)=>{
  el.addEventListener('click', function(e){
    //e.preventDefault();
    fetch(`/blogs/${el.dataset.id}/delete`, {
      method: "DELETE"
    }).then(res=>{
      if (res.status == 200){
        location.reload()
      }
      else{ alert('something went wrong'); }
    })
  })
}
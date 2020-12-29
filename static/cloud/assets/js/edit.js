var g = document.getElementById('row');
                
for (var i = 0, len = g.children.length; i < len; i++){
    (function(index){
        var span = g.getElementsByClassName('rename')[i]
        span.onclick = function(){
            var edit = g.getElementsByClassName('edit')[index]
            if (edit.style.display == "none"){
                edit.style.display = "inline-block";
                span.classList.remove("fa-pen-square");
                span.classList.add("fa-window-close");
            }else{
                edit.style.display = "none";
                span.classList.add("fa-pen-square");
                span.classList.remove("fa-window-close");
            }

        }    
    })(i);
}
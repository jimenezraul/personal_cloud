function search(){
    var input, filter, i, txtValue, h5;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    const elementsList = document.querySelectorAll("#block, #row");
    const elementsArray = [...elementsList];
    var colums = elementsArray[0];
    var colums2 = elementsArray[1];
    var folders = colums.querySelectorAll(".folder");
    var files = colums2.querySelectorAll(".files");
    var div = colums.getElementsByTagName("h5");
    var div2 = colums2.getElementsByTagName("p");
    for (i = 0; i < div.length; i++) {
        h5 = div[i].getElementsByTagName("strong")[0];
        txtValue = h5.innerText;
        
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            folders[i].style.display = "";
        } else {
            folders[i].style.display = "none";
        }
    }
    for (i = 0; i < div2.length; i++) {
        h5 = div2[i].getElementsByTagName("strong")[0];
        txtValue = h5.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            files[i].style.display = "";
        } else {
            files[i].style.display = "none";
        } 
    }
    
}
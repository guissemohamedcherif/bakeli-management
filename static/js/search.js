const searchField = document.querySelector("#searchTxt");
searchField.addEventListener("keyup",(e)=> {
const searchValue = e.target.value;

if(searchValue.length > 0){
    console.log("searchValue",searchValue)
}
});
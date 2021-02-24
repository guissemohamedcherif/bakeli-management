const searchField = document.querySelector("#searchTxt");
const appTable = document.querySelector(".app-table");
const tableOutput= document.querySelector(".table-output");
tableOutput.style.display = "none";
const tbody = document.querySelector(".table-body")

searchField.addEventListener("keyup",(e)=> {
const searchValue = e.target.value;

if(searchValue.trim().length > 0){
    console.log("searchValue",searchValue)

    fetch("searchDept", {
        body: JSON.stringify({searchT : searchValue}),
        method: "POST",
    })
    .then((res) =>res.json())
    .then((data) => {
        console.log("data",data);
        tableOutput.style.display = "block";
        appTable.style.display = "none";

        if (data.length === 0){

            tableOutput.innerHTML = "No results found ";

        }else{

            data.forEach(item=>{

                tbody.innerHTML=+`
            
                <tr>
                <td>${item.code}</td>
                <td>${item.nom}</td>
                <td>${item.statut}</td>
                </tr> `;

            })


        }
    });
    }
    else{
    appTable.style.display = "block";
    }
});
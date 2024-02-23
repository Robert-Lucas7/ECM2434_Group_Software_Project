//On page load - get the entry data from the template
const data = JSON.parse(
    document.currentScript.nextElementSibling.textContent
);

function changeDataDisplayed(pageNumber){
    let contentDiv = document.getElementById("table-contents");
    while(contentDiv.lastElementChild){ //Remove all children of the contentDiv (clear the table)
        contentDiv.removeChild(contentDiv.lastChild);
    }
    for(let i=0;i<data[pageNumber].length;i++){
        let row = document.createElement('div');
        // Styling (specifically background colour) of the rows
        let positionStyle = "leaderboard-other"
        if(pageNumber == 0){
            if(i == 0){
                positionStyle = "leaderboard-first";
            } else if(i == 1){
                positionStyle = "leaderboard-second";
            } else if(i == 2){
                positionStyle = "leaderboard-third"
            } 
        }
        row.className = `row rounded-pill my-2 p-3 leaderboard ${positionStyle}`;
        // Populate row with the data needed.
        let col = document.createElement("div");
        col.className = "col";
        col.innerHTML = data[pageNumber][i]["username"];
        row.appendChild(col);
        let col2 = document.createElement('div')
        col2.className = "col";
        col2.innerHTML = data[pageNumber][i]["metric"];
        row.appendChild(col2);
        contentDiv.append(row);
    }
}

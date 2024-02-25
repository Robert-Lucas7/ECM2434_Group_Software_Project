// If the points button is clicked and the time period options are not displayed, display them.
$('#points_button').on("click", function(evt) {
    evt.preventDefault(); //Stop it activating twice
    console.log($('#points_button').attr("aria-expanded"));
    if( $('#points_button').attr("aria-expanded") == "false" ){
        $('.collapse').collapse('show');
        $('#points_button').attr("aria-expanded", "true");
    }
    sortData("points");
});
// If the streak button is clicked and the time period options are displayed, hide them.
$('#streak_button').on("click", function(evt){
    evt.preventDefault();
    if( $('#points_button').attr("aria-expanded") == "true" ){
        $('.collapse').collapse('hide');
        $('#points_button').attr("aria-expanded", "false");
    }
    sortData("streak");
});

//On page load - get the user and points data from the script tag.
let data = JSON.parse(
    document.currentScript.nextElementSibling.textContent
);
const entriesPerPage = 5;
let currentlySortedBy = "streak"; //What the data is sorted by
// Quicksort implementation from: https://www.freecodecamp.org/news/how-to-write-quick-sort-algorithm-with-javascript/
function quickSort(arr, metricToSort){ 
    if(arr.length <= 1){
        return arr;
    }
    let pivot = arr[0];
    let leftArr = [];
    let rightArr = [];
    for(let i=1;i<arr.length;i++){
        if(arr[i][metricToSort] > pivot[metricToSort]){
            leftArr.push(arr[i]);
        } else{
            rightArr.push(arr[i]);
        }
    }
    return [...quickSort(leftArr, metricToSort), pivot, ...quickSort(rightArr, metricToSort)];
}
// If the data is not already sorted by the 'metricToSort', sort the data, update the table headings, and change the data displayed in the table.
function sortData(metricToSort){
    if(currentlySortedBy != metricToSort){ //Don't perform unnecessary sorting (already sorted by the chosen metric).
        currentlySortedBy = metricToSort;
        data = quickSort(data, metricToSort);
        let new_heading = metricToSort.charAt(0).toUpperCase() + metricToSort.slice(1);
        document.getElementById('table_heading').innerHTML = `${new_heading}`;
        changeDataDisplayed(0, metricToSort);
    }
}
// Load the page specified entries into the table.
function changeDataDisplayed(pageNumber){
    let contentDiv = document.getElementById("table-contents");
    while(contentDiv.lastElementChild){ //Remove all children of the contentDiv (clear the table)
        contentDiv.removeChild(contentDiv.lastChild);
    }
    let i = 0;
    while( entriesPerPage > i && pageNumber * entriesPerPage + i < data.length){
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
        col.innerHTML = data[pageNumber * entriesPerPage + i]["username"];
        row.appendChild(col);
        let col2 = document.createElement('div')
        col2.className = "col";
        col2.innerHTML = data[pageNumber * entriesPerPage + i][currentlySortedBy];
        row.appendChild(col2);
        contentDiv.append(row);
        i += 1;
    }
}

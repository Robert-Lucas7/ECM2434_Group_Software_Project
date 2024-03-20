
//On page load - get the user and points data from the script tag.
let data = JSON.parse(
    document.currentScript.nextElementSibling.textContent
);
const challengesData = JSON.parse(document.getElementById('user_challenges_completed').textContent);
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
function getUserPosition(metricToSort){
    let position = 0;
    let count = 0;
    while( data[count].username != challengesData.username ){ //The logged in user will be in the data int some position so iterate until you find it.
        if( data[count][metricToSort] != data[count + 1][metricToSort] ){
            position += 1;
        }
        count += 1;
    }
    return position + 1;
}
function updateCardsDisplayed(metricToSort){
    //Update the 'challenges completed' card displayed at the top of the page.
    let num_challenges = challengesData["challenges_completed"];
    $('#challenges_completed_text').html(`Challenges Completed: ${num_challenges}`);
    //Update the position card displayed at the top of the page.
    let user_position = getUserPosition(metricToSort);
    $('#position_text').html(`Your Position: ${user_position}`);

}
// If the data is not already sorted by the 'metricToSort', sort the data, update the table headings, and change the data displayed in the table.
function sortData(metricToSort){
    if(currentlySortedBy != metricToSort){ //Don't perform unnecessary sorting (already sorted by the chosen metric).
        currentlySortedBy = metricToSort;
        data = quickSort(data, metricToSort);
        let new_heading = metricToSort.charAt(0).toUpperCase() + metricToSort.slice(1);
        document.getElementById('table_heading').innerHTML = `${new_heading}`;
        updateCardsDisplayed(metricToSort);
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
        let username = data[pageNumber * entriesPerPage + i]["username"];
        let aTag = document.createElement('a');
        aTag.className = "link";
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
        col.innerHTML = username;
        row.appendChild(col);
        let col2 = document.createElement('div')
        col2.className = "col";
        col2.innerHTML = data[pageNumber * entriesPerPage + i][currentlySortedBy];
        row.appendChild(col2);
        aTag.appendChild(row);
        contentDiv.append(aTag);
        i += 1;
    }
}

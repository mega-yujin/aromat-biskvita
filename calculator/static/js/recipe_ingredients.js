// adding ingredients to list

var tableQuantity = document.getElementsByClassName("quantity");
var tableComponents = document.getElementsByClassName("component");
var tableUnits = document.getElementsByClassName("units");
var addButton = document.getElementById("add");
// var clearButton = document.getElementById("clear");

addButton.onclick = addToList; // добавить ингридиенты в скписок


function addToList() {
    if (localStorage.getItem("list")) {
        var list = new Map(JSON.parse(localStorage.getItem("list")));
        getItems(list);
    }
    else {
        var list = new Map();
        getItems(list);
    }
}


function getItems(listMap) {
    for (var i = 0, len = tableComponents.length; i < len; i++) {
        var component = tableComponents[i].innerHTML;
        var quantity = tableQuantity[i].innerHTML;
        var units = tableUnits[i].innerHTML;
        var key = tableComponents[i].innerHTML + `(${units})`;

        if (listMap.get(key)) {
            var storedQauntity = parseFloat(listMap.get(key)[1], 10);
            var newQuantity = parseFloat((quantity), 10);
            listMap.set(key, [component, (storedQauntity + newQuantity), units]);
        }
        else {
            listMap.set(component + `(${units})`, [component, quantity, units]);
        }
    }

    var jsonlist = JSON.stringify([...listMap]);
    localStorage.setItem("list", jsonlist);
}

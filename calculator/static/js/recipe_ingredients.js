var tableQuantity = document.getElementsByClassName("quantity");
var tableComponents = document.getElementsByClassName("component");
var add = document.getElementById("add");
var clear = document.getElementById("clear");

add.onclick = addToList; // добавить ингридиенты в скписок
clear.onclick = clearList; // очистить список


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
    // var list = new Map();

    for (var i = 0, len = tableComponents.length; i < len; i++) {
        var component = tableComponents[i].innerHTML;
        var quantity = tableQuantity[i].innerHTML;

        if (listMap.get(component)) {
            var storedQauntity = parseFloat(listMap.get(component), 10);
            var newQuantity = parseFloat((quantity), 10);
            listMap.set(component, storedQauntity+newQuantity);
        }
        else {
            listMap.set(component, quantity);
        }

        var jsonlist = JSON.stringify([...listMap]);
    }

    localStorage.setItem("list", jsonlist);
}


function clearList() {
    console.log("GHGJHGJHGJH");
    localStorage.removeItem("list");
    document.getElementById("listTable").hidden = true;
}
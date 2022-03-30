// show shopping list

window.onload = init;
var header = document.getElementById("header"); // заголовок
var subHeader = document.getElementById("sub-header"); // подзаголовок
var clearButton = document.getElementById("clear"); // кнопка


function init() {
	clearButton.onclick = clearList; // очистить список

	if (localStorage.getItem("list")) {
		document.getElementById("listTable").hidden = false;
		var list = new Map(JSON.parse(localStorage.getItem("list")));

		let tbody = document.getElementById("listBody");
		list.forEach(function(value, key) {
			let row = document.createElement('tr');
			let component = document.createElement('td');
			let quantity = document.createElement('td');

			component.innerHTML = value[0];
			quantity.innerHTML = value[1] + ` ${value[2]}`;

			tbody.appendChild(row);
			row.appendChild(component);
			row.appendChild(quantity);
		})
	}
	else {
		header.innerHTML = "Список пуст";
		subHeader.innerHTML = "Нужно что-нибудь добавить";
		clearButton.hidden = true;
	}
}


function clearList() {
    localStorage.removeItem("list");
    document.getElementById("listTable").hidden = true;
    header.innerHTML = "Список пуст";
    subHeader.innerHTML = "Нужно что-нибудь добавить";
    clearButton.hidden = true;
}
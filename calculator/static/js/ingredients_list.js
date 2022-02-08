window.onload = init;


function init() {
	var clear = document.getElementById("clear");
	clear.onclick = clearList; // очистить список

	if (localStorage.getItem("list")) {
		var list = new Map(JSON.parse(localStorage.getItem("list")));

		let tbody = document.getElementById("listBody");
		list.forEach(function(value, key, map) {
			let row = document.createElement('tr');
			let component = document.createElement('td');
			let quantity = document.createElement('td');
			component.innerHTML = key;
			quantity.innerHTML = value;

			tbody.appendChild(row);
			row.appendChild(component);
			row.appendChild(quantity);
		})
	}
	else {
		console.log("nothing here");
	}
}


function clearList() {
    console.log("GHGJHGJHGJH");
    localStorage.removeItem("list");
    document.getElementById("listTable").hidden = true;
}
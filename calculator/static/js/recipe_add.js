// add ingredients form

window.onload = init;

var formSelector = document.getElementById("id_form")
var diameter = document.getElementById("id_diameter")
var length = document.getElementById("id_length")
var width = document.getElementById("id_width")

function init() {
    formSelect(); // скрыть ненужные поля ввода
    formSelector.addEventListener('change', formSelect); // скрыть ненужные поля ввода при выборе формы
}

function formSelect() {
    var index = formSelector.selectedIndex;
    switch (index) {
        case 0: // круг
            diameter.parentElement.parentElement.hidden = false;
            length.parentElement.parentElement.hidden = true;
            width.parentElement.parentElement.hidden = true;
            break;
        case 1: // квадрат
            diameter.parentElement.parentElement.hidden = true;
            length.parentElement.parentElement.hidden = false;
            width.parentElement.parentElement.hidden = true;
            break;
        case 2: // прямоугольник
            diameter.parentElement.parentElement.hidden = true;
            length.parentElement.parentElement.hidden = false;
            width.parentElement.parentElement.hidden = false;
            break;
    }
}
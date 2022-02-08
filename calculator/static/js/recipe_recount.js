window.onload = init;

var ingredients; // таблица ингридиентов
var initialForm; // исходная форма тортика
var initialParams; // исходная площадь
var initialWeight; // исходный вес
var initialDiameter; // исходный диаметр круглого торта
var initialLength; // исходная длина стороны для квадрата или прямоугольника
var initialWidth; // исходная ширина примоугольника
var initialHeight; // исходная высота
var ingredientsQuantity = []; // количество ингридиентов

var formSelector; // селектор выбора формы торта
// var weightField;
// var diameterField;
// var lengthField;
// var widthField;
// var heightField;

function init() {
    fillVariables(); // инициализировать переменные начальными значениями
    formSelect(); // скрыть ненужные поля ввода

    var recountButton = document.getElementById("recount");
    var resetButton = document.getElementById("reset");

    recountButton.onclick = calculate; // перечсет ингридиентов по клику
    resetButton.onclick = reset; // сброс на начальные значения

    formSelector.addEventListener('change', formSelect); // скрыть ненужные поля ввода при выборе формы
}


function fillVariables () {

    ingredients = document.getElementsByClassName("quantity");
    formSelector = document.getElementById("form");
    weightField = document.getElementById("weight");
    heightField = document.getElementById("height");
    diameterField = document.getElementById("diameter");
    lengthField = document.getElementById("length");
    widthField = document.getElementById("weight");


    initialForm = formSelector.value;
    initialWeight = parseFloat(document.getElementById("weight").value, 10);
    initialHeight = parseFloat(document.getElementById("height").value, 10);

    switch (initialForm) {
        case "c":
            initialDiameter = parseInt(document.getElementById("diameter").value, 10);
            if (initialHeight) {
                initialParams = ((Math.PI * Math.pow(initialDiameter, 2)) / 4) * initialHeight;
            }
            else {
                initialParams = (Math.PI * Math.pow(initialDiameter, 2)) / 4;
            }
            break;

        case "s":
            initialLength = parseInt(document.getElementById("length").value, 10);
            if (initialHeight) {
                initialParams = Math.pow(initialLength, 2) * initialHeight;
            }
            else {
                initialParams = Math.pow(initialLength, 2);
            }
            break;

        case "r":
            initialLength = parseInt(document.getElementById("length").value, 10);
            initialWidth = parseInt(document.getElementById("width").value, 10);
            if (initialHeight) {
                initialParams = initialLength * initialWidth * initialHeight;
            }
            else {
                initialParams = initialLength * initialWidth;
            }
            break;
    }


    for (var i = 0, len = ingredients.length; i < len; i++) {
        var ingredient = parseFloat(ingredients[i].innerHTML, 10);
        ingredientsQuantity.push(ingredient);
    }

    console.log("Initial form: " + initialForm);
    console.log("Initial area: " + initialParams);
}

function calculate() {
    if (initialHeight) {
        console.log("Volume");
        var newParams = volumeCalc();
    }
    else {
        console.log("Area");
        var newParams = areaCalc();
    }
    var vRatio = ratio(initialParams, newParams);
    recount(vRatio);
}


function areaCalc() {
    var newForm = document.getElementById("form").value

    switch (newForm) {
        case "c":
            newDiameter = parseInt(document.getElementById("diameter").value, 10);
            return (Math.PI * Math.pow(newDiameter, 2)) / 4;

        case "s":
            newLength = parseInt(document.getElementById("length").value, 10);
            return Math.pow(newLength, 2);

        case "r":
            newLength = parseInt(document.getElementById("length").value, 10);
            newWidth = parseInt(document.getElementById("width").value, 10);
            return newLength * newWidth;
    }
}

function volumeCalc() {
    var newForm = document.getElementById("form").value
    var newHeight = parseFloat(document.getElementById("height").value, 10);

    switch (newForm) {
        case "c":
            newDiameter = parseInt(document.getElementById("diameter").value, 10);
            return ((Math.PI * Math.pow(newDiameter, 2)) / 4) * newHeight;

        case "s":
            newLength = parseInt(document.getElementById("length").value, 10);
            return Math.pow(newLength, 2) * newHeight;

        case "r":
            newLength = parseInt(document.getElementById("length").value, 10);
            newWidth = parseInt(document.getElementById("width").value, 10);
            return newLength * newWidth * newHeight;
    }
}


function ratio(initialParams, newParams) {
    return newParams / initialParams; //вычисление коэффициента пересчета
}

function recount(ratio) {               // вычисление необходимого количества ингридиентов
    console.log("Ratio: " + ratio);
    for (var i = 0, len = ingredients.length; i < len; i++) {
        var value = ingredientsQuantity[i] * ratio;
        ingredients[i].innerHTML = value.toFixed(1);
    }
    document.getElementById("weight").value = (initialWeight * ratio).toFixed(1); // новый вес тортика
}

function reset() {
    for (var i = 0, len = ingredients.length; i < len; i++) {
        ingredients[i].innerHTML = ingredientsQuantity[i];
    }

    document.getElementById("weight").value = initialWeight;
    document.getElementById("height").value = initialHeight;
    document.getElementById("diameter").value = initialDiameter;
    document.getElementById("length").value = initialLength;
    document.getElementById("width").value = initialWidth;
    document.getElementById("form").value = initialForm;

    formSelect();
}

function formSelect() {
    var index = formSelector.selectedIndex;
    switch (index) {
        case 0: // круг
            document.getElementById("diameter_field").hidden = false;
            document.getElementById("length_field").hidden = true;
            document.getElementById("width_field").hidden = true;
            break;
        case 1: // квадрат
            document.getElementById("diameter_field").hidden = true;
            document.getElementById("length_field").hidden = false;
            document.getElementById("width_field").hidden = true;
            break;
        case 2: // прямоугольник
            document.getElementById("diameter_field").hidden = true;
            document.getElementById("length_field").hidden = false;
            document.getElementById("width_field").hidden = false;
            break;
    }
}
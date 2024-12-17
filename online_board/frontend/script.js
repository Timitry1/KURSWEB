const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

let drawing = false;

// Подключение к WebSocket
const socket = new WebSocket("ws://" + window.location.host + "/ws");

// Начало рисования
canvas.addEventListener("mousedown", () => (drawing = true));
canvas.addEventListener("mouseup", () => (drawing = false));
canvas.addEventListener("mousemove", draw);

// Локальное рисование
function draw(event) {
    if (!drawing) return;
    const x = event.offsetX;
    const y = event.offsetY;

    ctx.lineTo(x, y);
    ctx.stroke();

    // Отправка координат на сервер
    const data = { x, y };
    socket.send(JSON.stringify(data));
}

// Получение данных от других клиентов
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    ctx.lineTo(data.x, data.y);
    ctx.stroke();
};

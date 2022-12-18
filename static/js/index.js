const lamp = document.getElementById("lamp");
const form = document.getElementById("form");
const ws = new WebSocket("ws://localhost:9999/ws_self?websocket=true");

function numberToColor(number) {
  const hex = number.toString(16).padStart(6, "0");
  return "#" + hex;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = {
    command: command.value,
    metadata: metadata.value,
  };
  ws.send(JSON.stringify(data));
});

ws.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  if (data.is_on) {
    document.body.classList.add("on");
    document
      .querySelector(":root")
      .style.setProperty("--bulb-color", numberToColor(data.color));
  } else {
    document.body.classList.remove("on");
  }
});

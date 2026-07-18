// =========================
// Live Clock
// =========================

function updateClock() {

    const now = new Date();

    const time = now.toLocaleTimeString();

    const clock = document.getElementById("clock");

    if (clock) {
        clock.innerHTML = time;
    }
}

setInterval(updateClock, 1000);

updateClock();


// =========================
// Demo Switch
// =========================

function changeDemo() {

    const demo = document.getElementById("demo").value;

    fetch("/change_demo/" + demo)
    .then(response => response.text())
    .then(() => {

        // Reload MJPEG stream
        document.getElementById("video").src =
            "/video?" + new Date().getTime();

    });

}
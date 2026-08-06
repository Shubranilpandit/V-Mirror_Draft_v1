const webcam = document.getElementById("webcam");
const outputFrame = document.getElementById("outputFrame");
const clothButtons = document.getElementById("clothButtons");
const captureBtn = document.getElementById("captureBtn");
const gallery = document.getElementById("gallery");

let selectedCloth = "shirt1";

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        webcam.srcObject = stream;
        await webcam.play();

    } catch (error) {
        console.error(error);
        alert("Camera access denied.");
    }
}

async function loadClothes() {
    try {
        const response = await fetch("/clothes");
        const data = await response.json();

        clothButtons.innerHTML = "";

        data.items.forEach(item => {
            const btn = document.createElement("button");
            btn.innerText = item.label;
            btn.className = "cloth-btn";

            btn.onclick = () => {
                selectedCloth = item.id;

                document.querySelectorAll(".cloth-btn")
                    .forEach(b => b.classList.remove("active"));

                btn.classList.add("active");
            };

            clothButtons.appendChild(btn);
        });

    } catch (error) {
        console.error(error);
    }
}

async function processFrame() {
    if (!webcam.videoWidth || !webcam.videoHeight) return;

    try {
        const canvas = document.createElement("canvas");
        canvas.width = webcam.videoWidth;
        canvas.height = webcam.videoHeight;

        const ctx = canvas.getContext("2d");

        // NO MIRRORING HERE
        ctx.drawImage(webcam, 0, 0);

        const frameData = canvas.toDataURL("image/jpeg");

        const response = await fetch("/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                frame: frameData,
                cloth: selectedCloth
            })
        });

        const result = await response.json();

        if (result.frame) {
            outputFrame.src = result.frame;
        }

    } catch (error) {
        console.error(error);
    }
}

captureBtn.addEventListener("click", () => {
    if (!outputFrame.src) return;

    const img = document.createElement("img");
    img.src = outputFrame.src;
    img.className = "saved-image";

    gallery.appendChild(img);
});

async function init() {
    await startCamera();
    await loadClothes();

    setInterval(processFrame, 500);
}

init();
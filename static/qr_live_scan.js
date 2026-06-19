document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("videoElement");
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    const resultBox = document.getElementById("result");

    let scanning = true;
    let streamRef = null;

    async function startCamera() {
        streamRef = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        video.srcObject = streamRef;
        video.play();

        scanLoop();
    }

    async function scanLoop() {
        if (!scanning) return;

        canvas.width = video.videoWidth || 400;
        canvas.height = video.videoHeight || 400;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL("image/png");

        const formData = new FormData();
        formData.append("image", imageData);

        const response = await fetch("/api/scan-live/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.found) {
            scanning = false;

            resultBox.innerText = "QR: " + data.data;

            stopCamera();

            return;
        }

        setTimeout(scanLoop, 500);
    }

    function stopCamera() {
        if (streamRef) {
            streamRef.getTracks().forEach(track => track.stop());
        }
    }

    startCamera();
});
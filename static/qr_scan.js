document.addEventListener("DOMContentLoaded", () => {
    const video = document.querySelector("#videoElement");
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    const captureBtn = document.getElementById("cap");
    const recaptureBtn = document.getElementById("recap");
    const doneBtn = document.getElementById("done");
    const imagePreview = document.getElementById("my-data-uri");
    const imageInput = document.getElementById("myImageInput");
    const form = document.getElementById("myForm");

    let beforeCapture = true;

    async function camera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: {
                    width: { min: 400, ideal: 400, max: 400 },
                    height: { min: 400, ideal: 400, max: 400 },
                },
            });

            video.srcObject = stream;
            canvas.width = 400;
            canvas.height = 400;
        } catch (error) {
            console.error("Something went wrong!", error);
        }
    }

    function getCurrentFrame() {
        beforeCapture = false;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imgDataURI = canvas.toDataURL("image/png");

        video.style.display = "none";
        imagePreview.src = imgDataURI;

        captureBtn.classList.add("is-hidden");
        doneBtn.classList.remove("is-hidden");
        recaptureBtn.classList.remove("is-hidden");
    }

    function recapture() {
        window.location.reload();
    }

    function postData() {
        imageInput.value = canvas.toDataURL("image/png");
        form.submit();
    }

    captureBtn.addEventListener("click", getCurrentFrame);
    recaptureBtn.addEventListener("click", recapture);
    doneBtn.addEventListener("click", postData);

    camera();
});
const media = {
    cameraOn: true,
    microphoneOn: true,
    microphoneElement: document.getElementById("microphone"),
    cameraElement: document.getElementById("camera"),
    toggleCamera() {
        this.cameraOn = !this.cameraOn;
        if (this.cameraOn) {
            this.cameraElement.classList.remove("media-off");
        } else {
            this.cameraElement.classList.add("media-off");
        }
    },
    toggleMicrophone() {
        this.microphoneOn = !this.microphoneOn;
        if (this.microphoneOn) {
            this.microphoneElement.classList.remove("media-off");
        } else {
            this.microphoneElement.classList.add("media-off");
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
   let video = document.querySelector("#video");

   navigator.mediaDevices.getUserMedia({ video: true })
       .then(stream  => {
           video.srcObject = stream;
       }).catch(e => {
           console.log(e)
       })
})

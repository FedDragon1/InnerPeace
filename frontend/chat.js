const chat = {
    textBox: document.querySelector("#chat-data"),
    backend: 'http://127.0.0.1:5000/api/',  // flask backend localhost
    requestFor(name) {
        return `${this.backend}/${name}`
    },
    sendChat() {
        axios.post(this.requestFor("chat"), { data: this.textBox.value })
            .then(resp => {
                console.log(resp)
                this.textBox.value;
            })
            .catch(err => {
                console.log(err)
            })
    }
}


function getDateString() {
    const today = new Date();
    const date = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
    return `Date: ${date}, Time: ${time}`;
}

function sendInfoToFusion(args) {

    // Send the data to Fusion as a JSON string. The return value is a Promise.
    adsk.fusionSendData("messageFromPalette", JSON.stringify(args)).then((result) =>
        document.getElementById("returnValue").innerHTML = `${result}`
    );

}

let data = {
	length: 105,
	girth: 50,
	ballDiameter: 50,
	urethraDiameter: 15,
	circumsized: false,
	foreskinLength: 15,
}

function validate() {
	return data.length/2 > data.foreskinLength && data.urethraDiameter < data.girth/2;
}

function renderObject() {
	document.getElementById("message").innerHTML =
		`Length: ${data["length"]}mm <br/>` +
		`Girth: ${data["girth"]}mm <br/>` +
		`Ball Diameter: ${data["ballDiameter"]}mm <br/>` +
		`Urethra Diameter: ${data["urethraDiameter"]}mm <br/>` +
		`Circumsized: ${data["circumsized"]} <br/>` +
		`Foreskin Length: ${data["foreskinLength"]}mm`;
}

function updateSliderDisplay(id, accessor, value) {
	document.getElementById(id).innerHTML = value;

	data[accessor] = value;

	renderObject();
}

function toggleButton(id, btn) {
	data[id] = btn.checked

	renderObject();
}

function submitForm() {
	if (validate()) {
		sendInfoToFusion(data);
	} else {
		document.getElementById("message").innerHTML = "Invalid data! Urethra must be smaller than half of girth and half of length must be greater than foreskin!";
	}

}


function updateMessage(messageString) {
    // Message is sent from the add-in as a JSON string.
    const messageData = JSON.parse(messageString);

    // Update a paragraph with the data passed in.
    document.getElementById("fusionMessage").innerHTML =
        `<b>Your text</b>: ${messageData.myText} <br/>` +
        `<b>Your expression</b>: ${messageData.myExpression} <br/>` +
        `<b>Your value</b>: ${messageData.myValue}`;
}

window.fusionJavaScriptHandler = {
    handle: function (action, data) {
        try {
            if (action === "updateMessage") {
                updateMessage(data);
            } else if (action === "debugger") {
                debugger;
            } else {
                return `Unexpected command type: ${action}`;
            }
        } catch (e) {
            console.log(e);
            console.log(`Exception caught with command: ${action}, data: ${data}`);
        }
        return "OK";
    },
};

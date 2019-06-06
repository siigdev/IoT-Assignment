

window.addEventListener("load", function () {
    // ###############################
    // # MQTT CONNECTION             #
    // ###############################

    client = new Paho.MQTT.Client("m24.cloudmqtt.com", 31674, "hrngsnyc");
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;
    var options = {
        useSSL: true,
        userName: "hrngsnyc",
        password: "xxxx",
        onSuccess: onConnect,
        onFailure: doFail
    }
    client.connect(options);

    function onConnect() {
        console.log("onConnect");
        client.subscribe("/cloudmqtt");
        message = new Paho.MQTT.Message("Hello CloudMQTT");
        message.destinationName = "/cloudmqtt";
        client.send(message);
    }
    function doFail(e) {
        console.log(e);
    }
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }
    }
    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);
    }



    // ###############################
    // # DOM MANIPULATION            #
    // ###############################

    // Handle the Brightness Slider
    var brightnessSlider = document.getElementById("brightnessSlider");
    var level = document.getElementById("level")
    brightnessSlider.oninput = function () {
        level.textContent = this.value;
        var msg = ("brightness:" + this.value);
        message = new Paho.MQTT.Message(msg);
        message.destinationName = "/cloudmqtt";
        client.send(message);
    }

    // Handle the Modes radio buttons
    var modes = document.getElementsByName("mode")
    var none = document.getElementById("none")
    var breathe = document.getElementById("breathe")
    var party = document.getElementById("party")
    var party = document.getElementById("heartbeat")
    var automatic = document.getElementById("automatic")
    for (mode in modes) {
        modes[mode].onclick = function () {
            if (this.value == "automatic") {
                brightnessSlider.disabled = true
                level.textContent = "Automatic"
            }
            else {
                brightnessSlider.disabled = false
                level.textContent = brightnessSlider.value
            }
        }
    }

    var colorPicker = new iro.ColorPicker('#color-picker-container', {
        layout: [
            {
                component: iro.ui.Wheel,
                options: {
                    width: 200
                }
            }
        ]
    });

    function onColorChange(color, changes) {
        var msg = (color.rgbString);
        message = new Paho.MQTT.Message(msg);
        message.destinationName = "/cloudmqtt";
        client.send(message);
    }

    // listen to a color picker's color:change event
    colorPicker.on('color:change', onColorChange);
});


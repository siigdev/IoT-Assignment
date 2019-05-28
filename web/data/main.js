window.addEventListener("load", function () {
    
    // Handle the Brightness Slider
    var brightnessSlider = document.getElementById("brightnessSlider");
    var level = document.getElementById("level")
    brightnessSlider.oninput = function () {
        level.textContent = this.value;
    }

    // Handle the Modes radio buttons
    var modes = document.getElementsByName("mode")
    var breathe = document.getElementById("breathe")
    var party = document.getElementById("party")
    var automatic = document.getElementById("automatic")
    for(mode in modes) {
        modes[mode].onclick = function() {
            if (this.value == "automatic"){
                brightnessSlider.disabled = true
                level.textContent = "Automatic "
            }
            else {
                brightnessSlider.disabled = false
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
        // print the color's new hex value to the developer console
        console.log(color.rgb);
    }

    // listen to a color picker's color:change event
    colorPicker.on('color:change', onColorChange);
});


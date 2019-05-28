window.addEventListener("load", function () {
    var slider = document.getElementById("brightnessSlider");
    var output = document.getElementById("level");
    slider.oninput = function () {
        output.textContent = this.value;
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


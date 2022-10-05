var jumps = {{jumps}};

var script = {{script}};

var pointer = 0;

// A quick bit of syntactic sugar to make "If `not(x)`" slightly more readable.
function not(x) {
    return !x;
}

function go_to(name) {
    pointer = jumps[name];
}

var loading_indicator = null;
function show_loading_indicator() {
    loading_indicator = speak("..."); // The `speak` function is provided in botengine.js.
}

function next() {
    if (loading_indicator) {
        loading_indicator.remove();
        loading_indicator = null;
    }
    script[pointer++]();
}
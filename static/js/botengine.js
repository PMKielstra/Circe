var bot_display;

function launch_bot(id) {
    bot_display = document.getElementById(id);
    bot_display.innerHTML = "";
    next(); // Start bot
}

function print(utterance, human=false) {
    container = document.createElement("div");
    if (human) {
        container.className = "human";
    }
    container.appendChild(utterance);
    bot_display.appendChild(container);
    container.scrollIntoView();
    return container;
}

function speak(utterance, human=false) {
    var u = document.createElement("p");
    u.innerHTML = utterance;
    return print(u, human);
}

var pause = false;
function gated_next() {
    if (!pause) {
        next();
    }
}

function say(utterance) {
    speak(utterance);
    gated_next();
}

function choose(choices) {
    var choice_elements;
    choice_elements = choices.map(choice => {
        if (choice.filter()) {
            const text = choice.text();
            if (text == "") {
                choice.command();
                gated_next();
            } else {
                var choice_link = document.createElement("a");
                choice_link.href = "#";
                choice_link.innerHTML = text;
                choice_link.onclick = function () {
                    choice_elements.forEach(x => {if (x) x.remove(); });
                    speak(text, human=true);
                    choice.command();
                    gated_next();
                    if (pause) {
                        pause = false;
                    }
                }
                return print(choice_link, human=true);
            }
        } else {
            return null;
        }
    });
    if (choice_elements.every(x => x == null)) {
        gated_next();
    }
}

function input(type, params, callback) {
    pause = true;
    var input_element = document.createElement("input");
    input_element.type = type;
    for (const [key, value] of Object.entries(params)) {
        input_element[key] = value;
    }
    var submit_button = document.createElement("input");
    submit_button.type = "submit";
    var form = document.createElement("form");
    form.appendChild(input_element);
    form.appendChild(submit_button);
    var submit_func = function() {
        pause = false;
        submit_button.remove();
        input_element.disabled = true;
        callback(input_element);
        gated_next();
        return false;
    }
    form.onsubmit = submit_func;
    input_element.onkeydown = e => { if (e.key == "Enter") submit_func };
    return print(form, human=true);
}

function exit() {
    pause = true;
    speak ("Thanks for talking to this bot!  <a href=\"#\" onclick=\"window.location.reload();\">Click here</a> to start over.");
}
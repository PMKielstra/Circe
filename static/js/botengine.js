var bot_display;

var text_repl = false;
function request_text_repl(callback) {
    text_repl = true;
    while(true) { // TODO: IMPLEMENT THIS PROPERLY
        callback(prompt);
    }
}

function launch_bot(id) {
    bot_display = document.getElementById(id);
    bot_display.innerHTML = "";
    if (!text_repl) next(); // Start bot -- the `next` function will be provided by the bot's own code.
}

// Add a message, in the form of an arbitrary HTML element, to the bot display, as if it were being said either by the bot or by the human.
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

// Convert text to a paragraph and print it.
function speak(utterance, human=false) {
    var u = document.createElement("p");
    u.innerHTML = utterance;
    return print(u, human);
}

// Sometimes various instructions will require that the bot wait.
// For instance, it might have just asked the user for input.
// In these situations, we set `pause` to true.  Then, rather than calling `next`, we can call `gated_next`.
var pause = false;
function gated_next() {
    if (!pause) {
        next();
    }
}

// Speak a thing and then go to the next instruction.
function say(utterance) {
    speak(utterance);
    gated_next();
}

// Provide a number of options for the user to choose from.
function choose(choices) {
    var choice_elements; // Keep track of these so we can remove them later once the user has chosen.
    choice_elements = choices.map(choice => {
        if (choice.filter()) { // choice.filter: determine on the fly if a choice should be shown
            const text = choice.text(); // choice.text: determine the text to show the user
            if (text == "") { // If there's no text attached to the choice, just execute the command.  (In Markdown, we use a double hyphen instead of just a blank bullet point, but the compiler strips that.)
                choice.command();
                gated_next();
            } else {
                var choice_link = document.createElement("a");
                choice_link.href = "#";
                choice_link.innerHTML = text;
                choice_link.onclick = function () {                         // When a choice is selected,
                    choice_elements.forEach(x => {if (x) x.remove(); });    // remove all other choices,
                    speak(text, human=true);                                // speak back the selected choice as if it came from the human,
                    choice.command();                                       // run the relevant command,
                    gated_next();                                           // go on if possible,
                    if (pause) {                                            // and unpause if necessary.  (Sometimes the choice commands will require pausing.)
                        pause = false;
                    }
                }
                return print(choice_link, human=true);
            }
        } else {
            return null;
        }
    });
    // If all possible choices were filtered out, just go on.
    if (choice_elements.every(x => x == null)) {
        gated_next();
    }
}

// Provide a way for the user to give arbitrary input.
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
    form.onsubmit = submit_func;                                            // Submit either if the submit button is pressed...
    input_element.onkeydown = e => { if (e.key == "Enter") submit_func };   // ...or if the enter key is pressed.
    return print(form, human=true);
}

// Quit the bot.  Set pause to true and don't call next.
function exit() {
    pause = true;
    speak ("Thanks for talking to this bot!  <a href=\"#\" onclick=\"window.location.reload();\">Click here</a> to start over.");
}
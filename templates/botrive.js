<script type="text/javascript" src="https://unpkg.com/rivescript@latest/dist/rivescript.min.js"></script>
<script type="text/javascript">
    var rive = new RiveScript();
    var rivepromise = rive.loadFile("/botstatic/{{name}}.rive");
    rivepromise.then(loading_done).catch(loading_error);
    function loading_error() {
        say("Could not compile RiveScript");
    }
    function loading_done() {
        rive.sortReplies();
        say("You are now chatting with {{name}}.");
    }
    async function next(){
        await rivepromise;
        input("text", {}, function(user_input) {
            rive.reply("local-user", user_input.value).then(say);
        }, call_next = false);
    }
    request_self_start();
</script>
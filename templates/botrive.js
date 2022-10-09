<script type="text/javascript" src="https://unpkg.com/rivescript@latest/dist/rivescript.min.js"></script>
<script type="text/javascript">
    var rive = new RiveScript();
    const rive_code = "{{rive_code}}";
    if(!rive.stream(rive_code)) {
        say("Could not compile RiveScript");
    } else {
        rive.sortReplies();
        const username = "local-user";
        request_text_repl(function (input) {
            rive.reply(username, input).then(say);
        });
    }
</script>
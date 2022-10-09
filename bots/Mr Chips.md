# Mr. Chips

Hi!  I'm Mr. Chips, and I'm here to teach you how to write chatbots in Markdown for the Circe platform!

Where would you like to start?

* 1: What's Markdown?

  * Intro to Markdown

* 2: Choose Your Own Adventure
  
  * CYOA

* 3: Deploying to Circe
  
  * Deployment

* 4: User Input and Other Actions
  
  * Input

* 5: Advanced Scripting
  
  * JS

## Intro to Markdown

Let's get you started with an intro to Markdown.

When you write a plain text document, there's no formatting.  It's just the letters you put into your notepad program.  On the other hand, pretty much anyone can read a plain text document.  You can store it, send it to other people, or even use it as input for a program.

When you write a Word document, you can use all kinds of formatting.  You can have headings, links, bold or italic text, anything you want.  But Word documents are hard to read if you don't have Word.  In order to support the complex formatting, the Word developers gave up on creating documents that were easy for other people, or other people's software, to parse.

Markdown splits the difference.  It's a file format that you can easily read and write in a plain text editor, but, at the same time, one that you can render in a Markdown editor with all the pretty formatting you'll need.

* Let's get started!

Do you have a Markdown editor installed?

* I do
  
  * Editor installed

* I don't, or I don't know

There are plenty to choose from.  My illustrious creator usually uses [MarkText](https://github.com/marktext/marktext#download-and-installation).  It runs on Windows, Mac, and Linux.  If you don't like that, you can try [Abricotine](http://abricotine.brrd.fr/), which has the advantage of being named after a French apricot brandy.

Why not go ahead and install it?  I'll wait.

* I've installed a Markdown editor.

### Editor installed

There's loads you can do with Markdown.  For example, if you have an underscore or an asterisk at the beginning and end of a word or sentence, it'll be _italic_.  If you have two underscores or two asterisks, it'll be **bold**.

If you wrap some text in [square brackets] and immediately follow that, without a space, with a URL in (https://parentheses.com), it'll turn into [a link](https://github.com/PMKielstra/Circe).

You can see more Markdown syntax [here](https://learnxinyminutes.com/docs/markdown/).

But, to write a chatbot with Circe, there are only four Markdown commands you need to know.

The first is _headings_.  To create a heading, start a line with a hash symbol (#) and a space.  For smaller headings, use more hash symbols.  You can use up to 6.  Have a play around in your editor now, and make sure you can do that.

* Got it.

The next thing you need to learn is _lists_.  Start a line with an asterisk and a space, and it'll kick off a bullet-point list for you.  Any Markdown editor should make lists easy for you once you get started.  In particular, you should be able to press the tab key to get a level of indentation.  Make sure you can make a list of bullet points, where each bullet point has a sublist underneath it.

* Can do.

Believe it or not, that's all we'll be using for now.  Later on, though, you'll need to use code.  I'll cover that in more detail when I get to it, but for now let's make sure you know what a _backtick_ is.  It's on the top left of a US keyboard and it looks like this: `.  It's an apostrophe pointing the wrong way.

This is actually important enough that I'm going to make sure we agree on what key it is.  Can you give me three backticks?

#### Backtick test

* --
  
  * Input backticks text

```
if (backticks.value != "```") {
    speak ("I don't think that's quite right.  I'm looking for three backticks.  It should look something like this: ```.");
    go_to ("Backtick test");
}
```

Amazing!  That's all the Markdown you need for now.

* I want to write a bot!

## CYOA

Time to write your first bot!  We'll jump right into a Choose Your Own Adventure game.  Open a new document in your Markdown editor.

You can think of Circe as reading through your Markdown document top to bottom, bit by bit.  Each paragraph is a message sent by the chatbot.  So go ahead and create some paragraphs now, in your Markdown editor.  Maybe set the scene.

* "It's a dark and stormy night..."

As is, Circe is going to just read your entire file in one go and then stop.  That's not very interactive.  Let's give her some structure so she can make more complex paths through the document.

Circe doesn't read Markdown headings out loud.  (Remember, those start with a #.)  They exist, for her, as places you can tell her to go, sort of like page numbers.  Usually, when a user makes a choice, part of Circe's response to that choice will involve jumping to one heading or another.  For a Choose Your Own Adventure game, that's all that we want to do.

So create at least two different headings underneath your scene-setting paragraphs.  (It doesn't matter how many # symbols you use for each -- Circe treats them all the same -- but being logical about which headings are big and which are small can be helpful for making readable bots.)  Remember: the exact content of your headings won't be shown to the end user, so you can say whatever you want in there, but it should probably be short and snappy.

The headings should each represent a possible action the player can take.  Put a paragraph under each of them describing the outcome of that action.

* Well, that seemed kind of pointless...

It is.  Or, at least, it's pointless without this next bit.  Whenever Circe comes to a bullet list, she stops and lets the user pick an option from that list.  (Bullet lists are made with an asterisk.)  Go back to the bit just below your scene-setting paragraphs, and add a bullet list.  Each option should be a description of an action, corresponding to the actions you had in mind when you wrote your heading.

Then, add a sublist below each bullet point.  That sublist should have just one item: the name of the heading you'd like Circe to jump to if the user selects that choice.

All in all, it should look something like this:

<ul><li>Pick up the axe</li><ul><li>Axe Fun Time</li></ul><li>Jump off the cliff</li><ul><li>Cliff Fall Death</li></ul></ul>

* Yay interactivity!

One last thing: remember when I said that Circe will read through your entire file unless you tell her otherwise?  That's still true if the file has headers.  When Circe reaches the end of one section, she'll go straight on into the next by default.

To avoid that, we'll tell her to end the game early at the end of the second section.  Unless you're writing custom code, which we'll get to later, pretty much all of your commands should come in response to a choice the user makes.  That means that all of them follow this list-sublist pattern we've already seen.

But in this case we don't want to offer the user a choice.  We just want Circe to end the bot without saying anything.  So, rather than putting a choice option in your top-level bullet point, you can use two hyphen characters: "--".  This is a shorthand for "Don't actually say anything; just execute whatever command comes in the sublist for this bullet point."

And then, in that sublist, rather than giving a heading to jump to, just put "Exit".  (Note that there's no period after the word.)  This is a _special command_.  It tells Circe to say goodbye to the user, give them the option to restart the bot, and end the session.  

You can use a special command anywhere in these second-level lists that you might otherwise give a heading to jump to.  You can even chain them together: if you have more than one command in a second-level list after a bullet point, all of them are executed if the user chooses that bullet point.  (Since the only command you know so far is "Exit", I'm not sure why you'd want to do that, but it's more useful later.)

That's about all you need for a Choose Your Own Adventure game!  Feel free to expand yours a little bit, and then we can come back and turn it into a real live bot.  Let me know when you're ready for that.

* I'm good to go.

## Deployment

This is going to be a bit vague.  For security reasons, I can't tell you much about your server.  Here's what I _can_ say:

First, pick a name for your bot.  It shouldn't have any spaces in it.

* --
  
  * Input botname text (placeholder: "Bot name")

Now, rename your Markdown file to `botname.value`.md.  (Markdown files end in ".md".)

The administrator of this bot server should have told you where this file needs to go and how to upload it.  Put it there.

* Done it.

```
baseurl = window.location.href.replace("MrChips", "")
if (baseurl.slice(-1) == "#") {
    baseurl = baseurl.slice(0, -1)
}
boturl = baseurl + botname.value
resourceurl = baseurl.slice(0, -1) + "static/&lt;filename&gt;"
```

If your bot uses any images or other resources, put them into the same folder as the script file.  You can access them at `resourceurl` -- your Markdown script should reference them at that location.

Your bot should now be available at `"<a href=\"" + boturl + "\", target=\"_blank\">" + boturl + "</a>"`.  Have a play!  We'll cover basic scripting next.

* I'm ready.

## Input

Much like quitting the bot early, taking input from the user is a special command.  It looks something like this:

<ul><ul><li>Input username text (placeholder: "Your name")</li></ul></ul>

Let's break that down bit by bit.

It starts with "Input", which is always the case.

Then it has the name of the variable where the input will be stored.  In this case, that's "username".  This variable name isn't shown to the end-user.  Since you'll be using it in code later, make sure it actually does work as a variable name: it should have only letters and numbers in it, no spaces, and it should start with a letter.

Then there's the type of input, which is "text".  That's the most common.  You can ask for other types of input, too: "number" only lets the user enter numbers, and "password" hides anything they might type in from people looking over their shoulder.

Finally, there are parameters which can be passed to the input.  The big one is "placeholder", which is for the grey text that displays inside the input before the user puts any values there.  You don't have to have this.  Just "Input username text" would work just as well.

(In fact, you can use any HTML input type. Once the user submits their input, the entire &lt;input&gt; component gets stored in the named variable. If you want to access, say, uploaded files, you do that with the "files" property, just the same as on a normal component.  The entire parameter structure is exactly a JSON object with the outer curly brackets replaced by parentheses, and it gives property values that will be set on the input tag.  If you don't know what that means, don't worry about it.)

By the way, using a special command doesn't mean you can't also redirect the user.  You can always have multiple commands after a bullet point.  All of them will be executed if the user makes that choice.  It's perfectly possible for a user to have one and not another.

* How do I use this?

Great question.  Start a new bot.  This one's going to ask the user's name and then greet them.

First, we'll have to ask what the user's name is, and then go straight into an input scenario without giving them a choice.  Your result should look something like this:

<p>Hi!  What&#x27;s your name?<ul><li>--</li><ul><li>Input username text</li></ul></ul></p>

Note that we aren't telling Circe to jump to any heading after this, so she'll just keep on going down the bot script.

Now, as soon as the user has entered something into that text box, the "username" variable will acquire many different properties.  The one we're interested in is its _value_, that is, the thing the user actually typed.  So let's write another paragraph, after the list, which references that value.  The way to do this is through an _inline code block_.  In short, anything within a paragraph that you wrap in backticks (that's `, remember) is going to be treated, not as text, but as code.

Your next paragraph should look something like this:

Hello, &#96;username.value&#96;!  Great to meet you.

In general, this is the rhythm of collecting input from a user: you start with an "Input &lt;variable&gt; &lt;type&gt;" special command, and then later you access that with &#96;&lt;variable&gt;.value&#96; or similar.

* What if I want to actually process input?

The easiest way to do that, and the only way that doesn't require coding, is to show or hide chunks of text or choices based on what the user has and hasn't told you.

If you start a paragraph or choice with "(If &#96;&lt;something&gt;&#96;)", then that paragraph will only be shown if <something> is true.  For instance, you might start with "(If &#96;username.value == "admin"&#96;)" to give out information to which only the administrator should have access.

You can compare values in all the ways you can compare them in JavaScript.  Most likely, though, you'll want to use "==".  That means "Equals".  Programming languages pretty much universally use a double equals sign instead of a single equals sign for equality.  Don't mess this up.

To do any more complicated processing, you'll have to write full-on custom code.

* I want to write full-on custom code.

## JS

At this point I'll start assuming you know some JavaScript.  If you don't, my creator recommends [Codecademy's JavaScript course](https://www.codecademy.com/learn/introduction-to-javascript).

Instead of writing a paragraph, you can write JavaScript enclosed in a Markdown _code fence_ (a paragraph where the lines above and below, rather than being blank, have three backticks).  When Circe gets to code in a code fence, she'll run it rather than printing it.

You can use a code fence inside a choice sublist as a special command.  Circe will run the code in that fence if the user selects the relevant choice.  Of course, this does not preclude also adding further special commands to the same list.  (Using a WYSIWYG Markdown editor is often helpful to handle the logistics of a code fence inside a bullet list.)

Use global variables in code blocks (I know, I know...).  This is because each block is compiled to a separate function, so, if you want to share variables between functions, you should use global scope.

You have the following special functions:

"speak(text, human=false)": Say "text" as if it's coming from either the bot or the user.

"go_to(heading)": Go to a specific heading once this code block is done executing.

"show_loading_indicator()": show a loading indicator message from the bot that will automatically disappear when this code block is done executing.

"exit()": Stop the bot.

"not(x)": Calculate !x.  Can make inline code more elegant.

That's all there is to it!  Enjoy writing Markdown bots.

* Goodbye, Mr. Chips.

![Goodbye, Mr. Chips](/botstatic/GoodbyeMrChips.jpg)

Goodbye.

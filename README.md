# Adapt Bot
Currently, most chat bots require you to memorize argument order and syntax in
order to use them properly. However I see absolutely no reason why this needs
to be the case. Advances in natural language processing mean that we now have
open source parsers capable of understanding "normal" human speech.  

This bot uses the [Adapt Intent Parser](https://github.com/MycroftAI/adapt) to
accomplish exactly that. After outlining the basic syntax and vocabulary of your
plugin (called a Skill), Adapt Bot will recognize when you are attempting to
call this skill and properly order arguments and call your code. Instead of
having `!weatherbot question snow Seattle`, for example, Adapt Bot allows users
to ask `@AdaptBot Is it snowing in Seattle?`

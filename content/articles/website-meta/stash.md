## first positive surprise: updating the build chain

When creating this website about 3 years ago I used the [lektor development mode](https://github.com/lektor/lektor#want-to-develop-on-lektor) to be able to poke around in the code and write my own plugins, etc. This is fun, but also means that updating to a newer version might be more tedious especially when having dug around in some internals that you are not really supposed to touch. So I updated npm, pulled the newest changes from lektor and ran a build of my website to see if this bleeding edge approach still works for my site. To my surprise it did! Cudos to the Lektor developers :)

I created this web site a few years ago with the idea to share what I write more publicly as I have learned a lot from what others wrote. This is also a good way to gently nudge myself into thinking things through a bit more thoroughly in order to be able to explain them better. 

I have written and done quite a few things over the last few years, but my blog was the classic case of: built the site, wrote on article, lost interest. 

But there is a lot of material from my courses that I would like to make available to the community and there are also lots of half written articles in my drafts folder which I'd love to go back to and bring into a publishable state.

So what's a person like me to do about this? Of course: I spend a lot of time again thinking about how to ease the technical process of publishing articles and build something to support that process. As it seems to be a tradition for technical bloggers to blog about how they built their blog, I will blog about this now to get the ball rolling again :)

* lektor (because the others are too limiting)
* hosting on github with CNAME and HTTPS
* my own style (using sass)
* my own little plugin for sass watching
* lektor butler (for drafts workflow)
* lektor + jupyter
* tox for everything

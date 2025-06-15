If you want to build the whole thing, just run

bash build_everything.sh

You generally don't want to, because it takes ~15 minutes to do all the minutes, and nobody has time for that. Fine for a periodic refresh, but not every time we bring in a magazine. So...

First of all, everything is in git, so if you add something, you need to do it there. https://github.com/telliott/new_website_mitsfs (need to move it over to the mitsfs git account, but that requires someone to have the login). Ping ookcomm with your git account if you need commit access.



The website is designed to run at the root of your localhost. Every link is relative to there, so if you pull it down, you should be able to make changes locally and test them in your browser. If you don't have a local build, the ookcomm/new_website_test is a git copy and you can put stuff there to commit it. Sadly, there doesn't seem to be any way to run a test website.

The website runs at ookcomm/production, so you pull there once you're ready to go. 

NEW WEB PAGES

page_template.html in this folder is the general template that will get you the header and footer and pull in the css. Copy that where you want it to go, then edit away. Editing the original will not change most of the pages on the site (except the ones being automatically built below), so if you need to change the overall site look, you'll have ~10 pages you need to fix.

Don't mess with PAGE GOES HERE on the template unless you know what you're doing. The built parts of the site rely on that string to split the header and footer.

BOOKS

When the dex is updated. you need to export a copy into this directory, then run 

python3 copy_dex.py

That will copy the dex into the pinkdex directory. It's not checked into git in that folder because we need to update that script so that it'll pull straight from the database and write there instead of the interim stage.

MAGAZINES

The magazines are all json files in magdex/magazines. Add/edit them there, then run

python3 generate_mags.py

Creating a new magazine involves creating a new json file (needs to end in .json) and dropping it into the appropriate folder. The name is taken from the json, not the name of the file. Make sure to tag them correctly as issue-based or month-based in the json; and if you do month-based, watch out for the season map, which can vary depending on how the magazine did dates. There's plenty of examples of all types to follow in there.

REVIEWS:

Reviews get added into reviews/raw. What you call them doesn't really matter; the current Author-Title works fine, but you do need to make sure they end with .txt or they won't get picked up. The template to follow for reviews is review_template.txt in this folder so that they can be parsed properly into the front page.

When you have a new review in place, run

python3 generate_reviews.py

MINUTES

Minutes are written in latex, and saved into minutes/raw. The template for them is minutes/raw/format.tex, so copy that to the year folder (or create one if it's missing). They must be named minutes.YYYY-MM-DD.tex to be picked up and parsed correctly.

Running the minutes takes a while, and it would be a big pain if you had to do it every week. So the minutes script takes a parameter:

python3 generate_minutes.py <year>

If you give it a (4-digit) year, it'll rebuild just that year (including your new file!) and the index page.



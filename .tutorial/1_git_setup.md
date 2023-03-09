# Create a repo on GitHub

_Message on our [Discord](https://discord.com/invite/925SYVse2H) if you get stuck here!_

The first step to creating a bot on Regression Games is to
create a GitHub repository, which will hold your bot code. 
If you do not have a GitHub account, you can create one 
[here](https://github.com).

Open the "Git" tool on Replit from the tools section (or by clicking
`+` to open a new tab in the editor window and searching for "Git").

![Git tool on Replit](images/replit_git_1.png)

In the Git window that appears, click "+ Create a Git repo". Wait a few
seconds, as it sets everything up in your Repl. Eventually, you should
see a "New repo" button appear (or a button to connect your GitHub account
if you haven't yet - do that first). Click that button enter info about your
new bot (see example below), and then click
"+ Create repository". After a few seconds, your code will be pushed
to GitHub (or click the **Push** button yourself if it is present).
You can now visit your GitHub repository by clicking the
link at the top of the Git tool pane.

![Git initialized](images/replit_git_2.png)
![Git repo](images/replit_git_3.png)

## Updating code

Whenever you want to update code for your bot, all you need to do
is push your changes to GitHub! You have two options for doing this.

1. Visit this Replit Git pane and click "Commit All & Push". Note that sometimes the Git
   pane **will not detect your changes automatically**. If this happens,
   you can close the Git tab and re-open it using the steps above.

2. Open the Shell in Replit, and use normal Git commands. You will be prompted
   to verify usage of your Git credentials from Replit. For example, you can
   use the following series of commands to push new code.

```bash
git add .
git commit -m "A comment about my new changes"
git push # or, for the first time, "git push -u origin main"
```

![Git repo](images/replit_git_example.png)

## Note on ease-of-use (optional)

Coming soon - configs to have the "Run" button in Replit push your code
for you!
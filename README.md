# FOO

Basic git setup :

use the following in your desired working directory
```
  git clone https://github.com/arjun-krishna/FOO.git
  cd FOO
  git remote rename origin upstream
  git remote add origin https://github.com/{user_name}/FOO.git      # assuming you have this on the web too
```

to confirm the setup just type : git remote -v  [must have upstream, origin suitably pointed ]

Once the setup is done, add features you want to add and then commit it with a meaningful commit message using
```
  git commit -m "meaningful message"
```
and push the changes you make to your origin [master]
```
  git push origin master
```

Now, send a pull request from the website to the upstream/master from origin/master
The code shall we viewed and merged in case there is no merge conflicts

To stay upto-date with the main codebase, use
```
  git fetch upstream
  git rebase upstream/master
  
  # in case of any merge conflicts -- resolve it and then use
  # git rebase --continue

```
Use the above to even fix merge conflicts in the pull request sent, resolve the conflicts commit the changes and push 
the changes to your origin/master
  

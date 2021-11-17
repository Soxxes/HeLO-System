1) Download the .exe.
2) Run the .exe on your computer and select a directory where the "HeLO-System" should be installed.
3) After the installation process you will have a folder in your selected directory. Look for a file named "main.exe" and run it.
4) If you didn't get any errors, you're fine! :) Otherwise, contact me on Discord: Soxxes#8047.

IMPORTANT:
You have to change the data base information in the config.json after installing the application. Otherwise you will push your results
to my test data base. If you got a Superuser access from me, feel free to change "username" and "password".

Copy and paste this:
{
    "mongodb": {
        "cluster": "cluster0",
        "db": "HeLO_Scores",
        "collection": "scores",
        "username": "Public",
        "password": "6h2WPva5g"
    }
}
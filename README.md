Need config Advanced system settings
    key : GIT_API_KEY
    value : need to generate git rest api token
        profile --> Settings --> Developer settings --> Personal access tokens --> Token(classic) -- Generate new token
        After generate token, need authrise AspiraVentures

Generate exe file
    install dependancy 
        pip install -r requirements.txt
    
    generate main.exe
        pyinstaller --onefile --add-data "config;config" main.py

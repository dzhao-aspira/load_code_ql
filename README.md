Need config Advanced system settings
    key : GIT_API_KEY
    value : need to generate git rest api token
        profile --> Settings --> Developer settings --> Personal access tokens --> Token(classic) -- Generate new token
        After generate token, need authrise AspiraVentures

Generate exe file
    install dependancy 
        pip install -r requirements.txt

    generate main.spec
        pyinstaller --onefile main.py

    update main.spec
        a = Analysis(
            ['main.py'],
            pathex=[],
            binaries=[],
            datas=[('config/config.properties', 'config/config.properties')],
            ...
        )
    
    generate main.exe
        generate main.spec

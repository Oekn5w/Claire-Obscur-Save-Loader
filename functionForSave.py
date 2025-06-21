import os
import shutil
import stat
import json

folderLocation = os.path.join(os.getenv('LOCALAPPDATA'), "Sandfall", "Saved", "SaveGames")
AllSavePath = os.path.join(folderLocation, "Save")
os.makedirs(AllSavePath, exist_ok=True)
ConfigFile = os.path.join(folderLocation, 'config_SaveManager.json')

for i in os.listdir(folderLocation):
    if i.isdigit():
        CurrentSavePath = os.path.join(folderLocation, i)
        break

def GetSavePath(Profile):
    return os.path.join(AllSavePath, Profile)

def ImportSave(SteamID, Name, Profile):
    CurrentSavePath = os.path.join(folderLocation, SteamID)
    if not os.path.exists(CurrentSavePath):
        return False
    if Profile == "":
        return False
    NewSavePath = os.path.join(AllSavePath, Profile, Name)
    if os.path.exists(NewSavePath):
        os.chmod(NewSavePath, stat.S_IWUSR)
        shutil.rmtree(NewSavePath)
    shutil.copytree(CurrentSavePath, NewSavePath, dirs_exist_ok=True)
    return True

def DuplicateSave(Name, NameOfCopy, Profile):
    if Profile == "":
        return False
    OldSavePath = os.path.join(AllSavePath, Profile, Name)
    NewSavePath = os.path.join(AllSavePath, Profile, NameOfCopy)
    if os.path.exists(NewSavePath):
        os.chmod(NewSavePath, stat.S_IWUSR)
        shutil.rmtree(NewSavePath)
    shutil.copytree(OldSavePath, NewSavePath, dirs_exist_ok=True)
    return True

def RemoveSave(Name, Profile):
    if Profile == "":
        return False
    RemovedSavePath = os.path.join(AllSavePath, Profile, Name)
    os.chmod(RemovedSavePath, stat.S_IWUSR)
    shutil.rmtree(RemovedSavePath)
    return True

def RenameSave(OldName, NewName, Profile):
    if Profile == "":
        return False
    OldNamePath = os.path.join(AllSavePath, Profile, OldName)
    NewNamePath = os.path.join(AllSavePath, Profile, NewName)
    os.rename(OldNamePath, NewNamePath)
    return True

def LoadSave(SteamID, Name, Profile):
    CurrentSavePath = os.path.join(folderLocation, SteamID)
    if not os.path.exists(CurrentSavePath):
        return False
    if Profile == "":
        return False

    LoadedSavePath = os.path.join(AllSavePath, Profile, Name)

    if os.path.exists(CurrentSavePath):
        for i in os.listdir(CurrentSavePath):
            item_path = os.path.join(CurrentSavePath, i)
            if i == "Backup":
                for j in os.listdir(item_path):
                    os.remove(os.path.join(item_path, j))
            else:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    try:
        shutil.copytree(LoadedSavePath,CurrentSavePath,dirs_exist_ok=True)
    except Exception:
        return False

    return True

def GetListOfSave(Profile):
    return os.listdir(os.path.join(AllSavePath, Profile))

def GetListOfProfile():
    return os.listdir(AllSavePath)

def GetDictOfSteamIDs() -> dict:
    loaded_config = {}
    try:
        if os.path.exists(ConfigFile):
            with open(ConfigFile) as f:
                loaded_config: dict[str, Any] = json.load(f)
    except Exception as e:
        pass

    retVal = {
        "ids": {},
        "latest": ""
    }
    timecomp : float = 0
    for sid in os.listdir(folderLocation):
        if sid.isdigit():
            retVal["ids"][sid] = "name_" + sid
            if sid in loaded_config:
                retVal["ids"][sid] = loaded_config[sid]
            timefile = os.path.join(folderLocation, sid, "EnhancedInputUserSettings.sav")
            if os.path.exists(timefile):
                timeofSID = os.path.getmtime(timefile)
                if timeofSID > timecomp:
                    timecomp = timeofSID
                    retVal["latest"] = sid
    try:
        with open(ConfigFile, 'w') as f:
            json.dump(retVal["ids"],
                f,
                indent=2,
            )
    except Exception as e:
        pass
    return retVal

def CreateProfile(Profile):
    if Profile == "":
        return False
    NewProfilePath = os.path.join(AllSavePath, Profile)
    if os.path.exists(NewProfilePath):
        return "Profile already exist"
    os.makedirs(NewProfilePath, exist_ok=True)
    return True

def DeleteProfile(Profile):
    if Profile == "":
        return False
    RemovedProfilePath = os.path.join(AllSavePath, Profile)
    for root, dirs, files in os.walk(RemovedProfilePath):
        os.chmod(root, stat.S_IWUSR)
        for d in dirs:
            if d == "Backup":
                continue
            dirsPath = os.path.join(RemovedProfilePath, d)
            for i in os.listdir(dirsPath):
                if i == "Backup":
                    os.chmod(os.path.join(dirsPath, i), stat.S_IWUSR)
            os.chmod(dirsPath, stat.S_IWUSR)
    shutil.rmtree(RemovedProfilePath)
    return True

def DuplicateProfile(Profile, NameOfCopy):
    profilePath = os.path.join(AllSavePath, Profile)
    CopyPath = os.path.join(AllSavePath, NameOfCopy)
    shutil.copytree(profilePath, CopyPath, dirs_exist_ok=True)

def RenameProfile(Profile, NewName):
    OldProfilePath = os.path.join(AllSavePath, Profile)
    NewProfilePath = os.path.join(AllSavePath, NewName)
    os.rename(OldProfilePath, NewProfilePath)

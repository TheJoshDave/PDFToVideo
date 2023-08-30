#SingleInstance Force
SetTitleMatchMode, 2
Global VideoFolder := A_ScriptDir "\Video\"
Global AudioFolder := A_ScriptDir "\Audio\"
Global ImagesFolder := A_ScriptDir "\Images\"
Global TextFolder := A_ScriptDir "\Text\"
Global ShortcutsFolder := A_ScriptDir "\Shortcuts\"
Global ApplicationsFolder := A_ScriptDir "\Applications\"
Global BatchFileTXT := A_ScriptDir "\BatchList.txt"
Global SettingsArray := {AudioSpeed : 10} ; SettingsArray["AudioSpeed"]
Global pythonFolder := "C:\Users\Dave\Desktop\Programming\GitHub\PDFToVideo\Scripts\"
#Include C:\Users\Dave\Desktop\Programming\GitHub\PDFToVideo\Scripts\TextToAudio.ahk
#Include C:\Users\Dave\Desktop\Programming\GitHub\PDFToVideo\Scripts\MakeDescription.ahk
#Include C:\Users\Dave\Desktop\Programming\GitHub\PDFToVideo\Scripts\GetFileData.ahk
return

;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
F2::Pause
XButton1::
	SetTimer, ChangeButtonNames, 50 
	MsgBox, 3, Choose Or Run, Would you like to choose a file or run the batch list?
	IfMsgBox Yes ; Makes batch TXT
	{
        FileSelectFile, FilePath, 3, %A_MyDocuments%, Choose File, (*.pdf; *.txt; *.mp4)
        FileAppend, % FilePath "`n", % BatchFileTXT
    }
	IfMsgBox No ; Executes batch TXT
	{
		Loop, Read, % BatchFileTXT
		{
			RunWithFilePath(A_LoopReadLine)
		}
		FileDelete, % BatchFileTXT
	}
return
XButton2::
	SetTimer, ChangeButtonNames2, 50
	MsgBox, 1, Easy format application, Please select the root folder.
	IfMsgBox Ok ; Makes batch TXT
	{
        FileSelectFolder, Path, %A_MyDocuments%, 3, Choose Folder
        MakeWorkingFolder(Path)
        EasyFormatApplication()
    }
return
;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

RunWithFilePath(FilePath) {
	MakeWorkingFolder(ParentFolder(ParentFolder(FilePath)))
	if InStr(FilePath, ".pdf")
		PDFToUnformated(FilePath) ; PDF -> Images + Text
	else if InStr(FilePath, ".txt")
		MakeVideo(FilePath) ; Text -> Audio -> Video
	else if InStr(FilePath, ".mp4")
		MakeDescription() ; Video -> Description
	else
		MsgBox, Unsupported file type :(
}
MakeWorkingFolder(Folder) {
	Global VideoFolder := Folder "\Video\"
	Global AudioFolder := Folder "\Audio\"
	Global ImagesFolder := Folder "\Images\"
	Global TextFolder := Folder "\Text\"
	FileCreateDir, % VideoFolder
	FileCreateDir, % AudioFolder
	FileCreateDir, % ImagesFolder
	FileCreateDir, % TextFolder
}
ParentFolder(Path) {
	return SubStr(Path, 1, InStr(SubStr(Path,1,-1), "\", 0, 0)-1)
}
ChangeButtonNames:
    ; waits for window
	IfWinNotExist, Choose Or Run
		return
	SetTimer, ChangeButtonNames, Off

	WinActivate ; set window to front
	ControlSetText, Button1, &Choose File ; change button name
	ControlSetText, Button2, &Run ; change button name
return
ChangeButtonNames2:
    ; waits for window
	IfWinNotExist, Easy format application
		return
	SetTimer, ChangeButtonNames2, Off

	WinActivate ; set window to front
	ControlSetText, Button1, &Choose Folder ; change button name
return

PDFToUnformated(FilePath) {
	MakeWorkingFolder(ParentFolder(FilePath)) ; Root folder = parent folder
	run, % "python " pythonFolder "PDFToImages.py " FilePath " " ImagesFolder ; images
	run, % "python " pythonFolder "PDFToTXT.py " FilePath " " TextFolder ; text
}
MakeVideo(FilePath) {
	FileRemoveDir, % A_AppData "\Balabolka\", 1
	FileRemoveDir, % A_AppData "\Hunspell\", 1
	FileCopyDir, % ApplicationsFolder "Hunspell\", % A_AppData "\Hunspell\", 1
	MakeWorkingFolder(ParentFolder(ParentFolder(FilePath))) ; Root folder = parent parent folder
	TextToAudio(FilePath) ; turns text to audio
	run, % "python " pythonFolder "AudioImageFFMPEG.py " ImagesFolder " " AudioFolder " " VideoFolder ; creates video segments then video
} ; only handles one txt file with pages seperated by double lines
EasyFormatApplication() {
    Loop, Files, %ImagesFolder%*.png
    {
        txt_filepath := TextFolder SubStr(A_LoopFileName, 1, 3) ".txt"
        mp3_filepath := AudioFolder SubStr(A_LoopFileName, 1, 3) ".mp3"
        Gui, New, Resize ToolWindow, Close when done
        Gui, Margin, 1, 1
        Gui, Add, Picture, w-1 h790 x0 y0, %A_LoopFileFullPath%
        Gui, Show, x0 y0 h790
        WinGetPos,,, width,, A

        run, % txt_filepath
        WinWait ahk_exe notepad.exe
        WinMove, ahk_exe notepad.exe,, %width%, 0, % 1920 - width, 1020

        WinWaitClose, Close when done
        WinClose, ahk_exe notepad.exe
        RunWait, % "python " pythonFolder "TTS.py " txt_filepath " " mp3_filepath
    }
    run, % "python " pythonFolder "AudioImageFFMPEG.py " ImagesFolder " " AudioFolder " " VideoFolder ; creates video segments then video
}
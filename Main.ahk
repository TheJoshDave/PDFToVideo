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

Global pythonFolder := "C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\"
; python C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\PDFToImages.py <pdf_filepath> <images_folder_filepath>
; python C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\PDFToTXT.py <pdf_filepath> <txt_output_filepath>
; python C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\AudioPlusImagesToVideo.py <images_folder_filepath> <audio_folder_filepath> <video_folder_filepath>
#Include TextToAudio.ahk
#Include MakeDescription.ahk
#Include GetFileData.ahk
return
/*
------------------------------------------------------------------------------------------------------------------------------------------------------
Outline:
Open main
	Run Program Beef or choose program inputs

Program Beef:
	Choose PDF [step 1] (root folder from parent folder)
		Make PNG's from PDF pages with python
		Make TXT from PDF text with python
Human formats text
	Choose TXT [step 3] (root folder from second parent folder)
		Make audio from TXT with Balabolka
		Make mp4 from audio + PNG's with python
	Choose mp4 [step 4] (root folder from second parent folder)
		Make description copypastas from user inputed values
------------------------------------------------------------------------------------------------------------------------------------------------------
*/

;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
F2::Pause
XButton1::
	SetTimer, ChangeButtonNames, 50 
	MsgBox, 3, Choose Or Run, Would you like to choose a file or run the batch list?
	IfMsgBox Yes
		MakeBatchTXT()
	IfMsgBox No
	{
		Loop, Read, % BatchFileTXT
		{
			RunWithFilePath(A_LoopReadLine)
		}
		FileDelete, % BatchFileTXT
	}
return
;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

MakeBatchTXT() {
	FileSelectFile, FilePath, 3, %A_MyDocuments%, Choose File, (*.pdf; *.txt; *.mp4)
	FileAppend, % FilePath "`n", % BatchFileTXT
}
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
}
ParentFolder(Path) {
	return SubStr(Path, 1, InStr(SubStr(Path,1,-1), "\", 0, 0)-1)
}
ChangeButtonNames: 
	IfWinNotExist, Choose Or Run
		return  ; Keep waiting for window
	SetTimer, ChangeButtonNames, Off ; stop waiting for window
	WinActivate ; set window to front
	ControlSetText, Button1, &Choose File ; change button name
	ControlSetText, Button2, &Run ; change button name
return

PDFToUnformated(FilePath) {
	MakeWorkingFolder(ParentFolder(FilePath)) ; creates root folder from pdf parent folder
	run, % "python " pythonFolder "PDFToImages.py " FilePath " " ImagesFolder ; images
	run, % "python " pythonFolder "PDFToTXT.py " FilePath " " TextFolder "Unformatted.txt" ; text
}
MakeVideo(FilePath) {
	FileRemoveDir, % A_AppData "\Balabolka\", 1
	FileRemoveDir, % A_AppData "\Hunspell\", 1
	FileCopyDir, % ApplicationsFolder "Hunspell\", % A_AppData "\Hunspell\", 1
	MakeWorkingFolder(ParentFolder(ParentFolder(FilePath))) ; creates root folder from txt second parent folder
	TextToAudio(FilePath) ; turns text to audio
	run, % "python " pythonFolder "AudioImageFFMPEG.py " ImagesFolder " " AudioFolder " " VideoFolder ; creates video segments then video
}

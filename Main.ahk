#SingleInstance Force
SetTitleMatchMode, 2
Global pythonFolder := "C:\Users\Dave\Desktop\Programming\GitHub\PDFToVideo\Scripts\"
Global PDFToImages := pythonFolder "\PDFToImages.py"
Global PDFToTXT := pythonFolder "\PDFToTXT.py"
Global TTS := pythonFolder "\TTS.py"
Global AudioImageFFMPEG := pythonFolder "\AudioImageFFMPEG.py"
return

;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
F2::Pause
XButton1::
	SetTimer, ChangeButtonNames, 50
	MsgBox, 3, Stage, 1. PDF->TXT+PNG`n2. Easy Format Application || TXT->MP3->MP4->Finish
	IfMsgBox Yes ; PDF->TXT+PNG
	{
        FileSelectFile, FilePath, 3, %A_MyDocuments%, Choose File, (*.pdf)
        run, % "python " PDFToImages " " FilePath ; images
        run, % "python " PDFToTXT " " FilePath ; text
    }
	IfMsgBox No ; Easy Format Application || TXT->MP3->MP4->Finish
	{
        SetTimer, ChangeButtonNames, 50
        MsgBox, 3, Stage, 1. Easy Format Application`n2. TXT->MP3->MP4->Finish
        IfMsgBox Yes ; Easy Format Application
        {
            EasyFormatApplication()
        }
        IfMsgBox No ; TXT->MP3->MP4->Finish
        {
            FileSelectFile, FilePath, 3, %A_MyDocuments%, Choose File, (*.pdf)
            RunWait, % "python " TTS " " FilePath
            run, % "python " AudioImageFFMPEG " " FilePath
        }
	}
return
;<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

ChangeButtonNames:
	IfWinNotExist, Stage
		return ; waits for window
	SetTimer, ChangeButtonNames, Off

	WinActivate ; set window to front
	ControlSetText, Button1, &1 ; change button name
	ControlSetText, Button2, &2 ; change button name
return

EasyFormatApplication() {
    FileSelectFolder, Path, %A_MyDocuments%, 3, Choose Folder
	ImagesFolder := Path "\Images\"
	AudioFolder := Path "\Audio\"
	TextFolder := Path "\Text\"

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
    }
}
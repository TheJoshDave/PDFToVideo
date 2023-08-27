TextToAudio(FilePath) {
	if WinExist("ahk_exe balabolka.exe")
		WinKill, ahk_exe balabolka.exe
	Run, %ShortcutsFolder%Balabolka.lnk %FilePath%
	WinWaitActive, Balabolka
	;opens balabolka
	
	
	While (!WinActive("ahk_class TSetForm")) {
		Send, +{F6}
		Sleep, 1000
	}
	Tab(11, true)
	Tab(3, false)
	Right(4)
	Tab(4, true)
	Send, {up}
	Tab(1, false)
	Send, {up}
	Tab(1, false)
	Loop, 6
		Send, {up}
	Send, {down}
	Tab(2, false)
	Send, 1000
	Tab(1, true)
	Tab(8, false)
	Tab(3, false)
	Loop, 30
		Send, {down}
	Send, {space}
	Tab(7, true)
	Tab(2, false)
	Loop, 30
		Send, {down}
	Loop, 20
		Send, ^!{left}
	Loop, % SettingsArray["AudioSpeed"]
		Send, ^!{right}
	;sets settings
	
	Send, ^{F8}
	WinWaitActive, ahk_class TSplitAndSaveForm
	SpiltPopup(AudioFolder)
	Tab(6, true)
	Tab(2, true)
	Tab(4, true)
	Tab(3, true)
	
	WinWait, ahk_class TSplitSavingForm
	While WinExist("ahk_class TSplitSavingForm")
		Sleep, 1000
	WinKill, ahk_exe balabolka.exe
}
SpiltPopup(Folder) {
	FileCreateDir, % Folder
	FileRemoveDir, % Folder, 1
	FileCreateDir, % Folder
	Send, % Folder
}
Tab(Times, EnterEnd) {
	Loop, %Times%
		Send, {tab}
	if EnterEnd
		Send, {space}
}
Right(Times) {
	Loop, %Times%
		Send, {right}
}
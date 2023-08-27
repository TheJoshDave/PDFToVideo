Global State := ""
Global Year := ""
Global Month := ""
Global Day := ""
MakeDescription() {
	
	Gui, New, -0xC00000 +Owner
	Gui, Add, Text, hwndControlID Center, Enter State
	SetSize(ControlID)
	Gui, Add, DropDownList, hwndControlID vState Choose1, Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming
	SetSize(ControlID)
	Gui, Add, Text, hwndControlID Center yp+50, Enter Date
	SetSize(ControlID)
	Gui, Add, Edit, hwndControlID Number Limit4 vYear, % A_YYYY
	SetSize(ControlID, "H2")
	GuiControlGet, OutputVar, Pos, % ControlID
	Gui, Add, Text, hwndControlID Center Y%OutputVarY% H%OutputVarH%, Year:
	SetSize(ControlID, "H1")
	Gui, Add, Edit, hwndControlID Number Limit2 vMonth, % A_MM
	SetSize(ControlID, "H2")
	GuiControlGet, OutputVar, Pos, % ControlID
	Gui, Add, Text, hwndControlID Center Y%OutputVarY% H%OutputVarH%, Month:
	SetSize(ControlID, "H1")
	Gui, Add, Edit, hwndControlID vDay Number Limit2, % A_DD
	SetSize(ControlID, "H2")
	GuiControlGet, OutputVar, Pos, % ControlID
	Gui, Add, Text, hwndControlID Center Y%OutputVarY% H%OutputVarH%, Day:
	SetSize(ControlID, "H1")
	Gui, Add, Button, hwndControlID gDescriptionComplete, Confirm
	SetSize(ControlID)
	Gui, Show, % "W" A_ScreenWidth/2, Make Description
	return
	DescriptionComplete:
		Gui, Submit
		DescriptionTXT()
	return
}
DescriptionTXT() {
	NumberToMonth := {1:" January"
	, 2:"February"
	, 3:"March"
	, 4:"April"
	, 5:"May"
	, 6:"June"
	, 7:"July"
	, 8:"August"
	, 9:"September"
	, 10:"October"
	, 11:"November"
	, 12:"December"}
	
	DesString := State " Driver Handbook - Audio - " Year
	SaveTXT(DesString, "Title")
	
	DesString := "The " State " Driver License Handbook - Audio - "
	if ((Month != "") && (Day != ""))
		DesString .= NumberToMonth[Month] " " Day ", "
	else if (Month != "")
		DesString .= NumberToMonth[Month] " "
	DesString .= Year
	DesString .= "`nDownload the handbook: `n"
	TotalAudioLength := 0
	Loop, Files, % AudioFolder "*.*"
	{
		PossibleHour := Mod(Floor(Floor(TotalAudioLength/60)/60), 24)
		PossibleMinute := Mod(Floor(TotalAudioLength/60), 60)
		PossibleSecond := Floor(Mod(TotalAudioLength, 60))
		DesString .= "`n"
		if PossibleHour
			DesString .= PossibleHour ":" SubStr("00" PossibleMinute, -1) ":" SubStr("00" PossibleSecond, -1)
		else if PossibleMinute
			DesString .= PossibleMinute ":" SubStr("00" PossibleSecond, -1)
		else
			DesString .= "0:" SubStr("00" PossibleSecond, -1)
		AudioLength := (SubStr(FGP_Value(A_LoopFileFullPath, "Length"), 1, 2)*60)+(SubStr(FGP_Value(A_LoopFileFullPath, "Length"), 4, 2)*60)+(SubStr(FGP_Value(A_LoopFileFullPath, "Length"), 7, 2))
		TotalAudioLength += AudioLength + 0.5
	}
	SaveTXT(DesString, "Description")
	
	DesString := "Audio, Sound, Audiobook, Driver, Driving, Drive, Road, License, Licensing, Test, Exam, Learn, Education, DMV, Permit" 
	DesString .= ", " State
	DesString .= ", " Year
	if (Month != "")
		DesString .= ", " NumberToMonth[Month]
	SaveTXT(DesString, "Tags")
}
SetSize(ControlHWND, Size := "", EdgeWidth := 10) {
	WindowSize := A_ScreenWidth/2
	GuiControl, Move, % ControlHWND, % (Size == "H1") 
? "W" WindowSize/2-EdgeWidth*2 " X" EdgeWidth : (Size == "H2") 
? "W" WindowSize/2-EdgeWidth*2 " X" WindowSize/2+EdgeWidth : "W" WindowSize-EdgeWidth*2 " X" EdgeWidth
}
SaveTXT(Stuff, Name) {
	FileDelete, % VideoFolder Name ".txt"
	FileAppend, % Stuff, % VideoFolder Name ".txt"
	Run, % "notepad.exe " VideoFolder Name ".txt"
}
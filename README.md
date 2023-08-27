# PDFToVideo
Outline:

---
    Main.ahk
        F2
            Pause
        
        XButton1 (BACK)
            Choose Files
                File selector popup
                Files are added to BatchList.txt
            Run (From BatchList.txt)
                PDF
                    Root folder = parent folder
                    Make PNG's from PDF pages with PDFToImages.py
                    Make TXT from PDF text with PDFToTXT.py
                TXT
                    Root folder = parent parent folder
                    Make audio from TXT with Balabolka # should be made with python tts
                    Make mp4 from audio + PNG's with AudioImageFFMPEG.py
                MP4
                    Root folder = parent parent folder
                    Make description/tags/title with MakeDescription.ahk # could be made with python
            Close
        
        XButton2 (FRONT)
            Easy format application
                Choose root folder
                Cancel
---
; vim: set commentstring=;\ %s:ts=4:
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

remainingTime = %1%

BlockInput, On
while remainingTime > 0 {
    sleep 100
    MouseMove, 0, 0
    remainingTime -= 100
}
BlockInput, Off

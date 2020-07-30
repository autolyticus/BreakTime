; vim: set commentstring=;\ %s:ts=4:
; vim: set commentstring=;\ %s:
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;delay := %1%
;;for n, param in A_Args  ; For each parameter:
;;{
;;    MsgBox Parameter number %n% is %param%.
;;}
;if delay is integer
;{
;    MsgBox You set delay = %delay% seconds
;    return
;}
;else
;{
;    MsgBox "%delay%" is not a valid number.
;    ; goSub, input
;}


BlockInput, On
Sleep % %1%
BlockInput, Off

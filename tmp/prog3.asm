format PE console

include "win32ax.inc"

entry _start

macro @convert_hex8 dst,val
{
        local .x

        repeat 4 ; 4 bytes
                .x = (val and (0x0F shl ((2 - %) shl 2))) shr ((2 - %) shl 2) or '0'

                if .x > '9'
                        .x = .x + 'A' - ':'
                end if

                store byte .x at dst+(%-1)
        end repeat
}

;===========================
; section data
;===========================

section ".data" data readable writeable
str_fmt:    db "%d",13,10,0
sysPause:   db "pause", 0
str_eax:    db "EAX: %d", 13, 10, 0
str_ebx:    db "EBX: %d", 13, 10, 0
str_ecx:    db "ECX: %d", 13, 10, 0
str_edx:    db "EDX: %d", 13, 10, 0
str_ebp:    db "EBP: %d", 13, 10, 0
str_esp:    db "ESP: %d", 13, 10, 0
str_esi:    db "ESI: %d", 13, 10, 0
str_edi:    db "EDI: %d", 13, 10, 0
str_eip:    db "EIP: %d", 13, 10, 0

str_hex:    dq 0
str_dec:    dq 0


;===========================
; section code
;===========================
section ".text" code readable executable

_start:
    push    ebp
    mov     ebp, esp

    mov     eax, 10
    mov     ecx, 10
    add     eax, ecx

    push    eax
    push    str_fmt
    call    [printf]
    add     esp, 8

    call    _dump_reg

    push    sysPause
    call    [system]
    add     esp, 4


    push    0

    mov     esp, ebp
    pop     ebp

    call [ExitProcess]

_dump_reg:
    push    ebp
    mov     ebp, esp

    mov     [str_dec], eax
    ;@convert_hex8 str_hex, 0xFF
    push    str_dec
    push    str_eax
    call    [printf]
    add     esp, 8

    push    ebx
    push    str_ebx
    call    [printf]
    add     esp, 8

    push    ecx
    push    str_ecx
    call    [printf]
    add     esp, 8

    push    edx
    push    str_edx
    call    [printf]
    add     esp, 8

    push    ebp
    push    str_ebp
    call    [printf]
    add     esp, 8

    push    esp
    push    str_esp
    call    [printf]
    add     esp, 8

    push    esi
    push    str_esi
    call    [printf]
    add     esp, 8

    push    edi
    push    str_edi
    call    [printf]
    add     esp, 8


    mov     esp, ebp
    pop     ebp

    ret



;================
;section import (win32)
;================
section ".idata" import data readable writeable

library \
    kernel32, "kernel32.dll", \
    msvcrt, "msvcrt.dll"
import \
    kernel32, \
        ExitProcess, "ExitProcess"
import \
    msvcrt, \
        printf, "printf", \
        scanf, "scanf", \
        getchar, "getchar", \
        putchar,'putchar',\
        system,'system'
; Source: ROMs\BattleCity (Japan).nes; exact revision unconfirmed.
; SHA-256: 166ec235b062aa337045832843e2916f96f12dcf08972ad747016dbe77db761c
; Mapper 0, 16 KiB PRG: CPU $C000-$FFFF, mirrored at $8000-$BFFF.
; CPU addresses below are not file offsets; the PRG starts at file offset $0010.
; PPU registers: https://bugzmanov.github.io/nes_ebook/chapter_6_1.html
; Interrupts: https://bugzmanov.github.io/nes_ebook/chapter_6_2.html

PPUCTRL EQU $2000
PPUMASK EQU $2001
PPUSTATUS EQU $2002
OAMADDR EQU $2003
PPUSCROLL EQU $2005
PPUADDR EQU $2006
PPUDATA EQU $2007
PPUCTRL_2010 EQU $2010                 ; mirror of PPUCTRL ($2000)
PPUCTRL_2020 EQU $2020                 ; mirror of PPUCTRL ($2000)
PPUSTATUS_2022 EQU $2022               ; mirror of PPUSTATUS ($2002)
PPUSCROLL_20DD EQU $20DD               ; mirror of PPUSCROLL ($2005)
PPUSCROLL_22DD EQU $22DD               ; mirror of PPUSCROLL ($2005)
PPUSCROLL_2315 EQU $2315               ; mirror of PPUSCROLL ($2005)
PPUSTATUS_2422 EQU $2422               ; mirror of PPUSTATUS ($2002)
PPUCTRL_2440 EQU $2440                 ; mirror of PPUCTRL ($2000)
PPUCTRL_24D0 EQU $24D0                 ; mirror of PPUCTRL ($2000)
OAMDATA_24D4 EQU $24D4                 ; mirror of OAMDATA ($2004)
PPUSCROLL_24DD EQU $24DD               ; mirror of PPUSCROLL ($2005)
PPUCTRL_2D20 EQU $2D20                 ; mirror of PPUCTRL ($2000)
PPUSTATUS_2D22 EQU $2D22               ; mirror of PPUSTATUS ($2002)
OAMDATA_2D44 EQU $2D44                 ; mirror of OAMDATA ($2004)
OAMDATA_2DB4 EQU $2DB4                 ; mirror of OAMDATA ($2004)
PPUADDR_2E2E EQU $2E2E                 ; mirror of PPUADDR ($2006)
PPUCTRL_2E40 EQU $2E40                 ; mirror of PPUCTRL ($2000)
PPUDATA_307F EQU $307F                 ; mirror of PPUDATA ($2007)
PPUDATA_32FF EQU $32FF                 ; mirror of PPUDATA ($2007)
OAMADDR_334B EQU $334B                 ; mirror of OAMADDR ($2003)
PPUSCROLL_338D EQU $338D               ; mirror of PPUSCROLL ($2005)
OAMADDR_3393 EQU $3393                 ; mirror of OAMADDR ($2003)
OAMADDR_33D3 EQU $33D3                 ; mirror of OAMADDR ($2003)
PPUCTRL_33D8 EQU $33D8                 ; mirror of PPUCTRL ($2000)
PPUSCROLL_33DD EQU $33DD               ; mirror of PPUSCROLL ($2005)
PPUADDR_33DE EQU $33DE                 ; mirror of PPUADDR ($2006)
PPUADDR_33EE EQU $33EE                 ; mirror of PPUADDR ($2006)
OAMADDR_34C3 EQU $34C3                 ; mirror of OAMADDR ($2003)
PPUSCROLL_34DD EQU $34DD               ; mirror of PPUSCROLL ($2005)
PPUSTATUS_36D2 EQU $36D2               ; mirror of PPUSTATUS ($2002)
OAMADDR_36E3 EQU $36E3                 ; mirror of OAMADDR ($2003)
PPUSCROLL_374D EQU $374D               ; mirror of PPUSCROLL ($2005)
PPUMASK_3931 EQU $3931                 ; mirror of PPUMASK ($2001)
PPUCTRL_3A78 EQU $3A78                 ; mirror of PPUCTRL ($2000)
OAMADDR_3B33 EQU $3B33                 ; mirror of OAMADDR ($2003)
OAMADDR_3BD3 EQU $3BD3                 ; mirror of OAMADDR ($2003)
OAMDATA_3D44 EQU $3D44                 ; mirror of OAMDATA ($2004)
PPUSCROLL_3D4D EQU $3D4D               ; mirror of PPUSCROLL ($2005)
PPUSCROLL_3DAD EQU $3DAD               ; mirror of PPUSCROLL ($2005)
OAMDATA_3DD4 EQU $3DD4                 ; mirror of OAMDATA ($2004)
PPUSCROLL_3DDD EQU $3DDD               ; mirror of PPUSCROLL ($2005)
PULSE1_CTRL EQU $4000
OAMDMA EQU $4014
APU_STATUS EQU $4015                   ; read APU status, write channel enables
JOY1_STROBE EQU $4016                  ; read controller 1, write controller strobe
JOY2_APU_FRAME EQU $4017               ; read controller 2, write APU frame counter
L_0D20 EQU $0D20
L_1010 EQU $1010
L_1020 EQU $1020
L_2010 EQU PPUCTRL_2010
L_2020 EQU PPUCTRL_2020
L_307F EQU PPUDATA_307F
L_3931 EQU PPUMASK_3931
L_3B33 EQU OAMADDR_3B33
L_4157 EQU $4157
L_4552 EQU $4552
L_4C50 EQU $4C50
L_4F4C EQU $4F4C
L_4F4E EQU $4F4E
L_5220 EQU $5220
L_5250 EQU $5250
L_533B EQU $533B
L_5420 EQU $5420
L_544C EQU $544C
L_549C EQU $549C
L_5941 EQU $5941
L_5942 EQU $5942
L_5A4F EQU $5A4F
L_8101 EQU $8101                       ; mirror of $C101
L_82EE EQU $82EE                       ; mirror of $C2EE
L_84DD EQU $84DD                       ; mirror of $C4DD
L_88D4 EQU $88D4                       ; mirror of $C8D4
L_88DD EQU $88DD                       ; mirror of $C8DD
L_88ED EQU $88ED                       ; mirror of $C8ED
L_89BD EQU $89BD                       ; mirror of $C9BD
L_89DD EQU $89DD                       ; mirror of $C9DD
L_8B7D EQU $8B7D                       ; mirror of $CB7D
L_8D4D EQU $8D4D                       ; mirror of $CD4D
L_8D88 EQU $8D88                       ; mirror of $CD88
L_8D8D EQU $8D8D                       ; mirror of $CD8D
L_8D9D EQU $8D9D                       ; mirror of $CD9D
L_8DD4 EQU $8DD4                       ; mirror of $CDD4
L_8DD8 EQU $8DD8                       ; mirror of $CDD8
L_8DDA EQU $8DDA                       ; mirror of $CDDA
L_9449 EQU $9449                       ; mirror of $D449
L_944D EQU $944D                       ; mirror of $D44D
L_9494 EQU $9494                       ; mirror of $D494
L_94DD EQU $94DD                       ; mirror of $D4DD
L_97D5 EQU $97D5                       ; mirror of $D7D5
L_999D EQU $999D                       ; mirror of $D99D
L_99B4 EQU $99B4                       ; mirror of $D9B4
L_99B9 EQU $99B9                       ; mirror of $D9B9
L_99DD EQU $99DD                       ; mirror of $D9DD
L_99EC EQU $99EC                       ; mirror of $D9EC
L_9B9B EQU $9B9B                       ; mirror of $DB9B
L_9BBB EQU $9BBB                       ; mirror of $DBBB
L_9BD9 EQU $9BD9                       ; mirror of $DBD9
L_9BDD EQU $9BDD                       ; mirror of $DBDD
L_9CCD EQU $9CCD                       ; mirror of $DCCD
L_9D49 EQU $9D49                       ; mirror of $DD49
L_9D4D EQU $9D4D                       ; mirror of $DD4D
L_9D8D EQU $9D8D                       ; mirror of $DD8D
L_9D9D EQU $9D9D                       ; mirror of $DD9D
L_9DAA EQU $9DAA                       ; mirror of $DDAA
L_9DBB EQU $9DBB                       ; mirror of $DDBB
L_9DBD EQU $9DBD                       ; mirror of $DDBD
L_9DD4 EQU $9DD4                       ; mirror of $DDD4
L_9DD5 EQU $9DD5                       ; mirror of $DDD5
L_9DD9 EQU $9DD9                       ; mirror of $DDD9
L_9DDB EQU $9DDB                       ; mirror of $DDDB
L_9DDD EQU $9DDD                       ; mirror of $DDDD
L_A2D8 EQU $A2D8                       ; mirror of $E2D8
L_A4AA EQU $A4AA                       ; mirror of $E4AA
L_A978 EQU $A978                       ; mirror of $E978
L_A9CA EQU $A9CA                       ; mirror of $E9CA
L_AA44 EQU $AA44                       ; mirror of $EA44
L_AA9D EQU $AA9D                       ; mirror of $EA9D
L_AAA4 EQU $AAA4                       ; mirror of $EAA4
L_AAAA EQU $AAAA                       ; mirror of $EAAA
L_AAAD EQU $AAAD                       ; mirror of $EAAD
L_AABB EQU $AABB                       ; mirror of $EABB
L_AADD EQU $AADD                       ; mirror of $EADD
L_AB9B EQU $AB9B                       ; mirror of $EB9B
L_ABBA EQU $ABBA                       ; mirror of $EBBA
L_ABDD EQU $ABDD                       ; mirror of $EBDD
L_ADAA EQU $ADAA                       ; mirror of $EDAA
L_ADAB EQU $ADAB                       ; mirror of $EDAB
L_ADDA EQU $ADDA                       ; mirror of $EDDA
L_ADDD EQU $ADDD                       ; mirror of $EDDD
L_B1D1 EQU $B1D1                       ; mirror of $F1D1
L_B44B EQU $B44B                       ; mirror of $F44B
L_B44D EQU $B44D                       ; mirror of $F44D
L_B4BB EQU $B4BB                       ; mirror of $F4BB
L_B4DB EQU $B4DB                       ; mirror of $F4DB
L_B4DD EQU $B4DD                       ; mirror of $F4DD
L_B5D6 EQU $B5D6                       ; mirror of $F5D6
L_B6DD EQU $B6DD                       ; mirror of $F6DD
L_B8DD EQU $B8DD                       ; mirror of $F8DD
L_B99B EQU $B99B                       ; mirror of $F99B
L_B9BD EQU $B9BD                       ; mirror of $F9BD
L_B9DD EQU $B9DD                       ; mirror of $F9DD
L_BABB EQU $BABB                       ; mirror of $FABB
L_BB04 EQU $BB04                       ; mirror of $FB04
L_BB4B EQU $BB4B                       ; mirror of $FB4B
L_BB6B EQU $BB6B                       ; mirror of $FB6B
L_BB8B EQU $BB8B                       ; mirror of $FB8B
L_BB99 EQU $BB99                       ; mirror of $FB99
L_BBAA EQU $BBAA                       ; mirror of $FBAA
L_BBAD EQU $BBAD                       ; mirror of $FBAD
L_BBBB EQU $BBBB                       ; mirror of $FBBB
L_BBBD EQU $BBBD                       ; mirror of $FBBD
L_BBCC EQU $BBCC                       ; mirror of $FBCC
L_BBD3 EQU $BBD3                       ; mirror of $FBD3
L_BBD4 EQU $BBD4                       ; mirror of $FBD4
L_BBDB EQU $BBDB                       ; mirror of $FBDB
L_BBDD EQU $BBDD                       ; mirror of $FBDD
L_BD04 EQU $BD04                       ; mirror of $FD04
L_BD4D EQU $BD4D                       ; mirror of $FD4D
L_BD99 EQU $BD99                       ; mirror of $FD99
L_BD9B EQU $BD9B                       ; mirror of $FD9B
L_BDBB EQU $BDBB                       ; mirror of $FDBB
L_BDBD EQU $BDBD                       ; mirror of $FDBD
L_BDCB EQU $BDCB                       ; mirror of $FDCB
L_BDD8 EQU $BDD8                       ; mirror of $FDD8
L_BDDB EQU $BDDB                       ; mirror of $FDDB
L_BDDD EQU $BDDD                       ; mirror of $FDDD
L_CDCC EQU $CDCC
L_D36A EQU $D36A
L_D3A3 EQU $D3A3
L_D3B4 EQU $D3B4
L_D415 EQU $D415
L_D4BD EQU $D4BD
L_D57F EQU $D57F
L_DD0D EQU $DD0D
L_E4BF EQU $E4BF
L_E82C EQU $E82C
L_E8DC EQU $E8DC
L_EDC2 EQU $EDC2
L_EDDF EQU $EDDF
L_EE9A EQU $EE9A
L_EEDC EQU $EEDC
L_F130 EQU $F130
L_F137 EQU $F137
L_F2BC EQU $F2BC
L_F339 EQU $F339
L_F369 EQU $F369
L_F439 EQU $F439
L_F4B9 EQU $F4B9
L_F4C9 EQU $F4C9
L_F953 EQU $F953
START EQU $C070
IRQ EQU $C070

; RAM variables.
; PpuPageOffset ($0005): Added to a RAM source page to form the PPU destination page in $D771.
; InitGameState ($D491) sets $1C or $24; other values and users are not yet fully traced.
PpuPageOffset EQU $05
; PpuQueueEnd ($000C): End offset of queued PPU writes starting at $0180; $00 means the queue is empty.
; InitGameState ($D491) clears it; $D6B3 advances it and NMI ($D400) drains it through $D8FD.
PpuQueueEnd EQU $0C
; OamIndex ($000D): Byte offset into the shadow OAM buffer at $0200.
; InitGameState ($D491) sets $00; HideSprites ($DA93) sets $04 and $DA2B uses it for sprite writes.
OamIndex EQU $0D
; OamStep ($000E): Signed byte added to OamIndex ($000D) by $DA2B.
; InitGameState ($D491) sets $04; HideSprites ($DA93) negates it to $FC (-4). Other values are untraced.
OamStep EQU $0E
; PaletteReq ($004D): Background palette request; values with bit 7 set are skipped by NMI ($D400).
; InitGameState ($D491) and $D50E set $FF; nonnegative values select a palette, with valid indices untraced.
PaletteReq EQU $4D
; ScrollY ($004F): Vertical scroll byte written to PPUSCROLL by NMI ($D400).
; ResetEntry ($C070) clears it; $C7AB also changes it. Other values and users are not yet analyzed.
ScrollY EQU $4F
; PpuCtrlBits ($0050): Bits ORed with $B0 and written to PPUCTRL by NMI ($D400).
; ResetEntry ($C070) writes $00; $C9C0 writes $02. Other values and users are not yet analyzed.
PpuCtrlBits EQU $50
; PpuDataOffset ($0060): Offset added to selected data bytes by $D6DD and $D8D2.
; InitGameState ($D491) sets $00; other values and users are not yet fully traced.
PpuDataOffset EQU $60
; StringTrim ($006B): Controls how far $D934 steps back after finding a $FF terminator.
; InitGameState ($D491) sets $00; $01 is also written elsewhere. Other values and users are untraced.
StringTrim EQU $6B
; PauseFlag ($006D): Likely pause state; $C1F9 toggles $00/$01 and $EA7E uses it to select audio processing.
; InitGameState ($D491) sets $00; the complete range and other users are not yet traced.
PauseFlag EQU $6D
; TileAttrBits ($006E): Bits ORed into a shadow OAM attribute when $DA2B reads $22 from its indirect source.
; InitGameState ($D491) sets $20; other values and users are not yet fully traced.
TileAttrBits EQU $6E
; OptionIndex ($0083): Selector used as a jump-table index at $CA58; $C9C0 cycles it through $00-$02.
; InitGameState ($D491) sets $00 when the RAM marker differs; other values and users are untraced.
OptionIndex EQU $83

; CreditsText ($C000-$C06F): ASCII text with CR/LF separators and space padding, not a null-terminated string.
; The 16 bytes at $C040 are also copied to and compared with RAM $0110-$011F by $D4E3 and $D4EF.
CreditsText:
$C000: 43 4F 50 59 52 49 47 48 54 20 31 39 38 31 20 31  db "COPYRIGHT 1981 1"
$C010: 39 38 35 20 4E 41 4D 43 4F 20 4C 54 44 2E 0D 0A  db "985 NAMCO LTD.", $0D, $0A
$C020: 41 4C 4C 20 52 49 47 48 54 53 20 52 45 53 45 52  db "ALL RIGHTS RESER"
$C030: 56 45 44 20 20 20 20 20 20 20 20 20 20 20 0D 0A  db "VED           ", $0D, $0A
$C040: 52 59 4F 55 49 54 49 20 4F 4F 4B 55 42 4F 20 20  db "RYOUITI OOKUBO  "
$C050: 54 41 4B 45 46 55 4D 49 20 48 59 4F 55 44 4F 55  db "TAKEFUMI HYOUDOU"
$C060: 4A 55 4E 4B 4F 20 4F 5A 41 57 41 20 20 20 20 20  db "JUNKO OZAWA     "

; ResetEntry ($C070): Reset and IRQ/BRK entry; initialize the machine and enter a repeating call sequence.
; Inputs: CPU reset or IRQ/BRK; no explicit parameters. Output: transfers control to MainLoop ($C09C).
ResetEntry:
    ; Mask IRQs, request PPUCTRL $10, and clear the decimal flag; NES arithmetic is binary regardless of D.
    ; The PPU can ignore the PPUCTRL write during power-up warm-up. $10 selects background pattern table $1000.
    $C070: 78        SEI
    $C071: A9 10     LDA #$10
    $C073: 8D 00 20  STA PPUCTRL       ; PPUCTRL ($2000): NMI generation bit clear
    $C076: D8        CLD
    $C077: A2 02     LDX #$02

    ; Wait for vblank flag. Reading PPUSTATUS clears its vblank flag, so the second pass waits for another set.
WaitVblank:
    $C079: AD 02 20  LDA PPUSTATUS     ; PPUSTATUS ($2002), bit 7 is vblank
    $C07C: 10 FB     BPL WaitVblank    ; WaitVblank ($C079)
    $C07E: A9 06     LDA #$06
    $C080: 8D 01 20  STA PPUMASK       ; PPUMASK ($2001): disable background and sprite rendering if accepted
    $C083: CA        DEX
    $C084: D0 F3     BNE WaitVblank    ; WaitVblank ($C079)

    ; Initialize the stack, then initialize RAM, video buffers, and audio.
    $C086: A2 7F     LDX #$7F
    $C088: 9A        TXS
    $C089: 20 91 D4  JSR InitGameState ; InitGameState ($D491)

    ; Clear the scroll and PPU control variables, then synchronize with vblank and enable PPU NMIs.
    $C08C: A9 00     LDA #$00
    $C08E: 85 4F     STA ScrollY       ; ScrollY ($004F)
    $C090: 85 50     STA PpuCtrlBits   ; PpuCtrlBits ($0050)
    $C092: 20 67 D4  JSR EnablePpuNmi  ; EnablePpuNmi ($D467)

    ; This setup can also be entered from $C292; the purpose of $004B is not yet known.
RestartSetup:
L_C095:
    $C095: 20 7F D1  JSR $D17F
    $C098: A9 00     LDA #$00
    $C09A: 85 4B     STA $4B

    ; Call the following routines in sequence and repeat; their full behavior is not yet analyzed.
    ; Some calls can transfer control directly to $C0A2 instead of returning normally.
MainLoop:
    $C09C: 20 6A D1  JSR $D16A
    $C09F: 20 AB C7  JSR $C7AB

    ; Other code can also resume the sequence here.
LoopContinue:
L_C0A2:
    $C0A2: 20 C0 C9  JSR $C9C0
    $C0A5: 20 B5 C3  JSR $C3B5
    $C0A8: 20 1D C4  JSR $C41D
    $C0AB: 4C 9C C0  JMP MainLoop      ; MainLoop ($C09C)
L_C0AE:
$C0AE: A5 4B     LDA $4B
$C0B0: D0 0C     BNE L_C0BE
$C0B2: 20 70 D4  JSR L_D470
$C0B5: 20 B0 C9  JSR L_C9B0
$C0B8: 20 B4 D7  JSR L_D7B4
$C0BB: 20 67 D4  JSR L_D467
L_C0BE:
$C0BE: 20 13 E4  JSR L_E413
$C0C1: A9 10     LDA #$10
$C0C3: 85 90     STA $90
$C0C5: A9 18     LDA #$18
$C0C7: 85 98     STA $98
$C0C9: A9 84     LDA #$84
$C0CB: 85 A0     STA $A0
$C0CD: A9 00     LDA #$00
$C0CF: 85 A8     STA $A8
$C0D1: 85 6E     STA $6E
$C0D3: 85 B0     STA $B0
$C0D5: 85 81     STA $81
$C0D7: 85 7B     STA $7B
$C0D9: 85 5C     STA $5C
$C0DB: 85 4F     STA $4F
$C0DD: 85 50     STA $50
$C0DF: 85 6F     STA $6F
$C0E1: 85 70     STA $70
$C0E3: A5 4B     LDA $4B
$C0E5: D0 03     BNE L_C0EA
$C0E7: 20 F5 CA  JSR L_CAF5
L_C0EA:
$C0EA: 20 F6 D8  JSR L_D8F6
$C0ED: 20 D2 C6  JSR L_C6D2
$C0F0: 20 D0 C8  JSR L_C8D0
$C0F3: A5 0B     LDA $0B
$C0F5: 29 10     AND #$10
$C0F7: F0 03     BEQ L_C0FC
$C0F9: 20 A6 DE  JSR L_DEA6
L_C0FC:
$C0FC: A5 06     LDA $06
$C0FE: 29 F0     AND #$F0
$C100: D0 3C     BNE L_C13E
$C102: A5 08     LDA $08
$C104: 29 01     AND #$01
$C106: F0 18     BEQ L_C120
$C108: A5 81     LDA $81
$C10A: D0 05     BNE L_C111
$C10C: E6 81     INC $81
$C10E: 4C 44 C1  JMP L_C144
L_C111:
$C111: E6 5C     INC $5C
$C113: A5 5C     LDA $5C
$C115: C9 0E     CMP #$0E
$C117: D0 2B     BNE L_C144
$C119: A9 00     LDA #$00
$C11B: 85 5C     STA $5C
$C11D: 4C 44 C1  JMP L_C144
L_C120:
$C120: A5 08     LDA $08
$C122: 29 02     AND #$02
$C124: F0 18     BEQ L_C13E
$C126: A5 81     LDA $81
$C128: D0 05     BNE L_C12F
$C12A: E6 81     INC $81
$C12C: 4C 44 C1  JMP L_C144
L_C12F:
$C12F: C6 5C     DEC $5C
$C131: A5 5C     LDA $5C
$C133: C9 FF     CMP #$FF
$C135: D0 0D     BNE L_C144
$C137: A9 0D     LDA #$0D
$C139: 85 5C     STA $5C
$C13B: 4C 44 C1  JMP L_C144
L_C13E:
$C13E: A5 06     LDA $06
$C140: 29 03     AND #$03
$C142: F0 03     BEQ L_C147
L_C144:
$C144: 20 C6 C6  JSR L_C6C6
L_C147:
$C147: A5 08     LDA $08
$C149: 29 08     AND #$08
$C14B: D0 03     BNE L_C150
$C14D: 4C EA C0  JMP L_C0EA
L_C150:
$C150: A9 20     LDA #$20
$C152: 85 6E     STA $6E
$C154: E6 4B     INC $4B
$C156: 4C A2 C0  JMP L_C0A2
L_C159:
$C159: 20 F6 D8  JSR L_D8F6
$C15C: 20 51 EA  JSR L_EA51
$C15F: A9 1C     LDA #$1C
$C161: 85 05     STA $05
$C163: A9 00     LDA #$00
$C165: 85 4F     STA $4F
$C167: 85 50     STA $50
$C169: 85 6D     STA $6D
$C16B: A9 04     LDA #$04
$C16D: 85 4D     STA $4D
$C16F: 20 90 CC  JSR L_CC90
L_C172:
$C172: 20 91 CA  JSR L_CA91
$C175: A5 4C     LDA $4C
$C177: D0 4C     BNE L_C1C5
$C179: A5 08     LDA $08
$C17B: 29 08     AND #$08
$C17D: D0 46     BNE L_C1C5
$C17F: A5 08     LDA $08
$C181: 29 01     AND #$01
$C183: D0 0C     BNE L_C191
$C185: A5 06     LDA $06
$C187: 29 01     AND #$01
$C189: F0 19     BEQ L_C1A4
$C18B: A5 0B     LDA $0B
$C18D: 29 07     AND #$07
$C18F: D0 13     BNE L_C1A4
L_C191:
$C191: A9 00     LDA #$00
$C193: 85 0B     STA $0B
$C195: E6 85     INC $85
$C197: A5 85     LDA $85
$C199: C9 24     CMP #$24
$C19B: D0 D5     BNE L_C172
$C19D: A9 23     LDA #$23
$C19F: 85 85     STA $85
$C1A1: 4C 72 C1  JMP L_C172
L_C1A4:
$C1A4: A5 08     LDA $08
$C1A6: 29 02     AND #$02
$C1A8: D0 0C     BNE L_C1B6
$C1AA: A5 06     LDA $06
$C1AC: 29 02     AND #$02
$C1AE: F0 C2     BEQ L_C172
$C1B0: A5 0B     LDA $0B
$C1B2: 29 07     AND #$07
$C1B4: D0 BC     BNE L_C172
L_C1B6:
$C1B6: A9 00     LDA #$00
$C1B8: 85 0B     STA $0B
$C1BA: C6 85     DEC $85
$C1BC: D0 B4     BNE L_C172
$C1BE: A9 01     LDA #$01
$C1C0: 85 85     STA $85
$C1C2: 4C 72 C1  JMP L_C172
L_C1C5:
$C1C5: A9 01     LDA #$01
$C1C7: 8D 01 03  STA $0301
$C1CA: 8D 02 03  STA $0302
$C1CD: 8D 03 03  STA $0303
$C1D0: A5 4B     LDA $4B
$C1D2: D0 0E     BNE L_C1E2
$C1D4: 20 B0 C9  JSR L_C9B0
$C1D7: A5 85     LDA $85
$C1D9: 20 00 F0  JSR L_F000
$C1DC: 20 F5 CA  JSR L_CAF5
$C1DF: 4C E5 C1  JMP L_C1E5
L_C1E2:
$C1E2: 20 5D CB  JSR L_CB5D
L_C1E5:
$C1E5: A9 00     LDA #$00
$C1E7: 85 0C     STA $0C
$C1E9: 20 27 CC  JSR L_CC27
$C1EC: 20 B2 CC  JSR L_CCB2
$C1EF: A9 00     LDA #$00
$C1F1: 85 4D     STA $4D
$C1F3: 20 F6 D8  JSR L_D8F6
$C1F6: 20 31 C3  JSR L_C331
L_C1F9:
$C1F9: 20 F6 D8  JSR L_D8F6
$C1FC: A5 6D     LDA $6D
$C1FE: D0 03     BNE L_C203
$C200: 20 E6 C2  JSR L_C2E6
L_C203:
$C203: 20 3B E2  JSR L_E23B
$C206: 20 D8 E0  JSR L_E0D8
$C209: 20 A6 DE  JSR L_DEA6
$C20C: A5 08     LDA $08
$C20E: 29 08     AND #$08
$C210: F0 09     BEQ L_C21B
$C212: A9 01     LDA #$01
$C214: 45 6D     EOR $6D
$C216: 85 6D     STA $6D
$C218: 8D 00 03  STA $0300
L_C21B:
$C21B: 20 F9 C8  JSR L_C8F9
$C21E: 20 28 C7  JSR L_C728
$C221: F0 D6     BEQ L_C1F9
$C223: A9 00     LDA #$00
$C225: 85 0A     STA $0A
$C227: 85 0B     STA $0B
$C229: 8D 11 03  STA $0311
$C22C: 8D 12 03  STA $0312
$C22F: AD 08 01  LDA $0108
$C232: F0 04     BEQ L_C238
$C234: A9 FE     LDA #$FE
$C236: 85 0A     STA $0A
L_C238:
$C238: 20 F6 D8  JSR L_D8F6
$C23B: 20 A2 C2  JSR L_C2A2
$C23E: 20 E6 C2  JSR L_C2E6
$C241: 20 3B E2  JSR L_E23B
$C244: 20 A6 DE  JSR L_DEA6
$C247: 20 D8 E0  JSR L_E0D8
$C24A: 20 1D C3  JSR L_C31D
$C24D: A5 0A     LDA $0A
$C24F: C9 02     CMP #$02
$C251: D0 E5     BNE L_C238
$C253: 20 51 EA  JSR L_EA51
$C256: 20 D4 CC  JSR L_CCD4
$C259: E6 85     INC $85
$C25B: A5 85     LDA $85
$C25D: C9 47     CMP #$47
$C25F: D0 08     BNE L_C269
$C261: A9 01     LDA #$01
$C263: 85 85     STA $85
$C265: A9 00     LDA #$00
$C267: 85 46     STA $46
L_C269:
$C269: A5 85     LDA $85
$C26B: C9 24     CMP #$24
$C26D: D0 04     BNE L_C273
$C26F: A9 01     LDA #$01
$C271: 85 46     STA $46
L_C273:
$C273: A5 51     LDA $51
$C275: 18        CLC
$C276: 65 52     ADC $52
$C278: F0 09     BEQ L_C283
$C27A: A5 68     LDA $68
$C27C: C9 80     CMP #$80
$C27E: D0 03     BNE L_C283
$C280: 4C 59 C1  JMP L_C159
L_C283:
$C283: 20 D9 C5  JSR L_C5D9
$C286: 20 7D D9  JSR L_D97D
$C289: 98        TYA
$C28A: F0 06     BEQ L_C292
$C28C: 20 4B C4  JSR L_C44B
$C28F: 20 95 C2  JSR L_C295
L_C292:
$C292: 4C 95 C0  JMP L_C095
L_C295:
$C295: 20 70 D4  JSR L_D470
$C298: 20 7E D4  JSR L_D47E
$C29B: 20 B4 D7  JSR L_D7B4
$C29E: 20 67 D4  JSR L_D467
$C2A1: 60        RTS
L_C2A2:
$C2A2: A5 68     LDA $68
$C2A4: C9 80     CMP #$80
$C2A6: F0 0A     BEQ L_C2B2
$C2A8: A9 00     LDA #$00
$C2AA: 85 06     STA $06
$C2AC: 85 07     STA $07
$C2AE: 85 08     STA $08
$C2B0: 85 09     STA $09
L_C2B2:
$C2B2: 60        RTS
L_C2B3:
$C2B3: A2 15     LDX #$15
$C2B5: 20 FE D9  JSR L_D9FE
$C2B8: A2 1D     LDX #$1D
$C2BA: 20 FE D9  JSR L_D9FE
L_C2BD:
$C2BD: A9 00     LDA #$00
$C2BF: 8D 01 01  STA $0101
$C2C2: 8D 02 01  STA $0102
$C2C5: A9 00     LDA #$00
$C2C7: 85 66     STA $66
$C2C9: 85 67     STA $67
$C2CB: 85 4C     STA $4C
$C2CD: A9 03     LDA #$03
$C2CF: 85 51     STA $51
$C2D1: 85 52     STA $52
$C2D3: 85 6A     STA $6A
$C2D5: A5 83     LDA $83
$C2D7: D0 04     BNE L_C2DD
$C2D9: A9 00     LDA #$00
$C2DB: 85 52     STA $52
L_C2DD:
$C2DD: A9 01     LDA #$01
$C2DF: 85 85     STA $85
$C2E1: A9 00     LDA #$00
$C2E3: 85 46     STA $46
$C2E5: 60        RTS
L_C2E6:
$C2E6: 20 81 E1  JSR L_E181
$C2E9: 20 75 DB  JSR L_DB75
$C2EC: 20 F1 DB  JSR L_DBF1
$C2EF: 20 FA E1  JSR L_E1FA
$C2F2: 20 2E E0  JSR L_E02E
$C2F5: 20 A9 E2  JSR L_E2A9
$C2F8: 20 7C E2  JSR L_E27C
$C2FB: 20 22 E1  JSR L_E122
$C2FE: 20 62 E1  JSR L_E162
$C301: 20 48 DB  JSR L_DB48
$C304: 20 04 E6  JSR L_E604
$C307: 20 10 E9  JSR L_E910
$C30A: 20 0C E7  JSR L_E70C
$C30D: 20 72 E9  JSR L_E972
$C310: 20 72 C9  JSR L_C972
$C313: 20 0B DB  JSR L_DB0B
$C316: 20 C8 C7  JSR L_C7C8
$C319: 20 1D C3  JSR L_C31D
$C31C: 60        RTS
L_C31D:
$C31D: A5 0B     LDA $0B
$C31F: 29 3F     AND #$3F
$C321: F0 09     BEQ L_C32C
$C323: C9 20     CMP #$20
$C325: D0 09     BNE L_C330
$C327: A9 01     LDA #$01
$C329: 85 4D     STA $4D
$C32B: 60        RTS
L_C32C:
$C32C: A9 02     LDA #$02
$C32E: 85 4D     STA $4D
L_C330:
$C330: 60        RTS
L_C331:
$C331: 20 09 E4  JSR L_E409
$C334: 20 13 E4  JSR L_E413
$C337: A9 F0     LDA #$F0
$C339: 8D 06 01  STA $0106
$C33C: A9 00     LDA #$00
$C33E: 8D 08 01  STA $0108
$C341: A5 51     LDA $51
$C343: F0 05     BEQ L_C34A
$C345: A2 00     LDX #$00
$C347: 20 63 E3  JSR L_E363
L_C34A:
$C34A: A5 52     LDA $52
$C34C: F0 05     BEQ L_C353
$C34E: A2 01     LDX #$01
$C350: 20 63 E3  JSR L_E363
L_C353:
$C353: A9 14     LDA #$14
$C355: 85 7F     STA $7F
$C357: 85 80     STA $80
$C359: A9 00     LDA #$00
$C35B: 85 8F     STA $8F
$C35D: 85 0A     STA $0A
$C35F: 85 4B     STA $4B
$C361: 85 45     STA $45
$C363: 85 6F     STA $6F
$C365: 85 70     STA $70
$C367: 85 89     STA $89
$C369: 85 8A     STA $8A
$C36B: 85 82     STA $82
$C36D: 85 86     STA $86
$C36F: 8D 00 01  STA $0100
$C372: 85 6A     STA $6A
$C374: 20 1E C7  JSR L_C71E
$C377: 20 C0 C8  JSR L_C8C0
$C37A: 20 F6 D8  JSR L_D8F6
$C37D: 20 30 C8  JSR L_C830
$C380: 20 59 C8  JSR L_C859
$C383: 20 2B E4  JSR L_E42B
$C386: A9 80     LDA #$80
$C388: 85 68     STA $68
$C38A: A9 01     LDA #$01
$C38C: 8D 12 03  STA $0312
$C38F: 85 4C     STA $4C
$C391: A5 46     LDA $46
$C393: C9 01     CMP #$01
$C395: D0 05     BNE L_C39C
$C397: A9 23     LDA #$23
$C399: 4C 9E C3  JMP L_C39E
L_C39C:
$C39C: A5 85     LDA $85
L_C39E:
$C39E: 0A        ASL A
$C39F: 0A        ASL A
$C3A0: 85 00     STA $00
$C3A2: A9 BE     LDA #$BE
$C3A4: 38        SEC
$C3A5: E5 00     SBC $00
$C3A7: 85 84     STA $84
$C3A9: A5 83     LDA $83
$C3AB: F0 07     BEQ L_C3B4
$C3AD: A5 84     LDA $84
$C3AF: 38        SEC
$C3B0: E9 14     SBC #$14
$C3B2: 85 84     STA $84
L_C3B4:
$C3B4: 60        RTS
L_C3B5:
$C3B5: A9 01     LDA #$01
$C3B7: 85 6D     STA $6D
$C3B9: A9 00     LDA #$00
$C3BB: 85 4D     STA $4D
$C3BD: 20 BD C2  JSR L_C2BD
$C3C0: A9 03     LDA #$03
$C3C2: 85 52     STA $52
$C3C4: A9 00     LDA #$00
$C3C6: 85 4F     STA $4F
$C3C8: 85 50     STA $50
$C3CA: 85 0A     STA $0A
$C3CC: 85 0B     STA $0B
$C3CE: 20 B0 C9  JSR L_C9B0
$C3D1: A9 FF     LDA #$FF
$C3D3: 85 85     STA $85
$C3D5: 20 00 F0  JSR L_F000
$C3D8: A9 1E     LDA #$1E
$C3DA: 85 85     STA $85
$C3DC: A9 02     LDA #$02
$C3DE: 85 46     STA $46
$C3E0: 20 70 D4  JSR L_D470
$C3E3: A2 1A     LDX #$1A
$C3E5: 86 56     STX $56
$C3E7: A0 46     LDY #$46
$C3E9: 84 57     STY $57
$C3EB: A9 D2     LDA #$D2
$C3ED: 85 14     STA $14
$C3EF: A9 99     LDA #$99
$C3F1: 85 13     STA $13
$C3F3: 20 D2 D8  JSR L_D8D2
$C3F6: A2 3C     LDX #$3C
$C3F8: 86 56     STX $56
$C3FA: A0 78     LDY #$78
$C3FC: 84 57     STY $57
$C3FE: A9 D2     LDA #$D2
$C400: 85 14     STA $14
$C402: A9 A0     LDA #$A0
$C404: 85 13     STA $13
$C406: 20 D2 D8  JSR L_D8D2
$C409: 20 B4 D7  JSR L_D7B4
$C40C: 20 67 D4  JSR L_D467
$C40F: 20 31 C3  JSR L_C331
$C412: 20 F5 CA  JSR L_CAF5
$C415: 20 F6 D8  JSR L_D8F6
$C418: A9 05     LDA #$05
$C41A: 85 6C     STA $6C
$C41C: 60        RTS
L_C41D:
$C41D: 20 F6 D8  JSR L_D8F6
$C420: A5 08     LDA $08
$C422: 29 0C     AND #$0C
$C424: D0 19     BNE L_C43F
$C426: 20 42 C6  JSR L_C642
$C429: 20 E6 C2  JSR L_C2E6
$C42C: 20 3B E2  JSR L_E23B
$C42F: 20 A6 DE  JSR L_DEA6
$C432: 20 D8 E0  JSR L_E0D8
$C435: 20 28 C7  JSR L_C728
$C438: F0 E3     BEQ L_C41D
$C43A: A9 00     LDA #$00
$C43C: 85 0C     STA $0C
$C43E: 60        RTS
L_C43F:
$C43F: 68        PLA
$C440: 68        PLA
$C441: A9 00     LDA #$00
$C443: 85 0C     STA $0C
$C445: 20 6A D1  JSR L_D16A
$C448: 4C A2 C0  JMP L_C0A2
L_C44B:
$C44B: 20 70 D4  JSR L_D470
$C44E: A9 1C     LDA #$1C
$C450: 85 05     STA $05
$C452: A9 00     LDA #$00
$C454: 85 4F     STA $4F
$C456: 85 50     STA $50
$C458: 20 7E D4  JSR L_D47E
$C45B: A2 10     LDX #$10
$C45D: 86 56     STX $56
$C45F: A0 32     LDY #$32
$C461: 84 57     STY $57
$C463: A9 D2     LDA #$D2
$C465: 85 14     STA $14
$C467: A9 B5     LDA #$B5
$C469: 85 13     STA $13
$C46B: 20 D2 D8  JSR L_D8D2
$C46E: 20 51 D9  JSR L_D951
$C471: 20 B4 D7  JSR L_D7B4
$C474: 20 67 D4  JSR L_D467
$C477: A9 00     LDA #$00
$C479: 85 0A     STA $0A
$C47B: A9 01     LDA #$01
$C47D: 8D 15 03  STA $0315
$C480: 8D 16 03  STA $0316
$C483: 8D 17 03  STA $0317
L_C486:
$C486: 20 F6 D8  JSR L_D8F6
$C489: A5 0B     LDA $0B
$C48B: 29 03     AND #$03
$C48D: 18        CLC
$C48E: 69 05     ADC #$05
$C490: 85 4D     STA $4D
$C492: AD 15 03  LDA $0315
$C495: D0 EF     BNE L_C486
$C497: A9 00     LDA #$00
$C499: 85 4D     STA $4D
$C49B: 60        RTS
L_C49C:
$C49C: 20 70 D4  JSR L_D470
$C49F: A9 1C     LDA #$1C
$C4A1: 85 05     STA $05
$C4A3: A9 00     LDA #$00
$C4A5: 85 4F     STA $4F
$C4A7: 85 50     STA $50
$C4A9: 20 7E D4  JSR L_D47E
$C4AC: 20 B4 D7  JSR L_D7B4
$C4AF: 20 67 D4  JSR L_D467
$C4B2: 20 67 C5  JSR L_C567
$C4B5: 20 67 C5  JSR L_C567
$C4B8: A9 D3     LDA #$D3
$C4BA: 85 12     STA $12
$C4BC: A9 0F     LDA #$0F
$C4BE: 85 11     STA $11
$C4C0: A2 08     LDX #$08
$C4C2: A0 08     LDY #$08
$C4C4: 20 B3 D6  JSR L_D6B3
$C4C7: 20 67 C5  JSR L_C567
$C4CA: A9 D2     LDA #$D2
$C4CC: 85 12     STA $12
$C4CE: A9 84     LDA #$84
$C4D0: 85 11     STA $11
$C4D2: A2 08     LDX #$08
$C4D4: A0 0A     LDY #$0A
$C4D6: 20 B3 D6  JSR L_D6B3
$C4D9: 20 67 C5  JSR L_C567
$C4DC: A9 D3     LDA #$D3
$C4DE: 85 12     STA $12
$C4E0: A9 34     LDA #$34
$C4E2: 85 11     STA $11
$C4E4: A2 08     LDX #$08
$C4E6: A0 0C     LDY #$0C
$C4E8: 20 B3 D6  JSR L_D6B3
$C4EB: 20 67 C5  JSR L_C567
$C4EE: A9 D3     LDA #$D3
$C4F0: 85 12     STA $12
$C4F2: A9 4D     LDA #$4D
$C4F4: 85 11     STA $11
$C4F6: A2 08     LDX #$08
$C4F8: A0 0E     LDY #$0E
$C4FA: 20 B3 D6  JSR L_D6B3
$C4FD: 20 67 C5  JSR L_C567
$C500: A9 D3     LDA #$D3
$C502: 85 12     STA $12
$C504: A9 3F     LDA #$3F
$C506: 85 11     STA $11
$C508: A2 08     LDX #$08
$C50A: A0 10     LDY #$10
$C50C: 20 B3 D6  JSR L_D6B3
$C50F: 20 67 C5  JSR L_C567
$C512: A9 D3     LDA #$D3
$C514: 85 12     STA $12
$C516: A9 3F     LDA #$3F
$C518: 85 11     STA $11
$C51A: A2 09     LDX #$09
$C51C: A0 10     LDY #$10
$C51E: 20 B3 D6  JSR L_D6B3
$C521: 20 67 C5  JSR L_C567
$C524: A9 D3     LDA #$D3
$C526: 85 12     STA $12
$C528: A9 3F     LDA #$3F
$C52A: 85 11     STA $11
$C52C: A2 0A     LDX #$0A
$C52E: A0 10     LDY #$10
$C530: 20 B3 D6  JSR L_D6B3
$C533: 20 67 C5  JSR L_C567
$C536: A9 D3     LDA #$D3
$C538: 85 12     STA $12
$C53A: A9 3F     LDA #$3F
$C53C: 85 11     STA $11
$C53E: A2 0B     LDX #$0B
$C540: A0 10     LDY #$10
$C542: 20 B3 D6  JSR L_D6B3
$C545: 20 67 C5  JSR L_C567
$C548: A9 D3     LDA #$D3
$C54A: 85 12     STA $12
$C54C: A9 3F     LDA #$3F
$C54E: 85 11     STA $11
$C550: A2 0C     LDX #$0C
$C552: A0 10     LDY #$10
$C554: 20 B3 D6  JSR L_D6B3
$C557: 20 75 C5  JSR L_C575
$C55A: 20 70 D4  JSR L_D470
$C55D: 20 B0 C9  JSR L_C9B0
$C560: 20 B4 D7  JSR L_D7B4
$C563: 20 67 D4  JSR L_D467
$C566: 60        RTS
L_C567:
$C567: A9 00     LDA #$00
$C569: 85 0B     STA $0B
L_C56B:
$C56B: 20 F6 D8  JSR L_D8F6
$C56E: A5 0B     LDA $0B
$C570: 29 3F     AND #$3F
$C572: D0 F7     BNE L_C56B
$C574: 60        RTS
L_C575:
$C575: A9 78     LDA #$78
$C577: 85 56     STA $56
$C579: A9 1E     LDA #$1E
$C57B: 85 57     STA $57
$C57D: A9 00     LDA #$00
$C57F: 85 5A     STA $5A
L_C581:
$C581: 20 B0 C5  JSR L_C5B0
$C584: 20 B0 C5  JSR L_C5B0
$C587: 20 B0 C5  JSR L_C5B0
$C58A: 20 B0 C5  JSR L_C5B0
$C58D: E6 5A     INC $5A
$C58F: A5 5A     LDA $5A
$C591: C9 07     CMP #$07
$C593: D0 EC     BNE L_C581
L_C595:
$C595: 20 F6 D8  JSR L_D8F6
$C598: E6 57     INC $57
$C59A: A9 9D     LDA #$9D
$C59C: 85 53     STA $53
$C59E: A9 01     LDA #$01
$C5A0: 85 04     STA $04
$C5A2: A6 56     LDX $56
$C5A4: A4 57     LDY $57
$C5A6: 20 7B DA  JSR L_DA7B
$C5A9: A5 57     LDA $57
$C5AB: C9 F8     CMP #$F8
$C5AD: D0 E6     BNE L_C595
$C5AF: 60        RTS
L_C5B0:
$C5B0: 20 F6 D8  JSR L_D8F6
$C5B3: A9 03     LDA #$03
$C5B5: 85 04     STA $04
$C5B7: A9 03     LDA #$03
$C5B9: 38        SEC
$C5BA: E5 5A     SBC $5A
$C5BC: 10 05     BPL L_C5C3
$C5BE: 49 FF     EOR #$FF
$C5C0: 18        CLC
$C5C1: 69 01     ADC #$01
L_C5C3:
$C5C3: 85 00     STA $00
$C5C5: A9 03     LDA #$03
$C5C7: 38        SEC
$C5C8: E5 00     SBC $00
$C5CA: 0A        ASL A
$C5CB: 0A        ASL A
$C5CC: 18        CLC
$C5CD: 69 A1     ADC #$A1
$C5CF: 85 53     STA $53
$C5D1: A6 56     LDX $56
$C5D3: A4 57     LDY $57
$C5D5: 20 7B DA  JSR L_DA7B
$C5D8: 60        RTS
L_C5D9:
$C5D9: 20 70 D4  JSR L_D470
$C5DC: A9 1C     LDA #$1C
$C5DE: 85 05     STA $05
$C5E0: A9 00     LDA #$00
$C5E2: 85 4F     STA $4F
$C5E4: 85 50     STA $50
$C5E6: 20 7E D4  JSR L_D47E
$C5E9: A2 3C     LDX #$3C
$C5EB: 86 56     STX $56
$C5ED: A0 46     LDY #$46
$C5EF: 84 57     STY $57
$C5F1: A9 D3     LDA #$D3
$C5F3: 85 14     STA $14
$C5F5: A9 43     LDA #$43
$C5F7: 85 13     STA $13
$C5F9: 20 D2 D8  JSR L_D8D2
$C5FC: A2 3C     LDX #$3C
$C5FE: 86 56     STX $56
$C600: A0 78     LDY #$78
$C602: 84 57     STY $57
$C604: A9 D3     LDA #$D3
$C606: 85 14     STA $14
$C608: A9 48     LDA #$48
$C60A: 85 13     STA $13
$C60C: 20 D2 D8  JSR L_D8D2
$C60F: 20 B4 D7  JSR L_D7B4
$C612: 20 67 D4  JSR L_D467
$C615: A9 00     LDA #$00
$C617: 85 0A     STA $0A
$C619: A9 01     LDA #$01
$C61B: 8D 18 03  STA $0318
$C61E: 8D 19 03  STA $0319
$C621: 8D 1A 03  STA $031A
L_C624:
$C624: 20 F6 D8  JSR L_D8F6
$C627: A5 08     LDA $08
$C629: 29 0C     AND #$0C
$C62B: D0 05     BNE L_C632
$C62D: AD 18 03  LDA $0318
$C630: D0 F2     BNE L_C624
L_C632:
$C632: 20 70 D4  JSR L_D470
$C635: 20 7E D4  JSR L_D47E
$C638: 20 B4 D7  JSR L_D7B4
$C63B: 20 67 D4  JSR L_D467
$C63E: 20 51 EA  JSR L_EA51
$C641: 60        RTS
L_C642:
$C642: A9 01     LDA #$01
$C644: 85 5A     STA $5A
L_C646:
$C646: A6 5A     LDX $5A
$C648: A5 86     LDA $86
$C64A: F0 12     BEQ L_C65E
$C64C: A5 62     LDA $62
$C64E: D0 0E     BNE L_C65E
$C650: A5 86     LDA $86
$C652: 85 71     STA $71
$C654: A5 87     LDA $87
$C656: 85 72     STA $72
$C658: 20 A2 DD  JSR L_DDA2
$C65B: 4C A5 C6  JMP L_C6A5
L_C65E:
$C65E: B5 A2     LDA $A2,X
$C660: 10 12     BPL L_C674
$C662: C9 E0     CMP #$E0
$C664: B0 0E     BCS L_C674
$C666: B5 92     LDA $92,X
$C668: 85 71     STA $71
$C66A: B5 9A     LDA $9A,X
$C66C: 85 72     STA $72
$C66E: 20 A2 DD  JSR L_DDA2
$C671: 4C A5 C6  JMP L_C6A5
L_C674:
$C674: B5 A4     LDA $A4,X
$C676: 10 12     BPL L_C68A
$C678: C9 E0     CMP #$E0
$C67A: B0 0E     BCS L_C68A
$C67C: B5 94     LDA $94,X
$C67E: 85 71     STA $71
$C680: B5 9C     LDA $9C,X
$C682: 85 72     STA $72
$C684: 20 A2 DD  JSR L_DDA2
$C687: 4C A5 C6  JMP L_C6A5
L_C68A:
$C68A: B5 A3     LDA $A3,X
$C68C: 10 12     BPL L_C6A0
$C68E: C9 E0     CMP #$E0
$C690: B0 0E     BCS L_C6A0
$C692: B5 93     LDA $93,X
$C694: 85 71     STA $71
$C696: B5 9B     LDA $9B,X
$C698: 85 72     STA $72
$C69A: 20 A2 DD  JSR L_DDA2
$C69D: 4C A5 C6  JMP L_C6A5
L_C6A0:
$C6A0: A9 00     LDA #$00
$C6A2: 4C AB C6  JMP L_C6AB
L_C6A5:
$C6A5: 29 03     AND #$03
$C6A7: A8        TAY
$C6A8: B9 C2 C6  LDA $C6C2,Y
L_C6AB:
$C6AB: A6 5A     LDX $5A
$C6AD: 95 06     STA $06,X
$C6AF: 95 08     STA $08,X
$C6B1: B5 98     LDA $98,X
$C6B3: C9 C8     CMP #$C8
$C6B5: 90 06     BCC L_C6BD
$C6B7: B5 08     LDA $08,X
$C6B9: 29 F0     AND #$F0
$C6BB: 95 08     STA $08,X
L_C6BD:
$C6BD: C6 5A     DEC $5A
$C6BF: 10 85     BPL L_C646
$C6C1: 60        RTS
$C6C2: 13        db $13
$C6C3: 43        db $43
$C6C4: 23        db $23
$C6C5: 83        db $83
L_C6C6:
$C6C6: A5 5C     LDA $5C
$C6C8: 29 0F     AND #$0F
$C6CA: A6 90     LDX $90
$C6CC: A4 98     LDY $98
$C6CE: 20 0B D8  JSR L_D80B
$C6D1: 60        RTS
L_C6D2:
$C6D2: A5 06     LDA $06
$C6D4: 29 F0     AND #$F0
$C6D6: F0 09     BEQ L_C6E1
$C6D8: E6 7B     INC $7B
$C6DA: A9 00     LDA #$00
$C6DC: 85 81     STA $81
$C6DE: 4C E5 C6  JMP L_C6E5
L_C6E1:
$C6E1: A9 00     LDA #$00
$C6E3: 85 7B     STA $7B
L_C6E5:
$C6E5: A5 7B     LDA $7B
$C6E7: C9 14     CMP #$14
$C6E9: F0 10     BEQ L_C6FB
$C6EB: A5 08     LDA $08
$C6ED: 29 F0     AND #$F0
$C6EF: F0 2C     BEQ L_C71D
$C6F1: A5 08     LDA $08
$C6F3: 20 51 E4  JSR L_E451
$C6F6: 30 25     BMI L_C71D
$C6F8: 4C 04 C7  JMP L_C704
L_C6FB:
$C6FB: A9 0F     LDA #$0F
$C6FD: 85 7B     STA $7B
$C6FF: A5 06     LDA $06
$C701: 20 51 E4  JSR L_E451
L_C704:
$C704: A8        TAY
$C705: B9 D5 D3  LDA $D3D5,Y
$C708: 0A        ASL A
$C709: 0A        ASL A
$C70A: 0A        ASL A
$C70B: 0A        ASL A
$C70C: 18        CLC
$C70D: 65 90     ADC $90
$C70F: 85 90     STA $90
$C711: B9 D9 D3  LDA $D3D9,Y
$C714: 0A        ASL A
$C715: 0A        ASL A
$C716: 0A        ASL A
$C717: 0A        ASL A
$C718: 18        CLC
$C719: 65 98     ADC $98
$C71B: 85 98     STA $98
L_C71D:
$C71D: 60        RTS
L_C71E:
$C71E: A2 07     LDX #$07
$C720: A9 00     LDA #$00
L_C722:
$C722: 95 73     STA $73,X
$C724: CA        DEX
$C725: 10 FB     BPL L_C722
$C727: 60        RTS
L_C728:
$C728: A5 68     LDA $68
$C72A: F0 0B     BEQ L_C737
$C72C: A5 80     LDA $80
$C72E: F0 1F     BEQ L_C74F
$C730: A5 51     LDA $51
$C732: 18        CLC
$C733: 65 52     ADC $52
$C735: D0 1B     BNE L_C752
L_C737:
$C737: A9 70     LDA #$70
$C739: 8D 05 01  STA $0105
$C73C: A9 F0     LDA #$F0
$C73E: 8D 06 01  STA $0106
$C741: A9 00     LDA #$00
$C743: 8D 07 01  STA $0107
$C746: A9 11     LDA #$11
$C748: 8D 08 01  STA $0108
$C74B: A9 00     LDA #$00
$C74D: 85 0B     STA $0B
L_C74F:
$C74F: A9 01     LDA #$01
$C751: 60        RTS
L_C752:
$C752: A9 00     LDA #$00
$C754: 60        RTS
$C755: AD 09 01  LDA $0109
$C758: 20 E1 D9  JSR L_D9E1
$C75B: A9 30     LDA #$30
$C75D: 85 60     STA $60
$C75F: A9 00     LDA #$00
$C761: 85 12     STA $12
$C763: A9 39     LDA #$39
$C765: 85 11     STA $11
$C767: A2 09     LDX #$09
$C769: A0 02     LDY #$02
$C76B: 20 DD D6  JSR L_D6DD
$C76E: AE 09 01  LDX $0109
$C771: B5 00     LDA $00,X
$C773: 20 E1 D9  JSR L_D9E1
$C776: A9 00     LDA #$00
$C778: 85 12     STA $12
$C77A: A9 39     LDA #$39
$C77C: 85 11     STA $11
$C77E: A2 0D     LDX #$0D
$C780: A0 02     LDY #$02
$C782: 20 DD D6  JSR L_D6DD
$C785: A9 00     LDA #$00
$C787: 85 60     STA $60
$C789: A5 08     LDA $08
$C78B: 29 04     AND #$04
$C78D: F0 03     BEQ L_C792
$C78F: EE 09 01  INC $0109
L_C792:
$C792: A5 08     LDA $08
$C794: 29 02     AND #$02
$C796: F0 03     BEQ L_C79B
$C798: CE 09 01  DEC $0109
L_C79B:
$C79B: A5 08     LDA $08
$C79D: 29 01     AND #$01
$C79F: F0 09     BEQ L_C7AA
$C7A1: AD 09 01  LDA $0109
$C7A4: 18        CLC
$C7A5: 69 10     ADC #$10
$C7A7: 8D 09 01  STA $0109
L_C7AA:
$C7AA: 60        RTS
L_C7AB:
$C7AB: A9 00     LDA #$00
$C7AD: 85 4F     STA $4F
$C7AF: 85 50     STA $50
L_C7B1:
$C7B1: 20 F6 D8  JSR L_D8F6
$C7B4: E6 4F     INC $4F
$C7B6: A5 08     LDA $08
$C7B8: 29 0C     AND #$0C
$C7BA: D0 07     BNE L_C7C3
$C7BC: A5 4F     LDA $4F
$C7BE: C9 F0     CMP #$F0
$C7C0: D0 EF     BNE L_C7B1
$C7C2: 60        RTS
L_C7C3:
$C7C3: 68        PLA
$C7C4: 68        PLA
$C7C5: 4C A2 C0  JMP L_C0A2
L_C7C8:
$C7C8: A9 01     LDA #$01
$C7CA: 85 5A     STA $5A
$C7CC: 85 6B     STA $6B
$C7CE: A9 6E     LDA #$6E
$C7D0: 85 60     STA $60
$C7D2: A9 D3     LDA #$D3
$C7D4: 85 12     STA $12
$C7D6: A9 41     LDA #$41
$C7D8: 85 11     STA $11
$C7DA: A2 1D     LDX #$1D
$C7DC: A0 12     LDY #$12
$C7DE: 20 B3 D6  JSR L_D6B3
$C7E1: A5 46     LDA $46
$C7E3: C9 02     CMP #$02
$C7E5: F0 0B     BEQ L_C7F2
$C7E7: A5 83     LDA $83
$C7E9: D0 07     BNE L_C7F2
$C7EB: A9 00     LDA #$00
$C7ED: 85 5A     STA $5A
$C7EF: 4C 01 C8  JMP L_C801
L_C7F2:
$C7F2: A9 D3     LDA #$D3
$C7F4: 85 12     STA $12
$C7F6: A9 41     LDA #$41
$C7F8: 85 11     STA $11
$C7FA: A2 1D     LDX #$1D
$C7FC: A0 15     LDY #$15
$C7FE: 20 B3 D6  JSR L_D6B3
L_C801:
$C801: A6 5A     LDX $5A
$C803: B5 51     LDA $51,X
$C805: 38        SEC
$C806: E9 01     SBC #$01
$C808: 10 02     BPL L_C80C
$C80A: A9 00     LDA #$00
L_C80C:
$C80C: 20 13 DA  JSR L_DA13
$C80F: A0 36     LDY #$36
$C811: A2 19     LDX #$19
$C813: 20 34 D9  JSR L_D934
$C816: A5 5A     LDA $5A
$C818: 85 00     STA $00
$C81A: 0A        ASL A
$C81B: 18        CLC
$C81C: 65 00     ADC $00
$C81E: 18        CLC
$C81F: 69 12     ADC #$12
$C821: A8        TAY
$C822: 20 DD D6  JSR L_D6DD
$C825: C6 5A     DEC $5A
$C827: 10 D8     BPL L_C801
$C829: A9 00     LDA #$00
$C82B: 85 60     STA $60
$C82D: 85 6B     STA $6B
$C82F: 60        RTS
L_C830:
$C830: A9 D2     LDA #$D2
$C832: 85 12     STA $12
$C834: A9 AB     LDA #$AB
$C836: 85 11     STA $11
$C838: A2 1D     LDX #$1D
$C83A: A0 11     LDY #$11
$C83C: 20 B3 D6  JSR L_D6B3
$C83F: A5 46     LDA $46
$C841: C9 02     CMP #$02
$C843: F0 04     BEQ L_C849
$C845: A5 83     LDA $83
$C847: F0 0F     BEQ L_C858
L_C849:
$C849: A9 D2     LDA #$D2
$C84B: 85 12     STA $12
$C84D: A9 AE     LDA #$AE
$C84F: 85 11     STA $11
$C851: A2 1D     LDX #$1D
$C853: A0 14     LDY #$14
$C855: 20 B3 D6  JSR L_D6B3
L_C858:
$C858: 60        RTS
L_C859:
$C859: 20 F6 D8  JSR L_D8F6
$C85C: A9 D3     LDA #$D3
$C85E: 85 12     STA $12
$C860: A9 65     LDA #$65
$C862: 85 11     STA $11
$C864: A2 1D     LDX #$1D
$C866: A0 17     LDY #$17
$C868: 20 B3 D6  JSR L_D6B3
$C86B: A9 D3     LDA #$D3
$C86D: 85 12     STA $12
$C86F: A9 68     LDA #$68
$C871: 85 11     STA $11
$C873: A2 1D     LDX #$1D
$C875: A0 18     LDY #$18
$C877: 20 B3 D6  JSR L_D6B3
$C87A: A9 6E     LDA #$6E
$C87C: 85 60     STA $60
$C87E: A5 85     LDA $85
$C880: 20 13 DA  JSR L_DA13
$C883: A0 36     LDY #$36
$C885: A2 19     LDX #$19
$C887: 20 34 D9  JSR L_D934
$C88A: A0 19     LDY #$19
$C88C: 20 DD D6  JSR L_D6DD
$C88F: A9 00     LDA #$00
$C891: 85 60     STA $60
$C893: 60        RTS
L_C894:
$C894: 48        PHA
$C895: 29 01     AND #$01
$C897: 18        CLC
$C898: 69 1D     ADC #$1D
$C89A: AA        TAX
$C89B: 68        PLA
$C89C: 4A        LSR A
$C89D: 18        CLC
$C89E: 69 03     ADC #$03
$C8A0: A8        TAY
$C8A1: 60        RTS
L_C8A2:
$C8A2: 20 94 C8  JSR L_C894
$C8A5: A9 D3     LDA #$D3
$C8A7: 85 12     STA $12
$C8A9: A9 62     LDA #$62
$C8AB: 85 11     STA $11
$C8AD: 20 B3 D6  JSR L_D6B3
$C8B0: 60        RTS
L_C8B1:
$C8B1: 20 94 C8  JSR L_C894
$C8B4: A9 D3     LDA #$D3
$C8B6: 85 12     STA $12
$C8B8: A9 6B     LDA #$6B
$C8BA: 85 11     STA $11
$C8BC: 20 B3 D6  JSR L_D6B3
$C8BF: 60        RTS
L_C8C0:
$C8C0: A9 12     LDA #$12
$C8C2: 85 5A     STA $5A
L_C8C4:
$C8C4: A5 5A     LDA $5A
$C8C6: 20 A2 C8  JSR L_C8A2
$C8C9: C6 5A     DEC $5A
$C8CB: C6 5A     DEC $5A
$C8CD: 10 F5     BPL L_C8C4
$C8CF: 60        RTS
L_C8D0:
$C8D0: A5 90     LDA $90
$C8D2: C9 D8     CMP #$D8
$C8D4: 90 04     BCC L_C8DA
$C8D6: A9 D8     LDA #$D8
$C8D8: 85 90     STA $90
L_C8DA:
$C8DA: A5 90     LDA $90
$C8DC: C9 18     CMP #$18
$C8DE: B0 04     BCS L_C8E4
$C8E0: A9 18     LDA #$18
$C8E2: 85 90     STA $90
L_C8E4:
$C8E4: A5 98     LDA $98
$C8E6: C9 D8     CMP #$D8
$C8E8: 90 04     BCC L_C8EE
$C8EA: A9 D8     LDA #$D8
$C8EC: 85 98     STA $98
L_C8EE:
$C8EE: A5 98     LDA $98
$C8F0: C9 18     CMP #$18
$C8F2: B0 04     BCS L_C8F8
$C8F4: A9 18     LDA #$18
$C8F6: 85 98     STA $98
L_C8F8:
$C8F8: 60        RTS
L_C8F9:
$C8F9: A5 6D     LDA $6D
$C8FB: F0 49     BEQ L_C946
$C8FD: A5 0B     LDA $0B
$C8FF: 29 10     AND #$10
$C901: F0 43     BEQ L_C946
$C903: A9 03     LDA #$03
$C905: 85 04     STA $04
$C907: A9 00     LDA #$00
$C909: 85 6E     STA $6E
$C90B: A2 64     LDX #$64
$C90D: A0 80     LDY #$80
$C90F: A9 17     LDA #$17
$C911: 85 53     STA $53
$C913: 20 2B DA  JSR L_DA2B
$C916: A2 6C     LDX #$6C
$C918: A0 80     LDY #$80
$C91A: A9 19     LDA #$19
$C91C: 85 53     STA $53
$C91E: 20 2B DA  JSR L_DA2B
$C921: A2 74     LDX #$74
$C923: A0 80     LDY #$80
$C925: A9 1B     LDA #$1B
$C927: 85 53     STA $53
$C929: 20 2B DA  JSR L_DA2B
$C92C: A2 7C     LDX #$7C
$C92E: A0 80     LDY #$80
$C930: A9 1D     LDA #$1D
$C932: 85 53     STA $53
$C934: 20 2B DA  JSR L_DA2B
$C937: A2 84     LDX #$84
$C939: A0 80     LDY #$80
$C93B: A9 1F     LDA #$1F
$C93D: 85 53     STA $53
$C93F: 20 2B DA  JSR L_DA2B
$C942: A9 20     LDA #$20
$C944: 85 6E     STA $6E
L_C946:
$C946: 60        RTS
L_C947:
$C947: A9 03     LDA #$03
$C949: 85 04     STA $04
$C94B: A9 00     LDA #$00
$C94D: 85 6E     STA $6E
$C94F: AE 05 01  LDX $0105
$C952: AC 06 01  LDY $0106
$C955: A9 79     LDA #$79
$C957: 85 53     STA $53
$C959: 20 7B DA  JSR L_DA7B
$C95C: AD 05 01  LDA $0105
$C95F: 18        CLC
$C960: 69 10     ADC #$10
$C962: AA        TAX
$C963: AC 06 01  LDY $0106
$C966: A9 7D     LDA #$7D
$C968: 85 53     STA $53
$C96A: 20 7B DA  JSR L_DA7B
$C96D: A9 20     LDA #$20
$C96F: 85 6E     STA $6E
$C971: 60        RTS
L_C972:
$C972: AD 08 01  LDA $0108
$C975: F0 38     BEQ L_C9AF
$C977: A5 46     LDA $46
$C979: C9 02     CMP #$02
$C97B: F0 32     BEQ L_C9AF
$C97D: A5 0B     LDA $0B
$C97F: 29 0F     AND #$0F
$C981: D0 0A     BNE L_C98D
$C983: CE 08 01  DEC $0108
$C986: D0 05     BNE L_C98D
$C988: A9 F0     LDA #$F0
$C98A: 8D 06 01  STA $0106
L_C98D:
$C98D: AD 08 01  LDA $0108
$C990: C9 0A     CMP #$0A
$C992: 90 18     BCC L_C9AC
$C994: AD 07 01  LDA $0107
$C997: A8        TAY
$C998: B9 D5 D3  LDA $D3D5,Y
$C99B: 18        CLC
$C99C: 6D 05 01  ADC $0105
$C99F: 8D 05 01  STA $0105
$C9A2: B9 D9 D3  LDA $D3D9,Y
$C9A5: 18        CLC
$C9A6: 6D 06 01  ADC $0106
$C9A9: 8D 06 01  STA $0106
L_C9AC:
$C9AC: 20 47 C9  JSR L_C947
L_C9AF:
$C9AF: 60        RTS
L_C9B0:
$C9B0: A9 02     LDA #$02
$C9B2: 85 56     STA $56
$C9B4: 85 57     STA $57
$C9B6: A9 1A     LDA #$1A
$C9B8: 85 5A     STA $5A
$C9BA: 85 5B     STA $5B
$C9BC: 20 CC D7  JSR L_D7CC
$C9BF: 60        RTS
L_C9C0:
$C9C0: A9 03     LDA #$03
$C9C2: 85 4D     STA $4D
$C9C4: 20 13 E4  JSR L_E413
$C9C7: A9 48     LDA #$48
$C9C9: 85 90     STA $90
$C9CB: 20 85 CA  JSR L_CA85
$C9CE: A9 83     LDA #$83
$C9D0: 85 A0     STA $A0
$C9D2: A9 00     LDA #$00
$C9D4: 85 0A     STA $0A
$C9D6: 85 A8     STA $A8
$C9D8: 85 B0     STA $B0
$C9DA: 85 6F     STA $6F
$C9DC: 85 70     STA $70
$C9DE: 85 4F     STA $4F
$C9E0: 85 4A     STA $4A
$C9E2: A9 02     LDA #$02
$C9E4: 85 50     STA $50
L_C9E6:
$C9E6: 20 F6 D8  JSR L_D8F6
$C9E9: A5 0B     LDA $0B
$C9EB: 29 03     AND #$03
$C9ED: D0 06     BNE L_C9F5
$C9EF: A5 B0     LDA $B0
$C9F1: 49 04     EOR #$04
$C9F3: 85 B0     STA $B0
L_C9F5:
$C9F5: 20 A6 DE  JSR L_DEA6
$C9F8: A5 08     LDA $08
$C9FA: 29 04     AND #$04
$C9FC: F0 06     BEQ L_CA04
$C9FE: E6 83     INC $83
$CA00: A9 00     LDA #$00
$CA02: 85 0A     STA $0A
L_CA04:
$CA04: A5 06     LDA $06
$CA06: 29 20     AND #$20
$CA08: F0 0D     BEQ L_CA17
$CA0A: A5 09     LDA $09
$CA0C: 29 01     AND #$01
$CA0E: F0 07     BEQ L_CA17
$CA10: A9 10     LDA #$10
$CA12: 18        CLC
$CA13: 65 4A     ADC $4A
$CA15: 85 4A     STA $4A
L_CA17:
$CA17: A5 06     LDA $06
$CA19: 29 80     AND #$80
$CA1B: F0 08     BEQ L_CA25
$CA1D: A5 09     LDA $09
$CA1F: 29 02     AND #$02
$CA21: F0 02     BEQ L_CA25
$CA23: C6 4A     DEC $4A
L_CA25:
$CA25: A5 83     LDA $83
$CA27: C9 03     CMP #$03
$CA29: 90 04     BCC L_CA2F
$CA2B: A9 00     LDA #$00
$CA2D: 85 83     STA $83
L_CA2F:
$CA2F: 20 85 CA  JSR L_CA85
$CA32: A5 0A     LDA $0A
$CA34: C9 0A     CMP #$0A
$CA36: D0 05     BNE L_CA3D
$CA38: A5 4B     LDA $4B
$CA3A: D0 01     BNE L_CA3D
$CA3C: 60        RTS
L_CA3D:
$CA3D: A5 08     LDA $08
$CA3F: 29 08     AND #$08
$CA41: F0 A3     BEQ L_C9E6
$CA43: A5 4B     LDA $4B
$CA45: C9 07     CMP #$07
$CA47: D0 09     BNE L_CA52
$CA49: A5 4A     LDA $4A
$CA4B: C9 74     CMP #$74
$CA4D: D0 03     BNE L_CA52
$CA4F: 20 9C C4  JSR L_C49C
L_CA52:
$CA52: A9 00     LDA #$00
$CA54: 85 4D     STA $4D
$CA56: 68        PLA
$CA57: 68        PLA
$CA58: A5 83     LDA $83
$CA5A: 0A        ASL A
$CA5B: A8        TAY
$CA5C: B9 69 CA  LDA $CA69,Y
$CA5F: 85 11     STA $11
$CA61: B9 6A CA  LDA $CA6A,Y
$CA64: 85 12     STA $12
$CA66: 6C 11 00  JMP ($0011)
$CA69: 6F        db $6F
$CA6A: CA        DEX
$CA6B: 74        db $74
$CA6C: CA        DEX
$CA6D: 7E CA A9  ROR L_A9CA,X
$CA70: 05 4C     ORA $4C
$CA72: 76 CA     ROR $CA,X
$CA74: A9 07     LDA #$07
$CA76: 85 6C     STA $6C
$CA78: 20 B3 C2  JSR L_C2B3
$CA7B: 4C 59 C1  JMP L_C159
$CA7E: A9 07     LDA #$07
$CA80: 85 6C     STA $6C
$CA82: 4C AE C0  JMP L_C0AE
L_CA85:
$CA85: A5 83     LDA $83
$CA87: 0A        ASL A
$CA88: 0A        ASL A
$CA89: 0A        ASL A
$CA8A: 0A        ASL A
$CA8B: 18        CLC
$CA8C: 69 8B     ADC #$8B
$CA8E: 85 98     STA $98
$CA90: 60        RTS
L_CA91:
$CA91: 20 F6 D8  JSR L_D8F6
$CA94: A2 0C     LDX #$0C
$CA96: A0 0E     LDY #$0E
$CA98: 20 FB D5  JSR L_D5FB
$CA9B: A6 0C     LDX $0C
$CA9D: 18        CLC
$CA9E: 69 1C     ADC #$1C
$CAA0: 9D 80 01  STA $0180,X
$CAA3: E8        INX
$CAA4: 98        TYA
$CAA5: 9D 80 01  STA $0180,X
$CAA8: E8        INX
$CAA9: A9 23     LDA #$23
$CAAB: 9D 80 01  STA $0180,X
$CAAE: E8        INX
$CAAF: A9 24     LDA #$24
$CAB1: 9D 80 01  STA $0180,X
$CAB4: E8        INX
$CAB5: A9 25     LDA #$25
$CAB7: 9D 80 01  STA $0180,X
$CABA: E8        INX
$CABB: A9 26     LDA #$26
$CABD: 9D 80 01  STA $0180,X
$CAC0: E8        INX
$CAC1: A9 27     LDA #$27
$CAC3: 9D 80 01  STA $0180,X
$CAC6: E8        INX
$CAC7: A9 11     LDA #$11
$CAC9: 9D 80 01  STA $0180,X
$CACC: E8        INX
$CACD: A9 11     LDA #$11
$CACF: 9D 80 01  STA $0180,X
$CAD2: E8        INX
$CAD3: A9 FF     LDA #$FF
$CAD5: 9D 80 01  STA $0180,X
$CAD8: E8        INX
$CAD9: 86 0C     STX $0C
$CADB: A9 6E     LDA #$6E
$CADD: 85 60     STA $60
$CADF: A5 85     LDA $85
$CAE1: 20 13 DA  JSR L_DA13
$CAE4: A0 36     LDY #$36
$CAE6: A2 0E     LDX #$0E
$CAE8: 20 34 D9  JSR L_D934
$CAEB: A0 0E     LDY #$0E
$CAED: 20 DD D6  JSR L_D6DD
$CAF0: A9 00     LDA #$00
$CAF2: 85 60     STA $60
$CAF4: 60        RTS
L_CAF5:
$CAF5: A9 D3     LDA #$D3
$CAF7: 85 12     STA $12
$CAF9: A9 6D     LDA #$6D
$CAFB: 85 11     STA $11
$CAFD: A2 0C     LDX #$0C
$CAFF: A0 18     LDY #$18
$CB01: 20 B3 D6  JSR L_D6B3
$CB04: A9 D3     LDA #$D3
$CB06: 85 12     STA $12
$CB08: A9 74     LDA #$74
$CB0A: 85 11     STA $11
$CB0C: A2 0C     LDX #$0C
$CB0E: A0 19     LDY #$19
$CB10: 20 B3 D6  JSR L_D6B3
$CB13: A9 D3     LDA #$D3
$CB15: 85 12     STA $12
$CB17: A9 7B     LDA #$7B
$CB19: 85 11     STA $11
$CB1B: A2 0C     LDX #$0C
$CB1D: A0 1A     LDY #$1A
$CB1F: 20 B3 D6  JSR L_D6B3
$CB22: A9 D3     LDA #$D3
$CB24: 85 12     STA $12
$CB26: A9 82     LDA #$82
$CB28: 85 11     STA $11
$CB2A: A2 0C     LDX #$0C
$CB2C: A0 1B     LDY #$1B
$CB2E: 20 B3 D6  JSR L_D6B3
$CB31: A6 0C     LDX $0C
$CB33: A9 23     LDA #$23
$CB35: 9D 80 01  STA $0180,X
$CB38: E8        INX
$CB39: A9 F3     LDA #$F3
$CB3B: 9D 80 01  STA $0180,X
$CB3E: E8        INX
$CB3F: A9 00     LDA #$00
$CB41: 8D F3 07  STA $07F3
$CB44: 9D 80 01  STA $0180,X
$CB47: E8        INX
$CB48: AD F4 07  LDA $07F4
$CB4B: 29 CC     AND #$CC
$CB4D: 8D F4 07  STA $07F4
$CB50: 9D 80 01  STA $0180,X
$CB53: E8        INX
$CB54: A9 FF     LDA #$FF
$CB56: 9D 80 01  STA $0180,X
$CB59: E8        INX
$CB5A: 86 0C     STX $0C
$CB5C: 60        RTS
L_CB5D:
$CB5D: A9 D3     LDA #$D3
$CB5F: 85 12     STA $12
$CB61: A9 A5     LDA #$A5
$CB63: 85 11     STA $11
$CB65: A2 0E     LDX #$0E
$CB67: A0 1A     LDY #$1A
$CB69: 20 B3 D6  JSR L_D6B3
$CB6C: A9 D3     LDA #$D3
$CB6E: 85 12     STA $12
$CB70: A9 A8     LDA #$A8
$CB72: 85 11     STA $11
$CB74: A2 0E     LDX #$0E
$CB76: A0 1B     LDY #$1B
$CB78: 20 B3 D6  JSR L_D6B3
$CB7B: A6 0C     LDX $0C
$CB7D: A9 23     LDA #$23
$CB7F: 9D 80 01  STA $0180,X
$CB82: E8        INX
$CB83: A9 F3     LDA #$F3
$CB85: 9D 80 01  STA $0180,X
$CB88: E8        INX
$CB89: AD F3 07  LDA $07F3
$CB8C: 29 3F     AND #$3F
$CB8E: 8D F3 07  STA $07F3
$CB91: 9D 80 01  STA $0180,X
$CB94: E8        INX
$CB95: A9 FF     LDA #$FF
$CB97: 9D 80 01  STA $0180,X
$CB9A: E8        INX
$CB9B: 86 0C     STX $0C
$CB9D: 60        RTS
L_CB9E:
$CB9E: A9 D3     LDA #$D3
$CBA0: 85 12     STA $12
$CBA2: A9 89     LDA #$89
$CBA4: 85 11     STA $11
$CBA6: A2 0C     LDX #$0C
$CBA8: A0 18     LDY #$18
$CBAA: 20 B3 D6  JSR L_D6B3
$CBAD: A9 D3     LDA #$D3
$CBAF: 85 12     STA $12
$CBB1: A9 90     LDA #$90
$CBB3: 85 11     STA $11
$CBB5: A2 0C     LDX #$0C
$CBB7: A0 19     LDY #$19
$CBB9: 20 B3 D6  JSR L_D6B3
$CBBC: A9 D3     LDA #$D3
$CBBE: 85 12     STA $12
$CBC0: A9 97     LDA #$97
$CBC2: 85 11     STA $11
$CBC4: A2 0C     LDX #$0C
$CBC6: A0 1A     LDY #$1A
$CBC8: 20 B3 D6  JSR L_D6B3
$CBCB: A9 D3     LDA #$D3
$CBCD: 85 12     STA $12
$CBCF: A9 9E     LDA #$9E
$CBD1: 85 11     STA $11
$CBD3: A2 0C     LDX #$0C
$CBD5: A0 1B     LDY #$1B
$CBD7: 20 B3 D6  JSR L_D6B3
$CBDA: A6 0C     LDX $0C
$CBDC: A9 23     LDA #$23
$CBDE: 9D 80 01  STA $0180,X
$CBE1: E8        INX
$CBE2: A9 F3     LDA #$F3
$CBE4: 9D 80 01  STA $0180,X
$CBE7: E8        INX
$CBE8: A9 3F     LDA #$3F
$CBEA: 8D F3 07  STA $07F3
$CBED: 9D 80 01  STA $0180,X
$CBF0: E8        INX
$CBF1: AD F4 07  LDA $07F4
$CBF4: 29 CC     AND #$CC
$CBF6: 09 33     ORA #$33
$CBF8: 8D F4 07  STA $07F4
$CBFB: 9D 80 01  STA $0180,X
$CBFE: E8        INX
$CBFF: A9 FF     LDA #$FF
$CC01: 9D 80 01  STA $0180,X
$CC04: E8        INX
$CC05: 86 0C     STX $0C
$CC07: 60        RTS
L_CC08:
$CC08: A9 D3     LDA #$D3
$CC0A: 85 12     STA $12
$CC0C: A9 AB     LDA #$AB
$CC0E: 85 11     STA $11
$CC10: A2 0E     LDX #$0E
$CC12: A0 1A     LDY #$1A
$CC14: 20 B3 D6  JSR L_D6B3
$CC17: A9 D3     LDA #$D3
$CC19: 85 12     STA $12
$CC1B: A9 AE     LDA #$AE
$CC1D: 85 11     STA $11
$CC1F: A2 0E     LDX #$0E
$CC21: A0 1B     LDY #$1B
$CC23: 20 B3 D6  JSR L_D6B3
$CC26: 60        RTS
L_CC27:
$CC27: A0 00     LDY #$00
$CC29: A9 23     LDA #$23
$CC2B: 85 12     STA $12
$CC2D: A9 C0     LDA #$C0
$CC2F: 85 11     STA $11
L_CC31:
$CC31: 20 F6 D8  JSR L_D8F6
$CC34: A6 0C     LDX $0C
$CC36: A5 12     LDA $12
$CC38: 9D 80 01  STA $0180,X
$CC3B: E8        INX
$CC3C: A5 11     LDA $11
$CC3E: 9D 80 01  STA $0180,X
$CC41: E8        INX
$CC42: B9 C0 07  LDA $07C0,Y
$CC45: C8        INY
$CC46: 9D 80 01  STA $0180,X
$CC49: E8        INX
$CC4A: A9 FF     LDA #$FF
$CC4C: 9D 80 01  STA $0180,X
$CC4F: E8        INX
$CC50: 86 0C     STX $0C
$CC52: A9 01     LDA #$01
$CC54: 20 AA D7  JSR L_D7AA
$CC57: C0 40     CPY #$40
$CC59: D0 D6     BNE L_CC31
$CC5B: 60        RTS
L_CC5C:
$CC5C: A2 00     LDX #$00
$CC5E: 20 FB D5  JSR L_D5FB
$CC61: 85 12     STA $12
$CC63: 84 11     STY $11
$CC65: A6 0C     LDX $0C
$CC67: A5 12     LDA $12
$CC69: 18        CLC
$CC6A: 69 1C     ADC #$1C
$CC6C: 9D 80 01  STA $0180,X
$CC6F: E8        INX
$CC70: A5 11     LDA $11
$CC72: 9D 80 01  STA $0180,X
$CC75: E8        INX
$CC76: A0 00     LDY #$00
L_CC78:
$CC78: A5 63     LDA $63
$CC7A: D0 02     BNE L_CC7E
$CC7C: B1 11     LDA ($11),Y
L_CC7E:
$CC7E: 9D 80 01  STA $0180,X
$CC81: E8        INX
$CC82: C8        INY
$CC83: C0 20     CPY #$20
$CC85: D0 F1     BNE L_CC78
$CC87: A9 FF     LDA #$FF
$CC89: 9D 80 01  STA $0180,X
$CC8C: E8        INX
$CC8D: 86 0C     STX $0C
$CC8F: 60        RTS
L_CC90:
$CC90: A9 11     LDA #$11
$CC92: 85 63     STA $63
$CC94: A9 00     LDA #$00
$CC96: 85 57     STA $57
L_CC98:
$CC98: 20 F6 D8  JSR L_D8F6
$CC9B: A4 57     LDY $57
$CC9D: 20 5C CC  JSR L_CC5C
$CCA0: A9 1D     LDA #$1D
$CCA2: 38        SEC
$CCA3: E5 57     SBC $57
$CCA5: A8        TAY
$CCA6: 20 5C CC  JSR L_CC5C
$CCA9: E6 57     INC $57
$CCAB: A5 57     LDA $57
$CCAD: C9 10     CMP #$10
$CCAF: D0 E7     BNE L_CC98
$CCB1: 60        RTS
L_CCB2:
$CCB2: A9 00     LDA #$00
$CCB4: 85 63     STA $63
$CCB6: A9 0F     LDA #$0F
$CCB8: 85 57     STA $57
L_CCBA:
$CCBA: 20 F6 D8  JSR L_D8F6
$CCBD: A4 57     LDY $57
$CCBF: 20 5C CC  JSR L_CC5C
$CCC2: A9 1D     LDA #$1D
$CCC4: 38        SEC
$CCC5: E5 57     SBC $57
$CCC7: A8        TAY
$CCC8: 20 5C CC  JSR L_CC5C
$CCCB: C6 57     DEC $57
$CCCD: A5 57     LDA $57
$CCCF: C9 FF     CMP #$FF
$CCD1: D0 E7     BNE L_CCBA
$CCD3: 60        RTS
L_CCD4:
$CCD4: 20 F7 CE  JSR L_CEF7
$CCD7: A2 1E     LDX #$1E
$CCD9: 20 76 D2  JSR L_D276
$CCDC: A5 73     LDA $73
$CCDE: 18        CLC
$CCDF: 65 74     ADC $74
$CCE1: 18        CLC
$CCE2: 65 75     ADC $75
$CCE4: 18        CLC
$CCE5: 65 76     ADC $76
$CCE7: 85 7D     STA $7D
$CCE9: A5 77     LDA $77
$CCEB: 18        CLC
$CCEC: 65 78     ADC $78
$CCEE: 18        CLC
$CCEF: 65 79     ADC $79
$CCF1: 18        CLC
$CCF2: 65 7A     ADC $7A
$CCF4: 85 7E     STA $7E
$CCF6: A9 00     LDA #$00
$CCF8: 85 5A     STA $5A
L_CCFA:
$CCFA: 20 F6 D8  JSR L_D8F6
$CCFD: 20 B8 D0  JSR L_D0B8
$CD00: A2 25     LDX #$25
$CD02: 20 FE D9  JSR L_D9FE
$CD05: A2 2D     LDX #$2D
$CD07: 20 FE D9  JSR L_D9FE
$CD0A: A9 00     LDA #$00
$CD0C: 85 5D     STA $5D
$CD0E: 85 5E     STA $5E
L_CD10:
$CD10: 20 F6 D8  JSR L_D8F6
$CD13: 20 B8 D0  JSR L_D0B8
$CD16: A9 00     LDA #$00
$CD18: 85 7C     STA $7C
$CD1A: A6 5A     LDX $5A
$CD1C: BD D1 D3  LDA $D3D1,X
$CD1F: 20 E1 D9  JSR L_D9E1
$CD22: A6 5A     LDX $5A
$CD24: B5 73     LDA $73,X
$CD26: F0 18     BEQ L_CD40
$CD28: A9 01     LDA #$01
$CD2A: 8D 13 03  STA $0313
$CD2D: 8D 14 03  STA $0314
$CD30: D6 73     DEC $73,X
$CD32: E6 5D     INC $5D
$CD34: A2 02     LDX #$02
$CD36: 20 BE D9  JSR L_D9BE
$CD39: A9 01     LDA #$01
$CD3B: 85 7C     STA $7C
$CD3D: 20 38 D1  JSR L_D138
L_CD40:
$CD40: A6 5A     LDX $5A
$CD42: B5 77     LDA $77,X
$CD44: F0 18     BEQ L_CD5E
$CD46: A9 01     LDA #$01
$CD48: 8D 13 03  STA $0313
$CD4B: 8D 14 03  STA $0314
$CD4E: D6 77     DEC $77,X
$CD50: E6 5E     INC $5E
$CD52: A2 03     LDX #$03
$CD54: 20 BE D9  JSR L_D9BE
$CD57: A9 01     LDA #$01
$CD59: 85 7C     STA $7C
$CD5B: 20 38 D1  JSR L_D138
L_CD5E:
$CD5E: A0 16     LDY #$16
$CD60: A2 05     LDX #$05
$CD62: 20 34 D9  JSR L_D934
$CD65: A0 09     LDY #$09
$CD67: 20 DD D6  JSR L_D6DD
$CD6A: A2 01     LDX #$01
$CD6C: A0 26     LDY #$26
$CD6E: 20 34 D9  JSR L_D934
$CD71: A5 5A     LDA $5A
$CD73: 0A        ASL A
$CD74: 18        CLC
$CD75: 65 5A     ADC $5A
$CD77: 18        CLC
$CD78: 69 0C     ADC #$0C
$CD7A: A8        TAY
$CD7B: 20 DD D6  JSR L_D6DD
$CD7E: A6 5A     LDX $5A
$CD80: A5 5D     LDA $5D
$CD82: 20 13 DA  JSR L_DA13
$CD85: A2 08     LDX #$08
$CD87: A0 36     LDY #$36
$CD89: 20 34 D9  JSR L_D934
$CD8C: A5 5A     LDA $5A
$CD8E: 0A        ASL A
$CD8F: 18        CLC
$CD90: 65 5A     ADC $5A
$CD92: 18        CLC
$CD93: 69 0C     ADC #$0C
$CD95: A8        TAY
$CD96: 20 DD D6  JSR L_D6DD
$CD99: A5 83     LDA $83
$CD9B: F0 3B     BEQ L_CDD8
$CD9D: A0 1E     LDY #$1E
$CD9F: A2 17     LDX #$17
$CDA1: 20 34 D9  JSR L_D934
$CDA4: A0 09     LDY #$09
$CDA6: 20 DD D6  JSR L_D6DD
$CDA9: A2 13     LDX #$13
$CDAB: A0 2E     LDY #$2E
$CDAD: 20 34 D9  JSR L_D934
$CDB0: A5 5A     LDA $5A
$CDB2: 0A        ASL A
$CDB3: 18        CLC
$CDB4: 65 5A     ADC $5A
$CDB6: 18        CLC
$CDB7: 69 0C     ADC #$0C
$CDB9: A8        TAY
$CDBA: 20 DD D6  JSR L_D6DD
$CDBD: A6 5A     LDX $5A
$CDBF: A5 5E     LDA $5E
$CDC1: 20 13 DA  JSR L_DA13
$CDC4: A2 0E     LDX #$0E
$CDC6: A0 36     LDY #$36
$CDC8: 20 34 D9  JSR L_D934
$CDCB: A5 5A     LDA $5A
$CDCD: 0A        ASL A
$CDCE: 18        CLC
$CDCF: 65 5A     ADC $5A
$CDD1: 18        CLC
$CDD2: 69 0C     ADC #$0C
$CDD4: A8        TAY
$CDD5: 20 DD D6  JSR L_D6DD
L_CDD8:
$CDD8: A2 08     LDX #$08
$CDDA: 20 76 D2  JSR L_D276
$CDDD: A5 7C     LDA $7C
$CDDF: F0 03     BEQ L_CDE4
$CDE1: 4C 10 CD  JMP L_CD10
L_CDE4:
$CDE4: E6 5A     INC $5A
$CDE6: A5 5A     LDA $5A
$CDE8: C9 04     CMP #$04
$CDEA: F0 08     BEQ L_CDF4
$CDEC: A2 14     LDX #$14
$CDEE: 20 76 D2  JSR L_D276
$CDF1: 4C FA CC  JMP L_CCFA
L_CDF4:
$CDF4: A2 1E     LDX #$1E
$CDF6: 20 76 D2  JSR L_D276
$CDF9: A5 7D     LDA $7D
$CDFB: 20 13 DA  JSR L_DA13
$CDFE: A0 36     LDY #$36
$CE00: A2 08     LDX #$08
$CE02: 20 34 D9  JSR L_D934
$CE05: A0 17     LDY #$17
$CE07: 20 DD D6  JSR L_D6DD
$CE0A: A5 83     LDA $83
$CE0C: F0 11     BEQ L_CE1F
$CE0E: A5 7E     LDA $7E
$CE10: 20 13 DA  JSR L_DA13
$CE13: A0 36     LDY #$36
$CE15: A2 0E     LDX #$0E
$CE17: 20 34 D9  JSR L_D934
$CE1A: A0 17     LDY #$17
$CE1C: 20 DD D6  JSR L_D6DD
L_CE1F:
$CE1F: A2 0F     LDX #$0F
$CE21: 20 76 D2  JSR L_D276
$CE24: A5 83     LDA $83
$CE26: D0 03     BNE L_CE2B
$CE28: 4C E5 CE  JMP L_CEE5
L_CE2B:
$CE2B: A5 68     LDA $68
$CE2D: D0 03     BNE L_CE32
$CE2F: 4C E5 CE  JMP L_CEE5
L_CE32:
$CE32: A5 7E     LDA $7E
$CE34: C5 7D     CMP $7D
$CE36: B0 55     BCS L_CE8D
$CE38: A5 51     LDA $51
$CE3A: F0 51     BEQ L_CE8D
$CE3C: A9 00     LDA #$00
$CE3E: 20 E1 D9  JSR L_D9E1
$CE41: A2 00     LDX #$00
$CE43: 20 BE D9  JSR L_D9BE
$CE46: A0 16     LDY #$16
$CE48: A2 05     LDX #$05
$CE4A: 20 34 D9  JSR L_D934
$CE4D: A0 09     LDY #$09
$CE4F: 20 DD D6  JSR L_D6DD
$CE52: A0 36     LDY #$36
$CE54: A2 01     LDX #$01
$CE56: 20 34 D9  JSR L_D934
$CE59: A0 1A     LDY #$1A
$CE5B: 20 DD D6  JSR L_D6DD
$CE5E: A9 D3     LDA #$D3
$CE60: 85 12     STA $12
$CE62: A9 C4     LDA #$C4
$CE64: 85 11     STA $11
$CE66: A2 03     LDX #$03
$CE68: A0 19     LDY #$19
$CE6A: 20 B3 D6  JSR L_D6B3
$CE6D: A9 D3     LDA #$D3
$CE6F: 85 12     STA $12
$CE71: A9 5E     LDA #$5E
$CE73: 85 11     STA $11
$CE75: A2 08     LDX #$08
$CE77: A0 1A     LDY #$1A
$CE79: 20 B3 D6  JSR L_D6B3
$CE7C: A9 01     LDA #$01
$CE7E: 8D 1B 03  STA $031B
$CE81: 8D 1C 03  STA $031C
$CE84: 8D 1D 03  STA $031D
$CE87: 20 38 D1  JSR L_D138
$CE8A: 4C E5 CE  JMP L_CEE5
L_CE8D:
$CE8D: A5 7D     LDA $7D
$CE8F: C5 7E     CMP $7E
$CE91: B0 52     BCS L_CEE5
$CE93: A5 52     LDA $52
$CE95: F0 4E     BEQ L_CEE5
$CE97: A9 00     LDA #$00
$CE99: 20 E1 D9  JSR L_D9E1
$CE9C: A2 01     LDX #$01
$CE9E: 20 BE D9  JSR L_D9BE
$CEA1: A0 1E     LDY #$1E
$CEA3: A2 17     LDX #$17
$CEA5: 20 34 D9  JSR L_D934
$CEA8: A0 09     LDY #$09
$CEAA: 20 DD D6  JSR L_D6DD
$CEAD: A0 36     LDY #$36
$CEAF: A2 14     LDX #$14
$CEB1: 20 34 D9  JSR L_D934
$CEB4: A0 1A     LDY #$1A
$CEB6: 20 DD D6  JSR L_D6DD
$CEB9: A9 D3     LDA #$D3
$CEBB: 85 12     STA $12
$CEBD: A9 C4     LDA #$C4
$CEBF: 85 11     STA $11
$CEC1: A2 16     LDX #$16
$CEC3: A0 19     LDY #$19
$CEC5: 20 B3 D6  JSR L_D6B3
$CEC8: A9 D3     LDA #$D3
$CECA: 85 12     STA $12
$CECC: A9 5E     LDA #$5E
$CECE: 85 11     STA $11
$CED0: A2 1B     LDX #$1B
$CED2: A0 1A     LDY #$1A
$CED4: 20 B3 D6  JSR L_D6B3
$CED7: A9 01     LDA #$01
$CED9: 8D 1B 03  STA $031B
$CEDC: 8D 1C 03  STA $031C
$CEDF: 8D 1D 03  STA $031D
$CEE2: 20 38 D1  JSR L_D138
L_CEE5:
$CEE5: A2 78     LDX #$78
$CEE7: 20 76 D2  JSR L_D276
$CEEA: A9 00     LDA #$00
$CEEC: 85 50     STA $50
$CEEE: 85 60     STA $60
$CEF0: 85 6B     STA $6B
$CEF2: A9 00     LDA #$00
$CEF4: 85 4D     STA $4D
$CEF6: 60        RTS
L_CEF7:
$CEF7: 20 F6 D8  JSR L_D8F6
$CEFA: A9 01     LDA #$01
$CEFC: 85 6B     STA $6B
$CEFE: A9 24     LDA #$24
$CF00: 85 05     STA $05
$CF02: A9 00     LDA #$00
$CF04: 85 4F     STA $4F
$CF06: A9 02     LDA #$02
$CF08: 85 50     STA $50
$CF0A: A9 30     LDA #$30
$CF0C: 85 60     STA $60
$CF0E: A9 03     LDA #$03
$CF10: 85 4D     STA $4D
$CF12: 20 70 D4  JSR L_D470
$CF15: 20 7E D4  JSR L_D47E
$CF18: 20 D9 D0  JSR L_D0D9
$CF1B: 20 B4 D7  JSR L_D7B4
$CF1E: 20 67 D4  JSR L_D467
$CF21: A9 D2     LDA #$D2
$CF23: 85 12     STA $12
$CF25: A9 BD     LDA #$BD
$CF27: 85 11     STA $11
$CF29: A2 08     LDX #$08
$CF2B: A0 03     LDY #$03
$CF2D: 20 B3 D6  JSR L_D6B3
$CF30: A0 3E     LDY #$3E
$CF32: A2 12     LDX #$12
$CF34: 20 34 D9  JSR L_D934
$CF37: A0 03     LDY #$03
$CF39: 20 DD D6  JSR L_D6DD
$CF3C: A9 D3     LDA #$D3
$CF3E: 85 12     STA $12
$CF40: A9 CB     LDA #$CB
$CF42: 85 11     STA $11
$CF44: A2 0C     LDX #$0C
$CF46: A0 05     LDY #$05
$CF48: 20 B3 D6  JSR L_D6B3
$CF4B: A5 85     LDA $85
$CF4D: 20 13 DA  JSR L_DA13
$CF50: A0 36     LDY #$36
$CF52: A2 0E     LDX #$0E
$CF54: 20 34 D9  JSR L_D934
$CF57: A0 05     LDY #$05
$CF59: 20 DD D6  JSR L_D6DD
$CF5C: 20 F6 D8  JSR L_D8F6
$CF5F: A9 D2     LDA #$D2
$CF61: 85 12     STA $12
$CF63: A9 D9     LDA #$D9
$CF65: 85 11     STA $11
$CF67: A2 03     LDX #$03
$CF69: A0 07     LDY #$07
$CF6B: 20 B3 D6  JSR L_D6B3
$CF6E: A0 16     LDY #$16
$CF70: A2 05     LDX #$05
$CF72: 20 34 D9  JSR L_D934
$CF75: A0 09     LDY #$09
$CF77: 20 DD D6  JSR L_D6DD
$CF7A: A9 D3     LDA #$D3
$CF7C: 85 12     STA $12
$CF7E: A9 B1     LDA #$B1
$CF80: 85 11     STA $11
$CF82: A2 0E     LDX #$0E
$CF84: A0 0C     LDY #$0C
$CF86: 20 B3 D6  JSR L_D6B3
$CF89: A9 D3     LDA #$D3
$CF8B: 85 12     STA $12
$CF8D: A9 B1     LDA #$B1
$CF8F: 85 11     STA $11
$CF91: A2 0E     LDX #$0E
$CF93: A0 0F     LDY #$0F
$CF95: 20 B3 D6  JSR L_D6B3
$CF98: A9 D3     LDA #$D3
$CF9A: 85 12     STA $12
$CF9C: A9 B1     LDA #$B1
$CF9E: 85 11     STA $11
$CFA0: A2 0E     LDX #$0E
$CFA2: A0 12     LDY #$12
$CFA4: 20 B3 D6  JSR L_D6B3
$CFA7: A9 D3     LDA #$D3
$CFA9: 85 12     STA $12
$CFAB: A9 B1     LDA #$B1
$CFAD: 85 11     STA $11
$CFAF: A2 0E     LDX #$0E
$CFB1: A0 15     LDY #$15
$CFB3: 20 B3 D6  JSR L_D6B3
$CFB6: A5 83     LDA $83
$CFB8: F0 5A     BEQ L_D014
$CFBA: 20 F6 D8  JSR L_D8F6
$CFBD: A9 D2     LDA #$D2
$CFBF: 85 12     STA $12
$CFC1: A9 E2     LDA #$E2
$CFC3: 85 11     STA $11
$CFC5: A2 15     LDX #$15
$CFC7: A0 07     LDY #$07
$CFC9: 20 B3 D6  JSR L_D6B3
$CFCC: A0 1E     LDY #$1E
$CFCE: A2 17     LDX #$17
$CFD0: 20 34 D9  JSR L_D934
$CFD3: A0 09     LDY #$09
$CFD5: 20 DD D6  JSR L_D6DD
$CFD8: A9 D3     LDA #$D3
$CFDA: 85 12     STA $12
$CFDC: A9 B3     LDA #$B3
$CFDE: 85 11     STA $11
$CFE0: A2 11     LDX #$11
$CFE2: A0 0C     LDY #$0C
$CFE4: 20 B3 D6  JSR L_D6B3
$CFE7: A9 D3     LDA #$D3
$CFE9: 85 12     STA $12
$CFEB: A9 B3     LDA #$B3
$CFED: 85 11     STA $11
$CFEF: A2 11     LDX #$11
$CFF1: A0 0F     LDY #$0F
$CFF3: 20 B3 D6  JSR L_D6B3
$CFF6: A9 D3     LDA #$D3
$CFF8: 85 12     STA $12
$CFFA: A9 B3     LDA #$B3
$CFFC: 85 11     STA $11
$CFFE: A2 11     LDX #$11
$D000: A0 12     LDY #$12
$D002: 20 B3 D6  JSR L_D6B3
$D005: A9 D3     LDA #$D3
$D007: 85 12     STA $12
$D009: A9 B3     LDA #$B3
$D00B: 85 11     STA $11
$D00D: A2 11     LDX #$11
$D00F: A0 15     LDY #$15
$D011: 20 B3 D6  JSR L_D6B3
L_D014:
$D014: 20 F6 D8  JSR L_D8F6
$D017: A9 D3     LDA #$D3
$D019: 85 12     STA $12
$D01B: A9 5E     LDA #$5E
$D01D: 85 11     STA $11
$D01F: A2 08     LDX #$08
$D021: A0 0C     LDY #$0C
$D023: 20 B3 D6  JSR L_D6B3
$D026: A9 D3     LDA #$D3
$D028: 85 12     STA $12
$D02A: A9 5E     LDA #$5E
$D02C: 85 11     STA $11
$D02E: A2 08     LDX #$08
$D030: A0 0F     LDY #$0F
$D032: 20 B3 D6  JSR L_D6B3
$D035: A9 D3     LDA #$D3
$D037: 85 12     STA $12
$D039: A9 5E     LDA #$5E
$D03B: 85 11     STA $11
$D03D: A2 08     LDX #$08
$D03F: A0 12     LDY #$12
$D041: 20 B3 D6  JSR L_D6B3
$D044: A9 D3     LDA #$D3
$D046: 85 12     STA $12
$D048: A9 5E     LDA #$5E
$D04A: 85 11     STA $11
$D04C: A2 08     LDX #$08
$D04E: A0 15     LDY #$15
$D050: 20 B3 D6  JSR L_D6B3
$D053: A5 83     LDA $83
$D055: F0 3F     BEQ L_D096
$D057: 20 F6 D8  JSR L_D8F6
$D05A: A9 D3     LDA #$D3
$D05C: 85 12     STA $12
$D05E: A9 5E     LDA #$5E
$D060: 85 11     STA $11
$D062: A2 1A     LDX #$1A
$D064: A0 0C     LDY #$0C
$D066: 20 B3 D6  JSR L_D6B3
$D069: A9 D3     LDA #$D3
$D06B: 85 12     STA $12
$D06D: A9 5E     LDA #$5E
$D06F: 85 11     STA $11
$D071: A2 1A     LDX #$1A
$D073: A0 0F     LDY #$0F
$D075: 20 B3 D6  JSR L_D6B3
$D078: A9 D3     LDA #$D3
$D07A: 85 12     STA $12
$D07C: A9 5E     LDA #$5E
$D07E: 85 11     STA $11
$D080: A2 1A     LDX #$1A
$D082: A0 12     LDY #$12
$D084: 20 B3 D6  JSR L_D6B3
$D087: A9 D3     LDA #$D3
$D089: 85 12     STA $12
$D08B: A9 5E     LDA #$5E
$D08D: 85 11     STA $11
$D08F: A2 1A     LDX #$1A
$D091: A0 15     LDY #$15
$D093: 20 B3 D6  JSR L_D6B3
L_D096:
$D096: 20 F6 D8  JSR L_D8F6
$D099: A9 D3     LDA #$D3
$D09B: 85 12     STA $12
$D09D: A9 BB     LDA #$BB
$D09F: 85 11     STA $11
$D0A1: A2 0C     LDX #$0C
$D0A3: A0 16     LDY #$16
$D0A5: 20 B3 D6  JSR L_D6B3
$D0A8: A9 D3     LDA #$D3
$D0AA: 85 12     STA $12
$D0AC: A9 B5     LDA #$B5
$D0AE: 85 11     STA $11
$D0B0: A2 06     LDX #$06
$D0B2: A0 17     LDY #$17
$D0B4: 20 B3 D6  JSR L_D6B3
$D0B7: 60        RTS
L_D0B8:
$D0B8: A9 02     LDA #$02
$D0BA: 85 04     STA $04
$D0BC: A0 64     LDY #$64
$D0BE: A9 80     LDA #$80
$D0C0: 20 30 D1  JSR L_D130
$D0C3: A0 7C     LDY #$7C
$D0C5: A9 A0     LDA #$A0
$D0C7: 20 30 D1  JSR L_D130
$D0CA: A0 94     LDY #$94
$D0CC: A9 C0     LDA #$C0
$D0CE: 20 30 D1  JSR L_D130
$D0D1: A0 AC     LDY #$AC
$D0D3: A9 E0     LDA #$E0
$D0D5: 20 30 D1  JSR L_D130
$D0D8: 60        RTS
L_D0D9:
$D0D9: A9 50     LDA #$50
$D0DB: 8D C0 07  STA $07C0
$D0DE: 8D C1 07  STA $07C1
$D0E1: 8D C2 07  STA $07C2
$D0E4: 8D C3 07  STA $07C3
$D0E7: 8D C8 07  STA $07C8
$D0EA: 8D C9 07  STA $07C9
$D0ED: 8D CA 07  STA $07CA
$D0F0: 8D CD 07  STA $07CD
$D0F3: 8D CE 07  STA $07CE
$D0F6: 8D CF 07  STA $07CF
$D0F9: A9 A0     LDA #$A0
$D0FB: 8D C4 07  STA $07C4
$D0FE: 8D C5 07  STA $07C5
$D101: 8D C6 07  STA $07C6
$D104: 8D C7 07  STA $07C7
$D107: A9 0A     LDA #$0A
$D109: 8D D0 07  STA $07D0
$D10C: 8D D1 07  STA $07D1
$D10F: 8D D2 07  STA $07D2
$D112: 8D D5 07  STA $07D5
$D115: 8D D6 07  STA $07D6
$D118: 8D D7 07  STA $07D7
$D11B: A9 05     LDA #$05
$D11D: 8D F0 07  STA $07F0
$D120: 8D F1 07  STA $07F1
$D123: 8D F2 07  STA $07F2
$D126: 8D F5 07  STA $07F5
$D129: 8D F6 07  STA $07F6
$D12C: 8D F7 07  STA $07F7
$D12F: 60        RTS
L_D130:
$D130: 85 53     STA $53
$D132: A2 81     LDX #$81
$D134: 20 7B DA  JSR L_DA7B
$D137: 60        RTS
L_D138:
$D138: A5 68     LDA $68
$D13A: C9 80     CMP #$80
$D13C: D0 2B     BNE L_D169
$D13E: A5 66     LDA $66
$D140: D0 0D     BNE L_D14F
$D142: A5 17     LDA $17
$D144: C9 02     CMP #$02
$D146: 90 07     BCC L_D14F
$D148: E6 51     INC $51
$D14A: E6 66     INC $66
$D14C: 4C 61 D1  JMP L_D161
L_D14F:
$D14F: A5 83     LDA $83
$D151: F0 16     BEQ L_D169
$D153: A5 67     LDA $67
$D155: D0 12     BNE L_D169
$D157: A5 1F     LDA $1F
$D159: C9 02     CMP #$02
$D15B: 90 0C     BCC L_D169
$D15D: E6 52     INC $52
$D15F: E6 67     INC $67
L_D161:
$D161: A9 01     LDA #$01
$D163: 8D 04 03  STA $0304
$D166: 8D 05 03  STA $0305
L_D169:
$D169: 60        RTS
L_D16A:
$D16A: 20 70 D4  JSR L_D470
$D16D: A9 03     LDA #$03
$D16F: 85 4D     STA $4D
$D171: A9 1C     LDA #$1C
$D173: 85 05     STA $05
$D175: 20 7E D4  JSR L_D47E
$D178: 20 B4 D7  JSR L_D7B4
$D17B: 20 67 D4  JSR L_D467
$D17E: 60        RTS
L_D17F:
$D17F: 20 70 D4  JSR L_D470
$D182: A9 24     LDA #$24
$D184: 85 05     STA $05
$D186: 20 7E D4  JSR L_D47E
$D189: A2 1A     LDX #$1A
$D18B: 86 56     STX $56
$D18D: A0 2E     LDY #$2E
$D18F: 84 57     STY $57
$D191: A9 D2     LDA #$D2
$D193: 85 14     STA $14
$D195: A9 99     LDA #$99
$D197: 85 13     STA $13
$D199: 20 D2 D8  JSR L_D8D2
$D19C: A2 3C     LDX #$3C
$D19E: 86 56     STX $56
$D1A0: A0 56     LDY #$56
$D1A2: 84 57     STY $57
$D1A4: A9 D2     LDA #$D2
$D1A6: 85 14     STA $14
$D1A8: A9 A0     LDA #$A0
$D1AA: 85 13     STA $13
$D1AC: 20 D2 D8  JSR L_D8D2
$D1AF: 20 B4 D7  JSR L_D7B4
$D1B2: 20 67 D4  JSR L_D467
$D1B5: A9 30     LDA #$30
$D1B7: 85 60     STA $60
$D1B9: A9 D2     LDA #$D2
$D1BB: 85 12     STA $12
$D1BD: A9 A5     LDA #$A5
$D1BF: 85 11     STA $11
$D1C1: A2 02     LDX #$02
$D1C3: A0 03     LDY #$03
$D1C5: 20 B3 D6  JSR L_D6B3
$D1C8: A0 16     LDY #$16
$D1CA: A2 04     LDX #$04
$D1CC: 20 34 D9  JSR L_D934
$D1CF: A0 03     LDY #$03
$D1D1: 20 DD D6  JSR L_D6DD
$D1D4: A9 D2     LDA #$D2
$D1D6: 85 12     STA $12
$D1D8: A9 B1     LDA #$B1
$D1DA: 85 11     STA $11
$D1DC: A2 0B     LDX #$0B
$D1DE: A0 03     LDY #$03
$D1E0: 20 B3 D6  JSR L_D6B3
$D1E3: A0 3E     LDY #$3E
$D1E5: A2 0E     LDX #$0E
$D1E7: 20 34 D9  JSR L_D934
$D1EA: A0 03     LDY #$03
$D1EC: 20 DD D6  JSR L_D6DD
$D1EF: A5 83     LDA $83
$D1F1: F0 1B     BEQ L_D20E
$D1F3: A9 D2     LDA #$D2
$D1F5: 85 12     STA $12
$D1F7: A9 A8     LDA #$A8
$D1F9: 85 11     STA $11
$D1FB: A2 15     LDX #$15
$D1FD: A0 03     LDY #$03
$D1FF: 20 B3 D6  JSR L_D6B3
$D202: A0 1E     LDY #$1E
$D204: A2 17     LDX #$17
$D206: 20 34 D9  JSR L_D934
$D209: A0 03     LDY #$03
$D20B: 20 DD D6  JSR L_D6DD
L_D20E:
$D20E: A9 00     LDA #$00
$D210: 85 60     STA $60
$D212: 20 F6 D8  JSR L_D8F6
$D215: A9 D2     LDA #$D2
$D217: 85 12     STA $12
$D219: A9 C6     LDA #$C6
$D21B: 85 11     STA $11
$D21D: A2 0B     LDX #$0B
$D21F: A0 11     LDY #$11
$D221: 20 B3 D6  JSR L_D6B3
$D224: A9 D2     LDA #$D2
$D226: 85 12     STA $12
$D228: A9 CF     LDA #$CF
$D22A: 85 11     STA $11
$D22C: A2 0B     LDX #$0B
$D22E: A0 13     LDY #$13
$D230: 20 B3 D6  JSR L_D6B3
$D233: A9 D2     LDA #$D2
$D235: 85 12     STA $12
$D237: A9 EB     LDA #$EB
$D239: 85 11     STA $11
$D23B: A2 0B     LDX #$0B
$D23D: A0 15     LDY #$15
$D23F: 20 B3 D6  JSR L_D6B3
$D242: 20 F6 D8  JSR L_D8F6
$D245: A9 D2     LDA #$D2
$D247: 85 12     STA $12
$D249: A9 8F     LDA #$8F
$D24B: 85 11     STA $11
$D24D: A2 0B     LDX #$0B
$D24F: A0 17     LDY #$17
$D251: 20 B3 D6  JSR L_D6B3
$D254: A9 D2     LDA #$D2
$D256: 85 12     STA $12
$D258: A9 F8     LDA #$F8
$D25A: 85 11     STA $11
$D25C: A2 04     LDX #$04
$D25E: A0 19     LDY #$19
$D260: 20 B3 D6  JSR L_D6B3
$D263: 20 F6 D8  JSR L_D8F6
$D266: A9 D3     LDA #$D3
$D268: 85 12     STA $12
$D26A: A9 20     LDA #$20
$D26C: 85 11     STA $11
$D26E: A2 06     LDX #$06
$D270: A0 1B     LDY #$1B
$D272: 20 B3 D6  JSR L_D6B3
$D275: 60        RTS
L_D276:
$D276: 20 F6 D8  JSR L_D8F6
$D279: 8A        TXA
$D27A: 48        PHA
$D27B: 20 B8 D0  JSR L_D0B8
$D27E: 68        PLA
$D27F: AA        TAX
$D280: CA        DEX
$D281: D0 F3     BNE L_D276
$D283: 60        RTS
$D284: 57        db $57
$D285: 52        db $52
$D286: 49 54     EOR #$54
$D288: 54        db $54
$D289: 45 4E     EOR $4E
$D28B: 20 42 59  JSR L_5942
$D28E: FF        db $FF
$D28F: 60        RTS
$D290: 61 62     ADC ($62,X)
$D292: 63        db $63
$D293: 64        db $64
$D294: 65 66     ADC $66
$D296: 67        db $67
$D297: 68        PLA
$D298: FF        db $FF
$D299: 42        db $42
$D29A: 41 54     EOR ($54,X)
$D29C: 54        db $54
$D29D: 4C 45 FF  JMP L_FF45
$D2A0: 43        db $43
$D2A1: 49 54     EOR #$54
$D2A3: 59 FF 5E  EOR $5EFF,Y
$D2A6: 6B        db $6B
$D2A7: FF        db $FF
$D2A8: 5F        db $5F
$D2A9: 6B        db $6B
$D2AA: FF        db $FF
$D2AB: 58        CLI
$D2AC: 13        db $13
$D2AD: FF        db $FF
$D2AE: 5A        db $5A
$D2AF: 13        db $13
$D2B0: FF        db $FF
$D2B1: 48        PHA
$D2B2: 49 6B     EOR #$6B
$D2B4: FF        db $FF
$D2B5: 48        PHA
$D2B6: 49 53     EOR #$53
$D2B8: 43        db $43
$D2B9: 4F        db $4F
$D2BA: 52        db $52
$D2BB: 45 FF     EOR $FF
L_D2BD:
$D2BD: 48        PHA
$D2BE: 49 6B     EOR #$6B
$D2C0: 53        db $53
$D2C1: 43        db $43
$D2C2: 4F        db $4F
$D2C3: 52        db $52
$D2C4: 45 FF     EOR $FF
$D2C6: 31 20     AND ($20),Y
$D2C8: 50 4C     BVC L_D316
$D2CA: 41 59     EOR ($59,X)
$D2CC: 45 52     EOR $52
$D2CE: FF        db $FF
$D2CF: 32        db $32
$D2D0: 20 50 4C  JSR L_4C50
$D2D3: 41 59     EOR ($59,X)
$D2D5: 45 52     EOR $52
$D2D7: 53        db $53
$D2D8: FF        db $FF
$D2D9: 5E 6B 50  LSR $506B,X
$D2DC: 4C 41 59  JMP L_5941
$D2DF: 45 52     EOR $52
$D2E1: FF        db $FF
$D2E2: 5F        db $5F
$D2E3: 6B        db $6B
$D2E4: 50 4C     BVC L_D332
$D2E6: 41 59     EOR ($59,X)
$D2E8: 45 52     EOR $52
$D2EA: FF        db $FF
$D2EB: 43        db $43
$D2EC: 4F        db $4F
$D2ED: 4E 53 54  LSR $5453
$D2F0: 52        db $52
$D2F1: 55 43     EOR $43,X
$D2F3: 54        db $54
$D2F4: 49 4F     EOR #$4F
$D2F6: 4E FF 40  LSR $40FF
$D2F9: 20 31 39  JSR L_3931
$D2FC: 38        SEC
$D2FD: 30 20     BMI L_D31F
$D2FF: 31 39     AND ($39),Y
$D301: 38        SEC
$D302: 35 20     AND $20,X
$D304: 4E 41 4D  LSR $4D41
$D307: 43        db $43
$D308: 4F        db $4F
$D309: 20 4C 54  JSR L_544C
$D30C: 44        db $44
$D30D: 69 FF     ADC #$FF
$D30F: 54        db $54
$D310: 48        PHA
$D311: 49 53     EOR #$53
$D313: 20 50 52  JSR L_5250
L_D316:
$D316: 4F        db $4F
$D317: 47        db $47
$D318: 52        db $52
$D319: 41 4D     EOR ($4D,X)
$D31B: 20 57 41  JSR L_4157
$D31E: 53        db $53
L_D31F:
$D31F: FF        db $FF
$D320: 41 4C     EOR ($4C,X)
$D322: 4C 20 52  JMP L_5220
$D325: 49 47     EOR #$47
$D327: 48        PHA
$D328: 54        db $54
$D329: 53        db $53
$D32A: 20 52 45  JSR L_4552
$D32D: 53        db $53
$D32E: 45 52     EOR $52
$D330: 56 45     LSR $45,X
L_D332:
$D332: 44        db $44
$D333: FF        db $FF
$D334: 4F        db $4F
$D335: 50 45     BVC L_D37C
$D337: 4E 6B 52  LSR $526B
$D33A: 45 41     EOR $41
$D33C: 43        db $43
$D33D: 48        PHA
$D33E: FF        db $FF
$D33F: 69 FF     ADC #$FF
$D341: 14        db $14
$D342: FF        db $FF
$D343: 47        db $47
$D344: 41 4D     EOR ($4D,X)
$D346: 45 FF     EOR $FF
$D348: 4F        db $4F
$D349: 56 45     LSR $45,X
$D34B: 52        db $52
$D34C: FF        db $FF
$D34D: 57        db $57
$D34E: 48        PHA
$D34F: 4F        db $4F
$D350: 20 4C 4F  JSR L_4F4C
$D353: 56 45     LSR $45,X
$D355: 53        db $53
$D356: 20 4E 4F  JSR L_4F4E
$D359: 52        db $52
$D35A: 49 4B     EOR #$4B
$D35C: 4F        db $4F
$D35D: FF        db $FF
$D35E: 50 54     BVC L_D3B4
$D360: 53        db $53
$D361: FF        db $FF
L_D362:
$D362: 6A        ROR A
$D363: 6A        ROR A
$D364: FF        db $FF
$D365: 6C FC FF  JMP ($FFFC)
$D368: 6D FD FF  ADC $FFFD
$D36B: 11 FF     ORA ($FF),Y
$D36D: 00        BRK
$D36E: 00        BRK
$D36F: 00        BRK
$D370: 00        BRK
$D371: 00        BRK
$D372: 00        BRK
$D373: FF        db $FF
$D374: 00        BRK
$D375: 0F        db $0F
$D376: 0F        db $0F
$D377: 0F        db $0F
$D378: 0F        db $0F
$D379: 00        BRK
$D37A: FF        db $FF
$D37B: 00        BRK
L_D37C:
$D37C: 0F        db $0F
$D37D: C8        INY
$D37E: CA        DEX
$D37F: 0F        db $0F
$D380: 00        BRK
$D381: FF        db $FF
$D382: 00        BRK
$D383: 0F        db $0F
$D384: C9 CB     CMP #$CB
$D386: 0F        db $0F
$D387: 00        BRK
$D388: FF        db $FF
$D389: 00        BRK
$D38A: 00        BRK
$D38B: 00        BRK
$D38C: 00        BRK
$D38D: 00        BRK
$D38E: 00        BRK
$D38F: FF        db $FF
$D390: 00        BRK
$D391: 10 10     BPL L_D3A3
$D393: 10 10     BPL L_D3A5
$D395: 00        BRK
$D396: FF        db $FF
$D397: 00        BRK
$D398: 10 C8     BPL L_D362
$D39A: CA        DEX
$D39B: 10 00     BPL L_D39D
L_D39D:
$D39D: FF        db $FF
$D39E: 00        BRK
$D39F: 10 C9     BPL L_D36A
$D3A1: CB        db $CB
$D3A2: 10 00     BPL L_D3A4
L_D3A4:
$D3A4: FF        db $FF
L_D3A5:
$D3A5: C8        INY
$D3A6: CA        DEX
$D3A7: FF        db $FF
$D3A8: C9 CB     CMP #$CB
$D3AA: FF        db $FF
$D3AB: CC CE FF  CPY $FFCE
$D3AE: CD CF FF  CMP $FFCF
$D3B1: 5B        db $5B
$D3B2: FF        db $FF
$D3B3: 5D FF 54  EOR $54FF,X
$D3B6: 4F        db $4F
$D3B7: 54        db $54
$D3B8: 41 4C     EOR ($4C,X)
$D3BA: FF        db $FF
$D3BB: 5C        db $5C
$D3BC: 5C        db $5C
$D3BD: 5C        db $5C
$D3BE: 5C        db $5C
$D3BF: 5C        db $5C
$D3C0: 5C        db $5C
$D3C1: 5C        db $5C
$D3C2: 5C        db $5C
$D3C3: FF        db $FF
$D3C4: 42        db $42
$D3C5: 4F        db $4F
$D3C6: 4E 55 53  LSR $5355
$D3C9: 15 FF     ORA $FF,X
$D3CB: 53        db $53
$D3CC: 54        db $54
$D3CD: 41 47     EOR ($47,X)
$D3CF: 45 FF     EOR $FF
$D3D1: 10 20     BPL L_D3F3
$D3D3: 30 40     BMI L_D415
$D3D5: 00        BRK
$D3D6: FF        db $FF
$D3D7: 00        BRK
$D3D8: 01 FF     ORA ($FF,X)
$D3DA: 00        BRK
$D3DB: 01 00     ORA ($00,X)
$D3DD: FF        db $FF
$D3DE: FF        db $FF
$D3DF: FF        db $FF
$D3E0: FF        db $FF
$D3E1: FF        db $FF
$D3E2: FF        db $FF
$D3E3: FF        db $FF
$D3E4: FF        db $FF
$D3E5: FF        db $FF
$D3E6: FF        db $FF
$D3E7: FF        db $FF
$D3E8: FF        db $FF
$D3E9: FF        db $FF
$D3EA: FF        db $FF
$D3EB: FF        db $FF
$D3EC: FF        db $FF
$D3ED: FF        db $FF
$D3EE: FF        db $FF
$D3EF: FF        db $FF
$D3F0: FF        db $FF
$D3F1: FF        db $FF
$D3F2: FF        db $FF
L_D3F3:
$D3F3: FF        db $FF
$D3F4: FF        db $FF
$D3F5: FF        db $FF
$D3F6: FF        db $FF
$D3F7: FF        db $FF
$D3F8: FF        db $FF
$D3F9: FF        db $FF
$D3FA: FF        db $FF
$D3FB: FF        db $FF
$D3FC: FF        db $FF
$D3FD: FF        db $FF
$D3FE: FF        db $FF
$D3FF: FF        db $FF
NMI:
$D400: 48        PHA
$D401: 8A        TXA
$D402: 48        PHA
$D403: 98        TYA
$D404: 48        PHA
$D405: 08        PHP
$D406: A9 00     LDA #$00
$D408: 8D 03 20  STA OAMADDR
$D40B: A9 02     LDA #$02
$D40D: 8D 14 40  STA OAMDMA
$D410: AD 02 20  LDA PPUSTATUS
$D413: 20 FD D8  JSR L_D8FD
$D416: A5 4D     LDA $4D
$D418: 30 03     BMI L_D41D
$D41A: 20 0E D5  JSR L_D50E
L_D41D:
$D41D: A5 50     LDA $50
$D41F: 09 B0     ORA #$B0
$D421: 8D 00 20  STA PPUCTRL
$D424: A9 00     LDA #$00
$D426: 8D 05 20  STA PPUSCROLL
$D429: A5 4F     LDA $4F
$D42B: 8D 05 20  STA PPUSCROLL
$D42E: A9 1E     LDA #$1E
$D430: 8D 01 20  STA PPUMASK
$D433: 20 89 D6  JSR L_D689
$D436: 20 93 DA  JSR L_DA93
$D439: 20 7E EA  JSR L_EA7E
$D43C: E6 0B     INC $0B
$D43E: A5 0B     LDA $0B
$D440: 29 3F     AND #$3F
$D442: D0 02     BNE L_D446
$D444: E6 0A     INC $0A
L_D446:
$D446: 28        PLP
$D447: 68        PLA
$D448: A8        TAY
$D449: 68        PLA
$D44A: AA        TAX
$D44B: 68        PLA
$D44C: 40        RTI
L_D44D:
$D44D: 8A        TXA
$D44E: 48        PHA
$D44F: A5 0F     LDA $0F
$D451: 0A        ASL A
$D452: 0A        ASL A
$D453: 0A        ASL A
$D454: 38        SEC
$D455: E5 0F     SBC $0F
$D457: 18        CLC
$D458: 65 0A     ADC $0A
$D45A: E6 10     INC $10
$D45C: A6 10     LDX $10
$D45E: 75 00     ADC $00,X
$D460: 85 0F     STA $0F
$D462: 68        PLA
$D463: AA        TAX
$D464: A5 0F     LDA $0F
$D466: 60        RTS

; EnablePpuNmi ($D467): Wait for a vblank flag, then configure PPUCTRL and enable vblank NMIs.
; Inputs: none; depends on PPUSTATUS ($2002). Outputs: A=$B0, N=1, Z=0; writes $B0 to PPUCTRL ($2000).
; Polling PPUSTATUS clears its vblank flag and resets the scroll/address write latch.
EnablePpuNmi:
L_D467:
    ; Poll until the vblank flag is observed; it may already be set.
    $D467: 20 F5 D5  JSR WaitForVblank ; WaitForVblank ($D5F5)

    ; Enable NMI, select 8x16 sprites, background table $1000, nametable $2000, and PPUDATA increment 1.
    ; The PPU may ignore this write during startup warm-up; this routine does not write PPUMASK.
    $D46A: A9 B0     LDA #$B0
    $D46C: 8D 00 20  STA PPUCTRL       ; PPUCTRL ($2000)
    $D46F: 60        RTS

L_D470:
$D470: 20 F6 D8  JSR L_D8F6
$D473: A9 10     LDA #$10
$D475: 8D 00 20  STA PPUCTRL
$D478: A9 06     LDA #$06
$D47A: 8D 01 20  STA PPUMASK
$D47D: 60        RTS
ClearPpuBuf:
L_D47E:
$D47E: A9 00     LDA #$00
$D480: AA        TAX
L_D481:
$D481: 9D 00 04  STA $0400,X
$D484: 9D 00 05  STA $0500,X
$D487: 9D 00 06  STA $0600,X
$D48A: 9D 00 07  STA $0700,X
$D48D: E8        INX
$D48E: D0 F1     BNE L_D481
$D490: 60        RTS

; InitGameState ($D491): Initialize game state, video buffers, and audio; preserve selected state if a marker matches.
; Inputs: no register parameters; depends on PPU status and the RAM marker at $0110-$011F.
; Outputs: initializes RAM and issues PPU/APU writes; A, X, Y, and flags are modified, with no return value.
InitGameState:
L_D491:
    ; Clear state variables, mark the palette request inactive, and load initial palettes after vblank.
    $D491: A9 00     LDA #$00
    $D493: 85 60     STA PpuDataOffset ; PpuDataOffset ($0060)
    $D495: 85 6B     STA StringTrim    ; StringTrim ($006B)
    $D497: 85 0C     STA PpuQueueEnd   ; PpuQueueEnd ($000C)
    $D499: 85 0D     STA OamIndex      ; OamIndex ($000D)
    $D49B: 85 6D     STA PauseFlag     ; PauseFlag ($006D)
    $D49D: A9 FF     LDA #$FF
    $D49F: 85 4D     STA PaletteReq    ; PaletteReq ($004D)
    $D4A1: 20 02 D5  JSR InitPalettes  ; InitPalettes ($D502)

    ; Clear the PPU buffer and hide shadow OAM sprites 1-63; HideSprites sets OamStep=$FC and OamIndex=$04.
    $D4A4: A9 04     LDA #$04
    $D4A6: 85 0E     STA OamStep       ; OamStep ($000E)
    $D4A8: A9 20     LDA #$20
    $D4AA: 85 6E     STA TileAttrBits  ; TileAttrBits ($006E)
    $D4AC: 20 7E D4  JSR ClearPpuBuf   ; ClearPpuBuf ($D47E)
    $D4AF: 20 93 DA  JSR HideSprites   ; HideSprites ($DA93)

    ; Initialize two eight-byte zero-page records at $0015-$001C and $001D-$0024.
    $D4B2: A2 15     LDX #$15
    $D4B4: 20 FE D9  JSR InitRecord    ; InitRecord ($D9FE)
    $D4B7: A2 1D     LDX #$1D
    $D4B9: 20 FE D9  JSR InitRecord    ; InitRecord ($D9FE)

    ; Keep the third record and option if $0110-$011F matches the 16-byte marker at $C040-$C04F.
    ; On mismatch initialize $003D-$0044 and set $003F to $02; the role of $003F is not yet known.
    $D4BC: 20 EF D4  JSR CheckMarker   ; CheckMarker ($D4EF)
    $D4BF: D0 0D     BNE FinishInit    ; FinishInit ($D4CE)
    $D4C1: A2 3D     LDX #$3D
    $D4C3: 20 FE D9  JSR InitRecord    ; InitRecord ($D9FE)
    $D4C6: A9 02     LDA #$02
    $D4C8: 85 3F     STA $3F
    $D4CA: A9 00     LDA #$00
    $D4CC: 85 83     STA OptionIndex   ; OptionIndex ($0083)

    ; Copy the cleared buffer to PPU $2000-$23FF and $2800-$2BFF, then store the marker and initialize audio.
FinishInit:
L_D4CE:
    $D4CE: A9 1C     LDA #$1C
    $D4D0: 85 05     STA PpuPageOffset ; PpuPageOffset ($0005)
    $D4D2: 20 B4 D7  JSR CopyPpuBuffer ; CopyPpuBuffer ($D7B4)
    $D4D5: A9 24     LDA #$24
    $D4D7: 85 05     STA PpuPageOffset ; PpuPageOffset ($0005)
    $D4D9: 20 B4 D7  JSR CopyPpuBuffer ; CopyPpuBuffer ($D7B4)
    $D4DC: 20 E3 D4  JSR StoreMarker   ; StoreMarker ($D4E3)
    $D4DF: 20 51 EA  JSR InitAudio     ; InitAudio ($EA51)
    $D4E2: 60        RTS

StoreMarker:
L_D4E3:
$D4E3: A2 0F     LDX #$0F
L_D4E5:
$D4E5: BD 40 C0  LDA $C040,X
$D4E8: 9D 10 01  STA $0110,X
$D4EB: CA        DEX
$D4EC: 10 F7     BPL L_D4E5
$D4EE: 60        RTS
CheckMarker:
L_D4EF:
$D4EF: A2 0F     LDX #$0F
L_D4F1:
$D4F1: BD 10 01  LDA $0110,X
$D4F4: DD 40 C0  CMP $C040,X
$D4F7: D0 06     BNE L_D4FF
$D4F9: CA        DEX
$D4FA: 10 F5     BPL L_D4F1
$D4FC: A9 01     LDA #$01
$D4FE: 60        RTS
L_D4FF:
$D4FF: A9 00     LDA #$00
$D501: 60        RTS
InitPalettes:
L_D502:
$D502: 20 F5 D5  JSR L_D5F5
$D505: 20 3E D5  JSR InitSpritePal
$D508: A9 00     LDA #$00
$D50A: 20 0E D5  JSR L_D50E
$D50D: 60        RTS
L_D50E:
$D50E: 0A        ASL A
$D50F: 0A        ASL A
$D510: 0A        ASL A
$D511: 0A        ASL A
$D512: AA        TAX
$D513: A0 10     LDY #$10
$D515: A9 3F     LDA #$3F
$D517: 8D 06 20  STA PPUADDR
$D51A: A9 00     LDA #$00
$D51C: 8D 06 20  STA PPUADDR
L_D51F:
$D51F: BD 65 D5  LDA $D565,X
$D522: 8D 07 20  STA PPUDATA
$D525: E8        INX
$D526: 88        DEY
$D527: D0 F6     BNE L_D51F
$D529: A9 FF     LDA #$FF
$D52B: 85 4D     STA $4D
$D52D: A9 3F     LDA #$3F
$D52F: 8D 06 20  STA PPUADDR
$D532: A9 00     LDA #$00
$D534: 8D 06 20  STA PPUADDR
$D537: 8D 06 20  STA PPUADDR
$D53A: 8D 06 20  STA PPUADDR
$D53D: 60        RTS

; InitSpritePal ($D53E): Copy four fixed sprite palettes to PPU palette memory.
; Inputs: PPUADDR ($2006) expects its first write, PPUCTRL ($2000) bit 2 is clear, and PPU memory is writable.
; Outputs: 16 writes to PPUDATA ($2007); PPU address=$3F20, A=$20, X=$10, Y=$00, N=0, Z=1.
; The routine does not wait for vblank; its caller InitPalettes ($D502) reads PPUSTATUS before calling it.
InitSpritePal:
    ; Set the PPU address to $3F10; Y also counts the 16 bytes to copy.
    $D53E: A2 00     LDX #$00
    $D540: A0 10     LDY #$10
    $D542: A9 3F     LDA #$3F
    $D544: 8D 06 20  STA PPUADDR       ; PPUADDR ($2006), high byte
    $D547: 8C 06 20  STY PPUADDR       ; PPUADDR ($2006), low byte

    ; Copy the table to consecutive palette addresses through PPUDATA.
SpritePalLoop:
L_D54A:
    $D54A: BD 55 D5  LDA SpritePal,X   ; SpritePal ($D555)
    $D54D: 8D 07 20  STA PPUDATA       ; PPUDATA ($2007)
    $D550: E8        INX
    $D551: 88        DEY
    $D552: D0 F6     BNE SpritePalLoop ; SpritePalLoop ($D54A)
    $D554: 60        RTS

; SpritePal ($D555-$D564): Four rows of NES color indices ($00-$3F), read by InitSpritePal ($D53E).
; Sprite pixel value 0 is transparent; the first byte of each row is written to a mirrored background entry.
; PPU $3F10/$3F14/$3F18/$3F1C mirror $3F00/$3F04/$3F08/$3F0C respectively.
SpritePal:
    $D555: 0F 18 27 38  db $0F, $18, $27, $38
    $D559: 0F 0A 1B 3B  db $0F, $0A, $1B, $3B
    $D55D: 0F 0C 10 20  db $0F, $0C, $10, $20
    $D561: 0F 04 16 20  db $0F, $04, $16, $20

$D565: 0F        db $0F
$D566: 17        db $17
$D567: 06 00     ASL $00
$D569: 0F        db $0F
$D56A: 3C        db $3C
$D56B: 10 12     BPL L_D57F
$D56D: 0F        db $0F
$D56E: 29 09     AND #$09
$D570: 0B        db $0B
$D571: 0F        db $0F
$D572: 00        BRK
$D573: 10 20     BPL L_D595
$D575: 0F        db $0F
$D576: 17        db $17
$D577: 06 00     ASL $00
$D579: 0F        db $0F
$D57A: 3C        db $3C
$D57B: 12        db $12
$D57C: 12        db $12
$D57D: 0F        db $0F
$D57E: 29 09     AND #$09
$D580: 0B        db $0B
L_D581:
$D581: 0F        db $0F
$D582: 00        BRK
$D583: 10 20     BPL L_D5A5
$D585: 0F        db $0F
$D586: 17        db $17
$D587: 06 00     ASL $00
$D589: 0F        db $0F
$D58A: 12        db $12
$D58B: 3C        db $3C
$D58C: 12        db $12
$D58D: 0F        db $0F
$D58E: 29 09     AND #$09
$D590: 0B        db $0B
$D591: 0F        db $0F
$D592: 00        BRK
$D593: 10 20     BPL L_D5B5
L_D595:
$D595: 0F        db $0F
$D596: 16 16     ASL $16,X
$D598: 30 0F     BMI L_D5A9
$D59A: 3C        db $3C
$D59B: 10 16     BPL L_D5B3
$D59D: 0F        db $0F
$D59E: 29 09     AND #$09
$D5A0: 27        db $27
$D5A1: 0F        db $0F
$D5A2: 00        BRK
$D5A3: 10 20     BPL L_D5C5
L_D5A5:
$D5A5: 0F        db $0F
$D5A6: 17        db $17
$D5A7: 06 00     ASL $00
L_D5A9:
$D5A9: 0F        db $0F
$D5AA: 3C        db $3C
$D5AB: 10 00     BPL L_D5AD
L_D5AD:
$D5AD: 0F        db $0F
$D5AE: 29 09     AND #$09
$D5B0: 00        BRK
$D5B1: 0F        db $0F
$D5B2: 00        BRK
L_D5B3:
$D5B3: 10 00     BPL L_D5B5
L_D5B5:
$D5B5: 0F        db $0F
$D5B6: 0F        db $0F
$D5B7: 06 00     ASL $00
$D5B9: 0F        db $0F
$D5BA: 3C        db $3C
$D5BB: 10 00     BPL L_D5BD
L_D5BD:
$D5BD: 0F        db $0F
$D5BE: 29 09     AND #$09
$D5C0: 00        BRK
$D5C1: 0F        db $0F
$D5C2: 00        BRK
$D5C3: 10 00     BPL L_D5C5
L_D5C5:
$D5C5: 0F        db $0F
$D5C6: 12        db $12
$D5C7: 06 00     ASL $00
$D5C9: 0F        db $0F
$D5CA: 3C        db $3C
$D5CB: 10 00     BPL L_D5CD
L_D5CD:
$D5CD: 0F        db $0F
$D5CE: 29 09     AND #$09
$D5D0: 00        BRK
$D5D1: 0F        db $0F
$D5D2: 00        BRK
$D5D3: 10 00     BPL L_D5D5
L_D5D5:
$D5D5: 0F        db $0F
$D5D6: 00        BRK
$D5D7: 06 00     ASL $00
$D5D9: 0F        db $0F
$D5DA: 3C        db $3C
$D5DB: 10 00     BPL L_D5DD
L_D5DD:
$D5DD: 0F        db $0F
$D5DE: 29 09     AND #$09
$D5E0: 00        BRK
$D5E1: 0F        db $0F
$D5E2: 00        BRK
$D5E3: 10 00     BPL L_D5E5
L_D5E5:
$D5E5: 0F        db $0F
$D5E6: 30 06     BMI L_D5EE
$D5E8: 00        BRK
$D5E9: 0F        db $0F
$D5EA: 3C        db $3C
$D5EB: 10 00     BPL L_D5ED
L_D5ED:
$D5ED: 0F        db $0F
L_D5EE:
$D5EE: 29 09     AND #$09
$D5F0: 00        BRK
$D5F1: 0F        db $0F
$D5F2: 00        BRK
$D5F3: 10 00     BPL L_D5F5
WaitForVblank:
L_D5F5:
$D5F5: AD 02 20  LDA PPUSTATUS
$D5F8: 10 FB     BPL L_D5F5
$D5FA: 60        RTS
L_D5FB:
$D5FB: A9 00     LDA #$00
$D5FD: 85 00     STA $00
$D5FF: 98        TYA
$D600: 4A        LSR A
$D601: 66 00     ROR $00
$D603: 4A        LSR A
$D604: 66 00     ROR $00
$D606: 4A        LSR A
$D607: 66 00     ROR $00
$D609: 48        PHA
$D60A: 8A        TXA
$D60B: 05 00     ORA $00
$D60D: A8        TAY
$D60E: 68        PLA
$D60F: 09 04     ORA #$04
$D611: 60        RTS
L_D612:
$D612: 20 35 D6  JSR L_D635
$D615: A6 0C     LDX $0C
$D617: A9 23     LDA #$23
$D619: 9D 80 01  STA $0180,X
$D61C: E8        INX
$D61D: 98        TYA
$D61E: 18        CLC
$D61F: 69 C0     ADC #$C0
$D621: 9D 80 01  STA $0180,X
$D624: E8        INX
$D625: B9 C0 07  LDA $07C0,Y
$D628: 9D 80 01  STA $0180,X
$D62B: E8        INX
$D62C: A9 FF     LDA #$FF
$D62E: 9D 80 01  STA $0180,X
$D631: E8        INX
$D632: 86 0C     STX $0C
$D634: 60        RTS
L_D635:
$D635: A5 04     LDA $04
$D637: 20 84 D6  JSR L_D684
$D63A: 20 84 D6  JSR L_D684
$D63D: 20 84 D6  JSR L_D684
$D640: 85 02     STA $02
$D642: 98        TYA
$D643: 29 02     AND #$02
$D645: D0 0F     BNE L_D656
$D647: 8A        TXA
$D648: 29 02     AND #$02
$D64A: F0 05     BEQ L_D651
$D64C: A9 F3     LDA #$F3
$D64E: 4C 62 D6  JMP L_D662
L_D651:
$D651: A9 FC     LDA #$FC
$D653: 4C 62 D6  JMP L_D662
L_D656:
$D656: 8A        TXA
$D657: 29 02     AND #$02
$D659: F0 05     BEQ L_D660
$D65B: A9 3F     LDA #$3F
$D65D: 4C 62 D6  JMP L_D662
L_D660:
$D660: A9 CF     LDA #$CF
L_D662:
$D662: 85 01     STA $01
$D664: 98        TYA
$D665: 0A        ASL A
$D666: 29 F8     AND #$F8
$D668: 85 00     STA $00
$D66A: 8A        TXA
$D66B: 4A        LSR A
$D66C: 4A        LSR A
$D66D: 18        CLC
$D66E: 65 00     ADC $00
$D670: A8        TAY
$D671: A5 01     LDA $01
$D673: 49 FF     EOR #$FF
$D675: 25 02     AND $02
$D677: 85 02     STA $02
$D679: B9 C0 07  LDA $07C0,Y
$D67C: 25 01     AND $01
$D67E: 05 02     ORA $02
$D680: 99 C0 07  STA $07C0,Y
$D683: 60        RTS
L_D684:
$D684: 0A        ASL A
$D685: 0A        ASL A
$D686: 05 04     ORA $04
$D688: 60        RTS
L_D689:
$D689: A2 01     LDX #$01
$D68B: 8E 16 40  STX JOY1_STROBE
$D68E: A0 00     LDY #$00
$D690: 8C 16 40  STY JOY1_STROBE
L_D693:
$D693: 84 00     STY $00
$D695: A0 08     LDY #$08
L_D697:
$D697: BD 16 40  LDA JOY1_STROBE,X
$D69A: 29 03     AND #$03
$D69C: C9 01     CMP #$01
$D69E: 66 00     ROR $00
$D6A0: 88        DEY
$D6A1: D0 F4     BNE L_D697
$D6A3: B5 06     LDA $06,X
$D6A5: 49 FF     EOR #$FF
$D6A7: 25 00     AND $00
$D6A9: 95 08     STA $08,X
$D6AB: A5 00     LDA $00
$D6AD: 95 06     STA $06,X
$D6AF: CA        DEX
$D6B0: 10 E1     BPL L_D693
$D6B2: 60        RTS
L_D6B3:
$D6B3: 20 FB D5  JSR L_D5FB
$D6B6: 85 14     STA $14
$D6B8: 18        CLC
$D6B9: 65 05     ADC $05
$D6BB: A6 0C     LDX $0C
$D6BD: 9D 80 01  STA $0180,X
$D6C0: E8        INX
$D6C1: 98        TYA
$D6C2: 9D 80 01  STA $0180,X
$D6C5: E8        INX
$D6C6: 85 13     STA $13
$D6C8: A0 00     LDY #$00
L_D6CA:
$D6CA: B1 11     LDA ($11),Y
$D6CC: 9D 80 01  STA $0180,X
$D6CF: E8        INX
$D6D0: C9 FF     CMP #$FF
$D6D2: F0 06     BEQ L_D6DA
$D6D4: 91 13     STA ($13),Y
$D6D6: C8        INY
$D6D7: 4C CA D6  JMP L_D6CA
L_D6DA:
$D6DA: 86 0C     STX $0C
$D6DC: 60        RTS
L_D6DD:
$D6DD: 20 FB D5  JSR L_D5FB
$D6E0: 18        CLC
$D6E1: 65 05     ADC $05
$D6E3: A6 0C     LDX $0C
$D6E5: 9D 80 01  STA $0180,X
$D6E8: E8        INX
$D6E9: 98        TYA
$D6EA: 9D 80 01  STA $0180,X
$D6ED: E8        INX
$D6EE: A0 00     LDY #$00
L_D6F0:
$D6F0: B1 11     LDA ($11),Y
$D6F2: 30 03     BMI L_D6F7
$D6F4: 18        CLC
$D6F5: 65 60     ADC $60
L_D6F7:
$D6F7: 9D 80 01  STA $0180,X
$D6FA: E8        INX
$D6FB: C9 FF     CMP #$FF
$D6FD: F0 04     BEQ L_D703
$D6FF: C8        INY
$D700: 4C F0 D6  JMP L_D6F0
L_D703:
$D703: 86 0C     STX $0C
$D705: 60        RTS
L_D706:
$D706: 20 13 D7  JSR L_D713
L_D709:
$D709: 20 FB D5  JSR L_D5FB
$D70C: 85 12     STA $12
$D70E: 84 11     STY $11
$D710: A0 00     LDY #$00
$D712: 60        RTS
L_D713:
$D713: 98        TYA
$D714: 4A        LSR A
$D715: 4A        LSR A
$D716: 4A        LSR A
$D717: A8        TAY
$D718: 8A        TXA
$D719: 4A        LSR A
$D71A: 4A        LSR A
$D71B: 4A        LSR A
$D71C: AA        TAX
$D71D: 60        RTS
L_D71E:
$D71E: 86 47     STX $47
$D720: 84 48     STY $48
$D722: 20 06 D7  JSR L_D706
L_D725:
$D725: A9 01     LDA #$01
$D727: 85 00     STA $00
$D729: A5 48     LDA $48
$D72B: 29 04     AND #$04
$D72D: F0 04     BEQ L_D733
$D72F: 06 00     ASL $00
$D731: 06 00     ASL $00
L_D733:
$D733: A5 47     LDA $47
$D735: 29 04     AND #$04
$D737: F0 02     BEQ L_D73B
$D739: 06 00     ASL $00
L_D73B:
$D73B: 60        RTS
L_D73C:
$D73C: A5 00     LDA $00
$D73E: 09 F0     ORA #$F0
$D740: 31 11     AND ($11),Y
$D742: 60        RTS
L_D743:
$D743: A5 00     LDA $00
$D745: 49 FF     EOR #$FF
$D747: 31 11     AND ($11),Y
$D749: 20 84 D7  JSR L_D784
$D74C: 60        RTS
L_D74D:
$D74D: B1 11     LDA ($11),Y
$D74F: 29 F0     AND #$F0
$D751: D0 08     BNE L_D75B
$D753: A5 00     LDA $00
$D755: 49 FF     EOR #$FF
$D757: 31 11     AND ($11),Y
$D759: 91 11     STA ($11),Y
L_D75B:
$D75B: 60        RTS
$D75C: A5 00     LDA $00
$D75E: 11 11     ORA ($11),Y
$D760: 20 84 D7  JSR L_D784
$D763: 60        RTS
L_D764:
$D764: B1 11     LDA ($11),Y
$D766: 29 F0     AND #$F0
$D768: D0 06     BNE L_D770
$D76A: A5 00     LDA $00
$D76C: 11 11     ORA ($11),Y
$D76E: 91 11     STA ($11),Y
L_D770:
$D770: 60        RTS
L_D771:
$D771: A5 12     LDA $12
$D773: 18        CLC
$D774: 65 05     ADC $05
$D776: 8D 06 20  STA PPUADDR
$D779: A5 11     LDA $11
$D77B: 8D 06 20  STA PPUADDR
$D77E: B1 11     LDA ($11),Y
$D780: 8D 07 20  STA PPUDATA
$D783: 60        RTS
L_D784:
$D784: 91 11     STA ($11),Y
$D786: 86 47     STX $47
$D788: A6 0C     LDX $0C
$D78A: A5 12     LDA $12
$D78C: 18        CLC
$D78D: 69 1C     ADC #$1C
$D78F: 9D 80 01  STA $0180,X
$D792: E8        INX
$D793: A5 11     LDA $11
$D795: 9D 80 01  STA $0180,X
$D798: E8        INX
$D799: B1 11     LDA ($11),Y
$D79B: 9D 80 01  STA $0180,X
$D79E: E8        INX
$D79F: A9 FF     LDA #$FF
$D7A1: 9D 80 01  STA $0180,X
$D7A4: E8        INX
$D7A5: 86 0C     STX $0C
$D7A7: A6 47     LDX $47
$D7A9: 60        RTS
L_D7AA:
$D7AA: 18        CLC
$D7AB: 65 11     ADC $11
$D7AD: 85 11     STA $11
$D7AF: 90 02     BCC L_D7B3
$D7B1: E6 12     INC $12
L_D7B3:
$D7B3: 60        RTS
CopyPpuBuffer:
L_D7B4:
$D7B4: A9 00     LDA #$00
$D7B6: 85 11     STA $11
$D7B8: A8        TAY
$D7B9: A9 04     LDA #$04
$D7BB: 85 12     STA $12
L_D7BD:
$D7BD: 20 71 D7  JSR L_D771
$D7C0: A9 01     LDA #$01
$D7C2: 20 AA D7  JSR L_D7AA
$D7C5: A5 12     LDA $12
$D7C7: C9 08     CMP #$08
$D7C9: D0 F2     BNE L_D7BD
$D7CB: 60        RTS
L_D7CC:
$D7CC: A2 00     LDX #$00
$D7CE: A9 11     LDA #$11
L_D7D0:
$D7D0: 9D 00 04  STA $0400,X
$D7D3: 9D 00 05  STA $0500,X
$D7D6: 9D 00 06  STA $0600,X
$D7D9: 9D 00 07  STA $0700,X
$D7DC: E8        INX
$D7DD: D0 F1     BNE L_D7D0
$D7DF: A9 00     LDA #$00
$D7E1: A2 C0     LDX #$C0
L_D7E3:
$D7E3: 9D 00 07  STA $0700,X
$D7E6: E8        INX
$D7E7: D0 FA     BNE L_D7E3
$D7E9: A6 56     LDX $56
$D7EB: A4 57     LDY $57
$D7ED: 20 FB D5  JSR L_D5FB
$D7F0: 85 12     STA $12
$D7F2: 84 11     STY $11
L_D7F4:
$D7F4: A4 5B     LDY $5B
$D7F6: 88        DEY
L_D7F7:
$D7F7: A9 00     LDA #$00
$D7F9: 91 11     STA ($11),Y
$D7FB: 88        DEY
$D7FC: 10 F9     BPL L_D7F7
$D7FE: C6 5A     DEC $5A
$D800: F0 08     BEQ L_D80A
$D802: A9 20     LDA #$20
$D804: 20 AA D7  JSR L_D7AA
$D807: 4C F4 D7  JMP L_D7F4
L_D80A:
$D80A: 60        RTS
L_D80B:
$D80B: 48        PHA
$D80C: 85 00     STA $00
$D80E: 20 13 D7  JSR L_D713
$D811: 86 47     STX $47
$D813: 84 48     STY $48
$D815: A4 00     LDY $00
$D817: B9 BB DA  LDA $DABB,Y
$D81A: 85 04     STA $04
$D81C: A4 48     LDY $48
$D81E: 20 12 D6  JSR L_D612
$D821: A5 48     LDA $48
$D823: 29 FE     AND #$FE
$D825: A8        TAY
$D826: A5 47     LDA $47
$D828: 29 FE     AND #$FE
$D82A: AA        TAX
$D82B: 20 09 D7  JSR L_D709
$D82E: 68        PLA
$D82F: 0A        ASL A
$D830: 0A        ASL A
$D831: AA        TAX
$D832: BD CB DA  LDA $DACB,X
$D835: E8        INX
$D836: 20 84 D7  JSR L_D784
$D839: A9 01     LDA #$01
$D83B: 20 AA D7  JSR L_D7AA
$D83E: BD CB DA  LDA $DACB,X
$D841: E8        INX
$D842: 20 84 D7  JSR L_D784
$D845: A9 1F     LDA #$1F
$D847: 20 AA D7  JSR L_D7AA
$D84A: BD CB DA  LDA $DACB,X
$D84D: E8        INX
$D84E: 20 84 D7  JSR L_D784
$D851: A9 01     LDA #$01
$D853: 20 AA D7  JSR L_D7AA
$D856: BD CB DA  LDA $DACB,X
$D859: E8        INX
$D85A: 20 84 D7  JSR L_D784
$D85D: 60        RTS
L_D85E:
$D85E: 86 5D     STX $5D
$D860: AA        TAX
$D861: 98        TYA
$D862: 18        CLC
$D863: 69 20     ADC #$20
$D865: 85 5E     STA $5E
$D867: A9 00     LDA #$00
$D869: 85 11     STA $11
$D86B: A9 10     LDA #$10
$D86D: 85 12     STA $12
L_D86F:
$D86F: CA        DEX
$D870: 30 08     BMI L_D87A
$D872: A9 10     LDA #$10
$D874: 20 AA D7  JSR L_D7AA
$D877: 4C 6F D8  JMP L_D86F
L_D87A:
$D87A: A5 12     LDA $12
$D87C: 8D 06 20  STA PPUADDR
$D87F: A5 11     LDA $11
$D881: 8D 06 20  STA PPUADDR
$D884: AD 07 20  LDA PPUDATA
$D887: A9 08     LDA #$08
$D889: 85 5A     STA $5A
L_D88B:
$D88B: AD 07 20  LDA PPUDATA
$D88E: 48        PHA
$D88F: C6 5A     DEC $5A
$D891: D0 F8     BNE L_D88B
$D893: A9 08     LDA #$08
$D895: 85 5A     STA $5A
L_D897:
$D897: 68        PLA
$D898: 85 02     STA $02
$D89A: A9 80     LDA #$80
$D89C: 85 03     STA $03
L_D89E:
$D89E: A6 5D     LDX $5D
$D8A0: A4 5E     LDY $5E
$D8A2: 20 1E D7  JSR L_D71E
$D8A5: A5 02     LDA $02
$D8A7: 25 03     AND $03
$D8A9: F0 06     BEQ L_D8B1
$D8AB: 20 64 D7  JSR L_D764
$D8AE: 4C B4 D8  JMP L_D8B4
L_D8B1:
$D8B1: 20 4D D7  JSR L_D74D
L_D8B4:
$D8B4: A5 5D     LDA $5D
$D8B6: 18        CLC
$D8B7: 69 04     ADC #$04
$D8B9: 85 5D     STA $5D
$D8BB: 46 03     LSR $03
$D8BD: 90 DF     BCC L_D89E
$D8BF: A5 5D     LDA $5D
$D8C1: 38        SEC
$D8C2: E9 20     SBC #$20
$D8C4: 85 5D     STA $5D
$D8C6: A5 5E     LDA $5E
$D8C8: 38        SEC
$D8C9: E9 04     SBC #$04
$D8CB: 85 5E     STA $5E
$D8CD: C6 5A     DEC $5A
$D8CF: D0 C6     BNE L_D897
$D8D1: 60        RTS
L_D8D2:
$D8D2: A0 00     LDY #$00
$D8D4: 84 5F     STY $5F
L_D8D6:
$D8D6: B1 13     LDA ($13),Y
$D8D8: C9 FF     CMP #$FF
$D8DA: F0 19     BEQ L_D8F5
$D8DC: C8        INY
$D8DD: 84 5F     STY $5F
$D8DF: A6 56     LDX $56
$D8E1: A4 57     LDY $57
$D8E3: 18        CLC
$D8E4: 65 60     ADC $60
$D8E6: 20 5E D8  JSR L_D85E
$D8E9: A5 56     LDA $56
$D8EB: 18        CLC
$D8EC: 69 20     ADC #$20
$D8EE: 85 56     STA $56
$D8F0: A4 5F     LDY $5F
$D8F2: 4C D6 D8  JMP L_D8D6
L_D8F5:
$D8F5: 60        RTS
L_D8F6:
$D8F6: A5 0B     LDA $0B
L_D8F8:
$D8F8: C5 0B     CMP $0B
$D8FA: F0 FC     BEQ L_D8F8
$D8FC: 60        RTS
L_D8FD:
$D8FD: A6 0C     LDX $0C
$D8FF: A9 00     LDA #$00
$D901: 9D 80 01  STA $0180,X
$D904: AA        TAX
L_D905:
$D905: E4 0C     CPX $0C
$D907: F0 26     BEQ L_D92F
$D909: BD 80 01  LDA $0180,X
$D90C: E8        INX
$D90D: 8D 06 20  STA PPUADDR
$D910: BD 80 01  LDA $0180,X
$D913: E8        INX
$D914: 8D 06 20  STA PPUADDR
L_D917:
$D917: BD 80 01  LDA $0180,X
$D91A: E8        INX
$D91B: C9 FF     CMP #$FF
$D91D: D0 0A     BNE L_D929
$D91F: BD 80 01  LDA $0180,X
$D922: C9 FF     CMP #$FF
$D924: D0 DF     BNE L_D905
$D926: BD 7F 01  LDA $017F,X
L_D929:
$D929: 8D 07 20  STA PPUDATA
$D92C: 4C 17 D9  JMP L_D917
L_D92F:
$D92F: A9 00     LDA #$00
$D931: 85 0C     STA $0C
$D933: 60        RTS
L_D934:
$D934: B9 00 00  LDA $0000,Y
$D937: D0 05     BNE L_D93E
$D939: C8        INY
$D93A: E8        INX
$D93B: 4C 34 D9  JMP L_D934
L_D93E:
$D93E: C9 FF     CMP #$FF
$D940: D0 08     BNE L_D94A
$D942: A5 6B     LDA $6B
$D944: D0 02     BNE L_D948
$D946: CA        DEX
$D947: 88        DEY
L_D948:
$D948: CA        DEX
$D949: 88        DEY
L_D94A:
$D94A: A9 00     LDA #$00
$D94C: 85 12     STA $12
$D94E: 84 11     STY $11
$D950: 60        RTS
L_D951:
$D951: A9 10     LDA #$10
$D953: 85 56     STA $56
$D955: A9 64     LDA #$64
$D957: 85 57     STA $57
$D959: A9 30     LDA #$30
$D95B: 85 60     STA $60
$D95D: A0 3D     LDY #$3D
L_D95F:
$D95F: B9 00 00  LDA $0000,Y
$D962: D0 0B     BNE L_D96F
$D964: C8        INY
$D965: A5 56     LDA $56
$D967: 18        CLC
$D968: 69 20     ADC #$20
$D96A: 85 56     STA $56
$D96C: 4C 5F D9  JMP L_D95F
L_D96F:
$D96F: A9 00     LDA #$00
$D971: 85 14     STA $14
$D973: 84 13     STY $13
$D975: 20 D2 D8  JSR L_D8D2
$D978: A9 00     LDA #$00
$D97A: 85 60     STA $60
$D97C: 60        RTS
L_D97D:
$D97D: A2 00     LDX #$00
$D97F: A0 00     LDY #$00
L_D981:
$D981: B5 15     LDA $15,X
$D983: D5 3D     CMP $3D,X
$D985: D0 08     BNE L_D98F
$D987: E8        INX
$D988: E0 07     CPX #$07
$D98A: F0 12     BEQ L_D99E
$D98C: 4C 81 D9  JMP L_D981
L_D98F:
$D98F: 30 0D     BMI L_D99E
$D991: A2 00     LDX #$00
L_D993:
$D993: B5 15     LDA $15,X
$D995: 95 3D     STA $3D,X
$D997: E8        INX
$D998: E0 07     CPX #$07
$D99A: D0 F7     BNE L_D993
$D99C: A0 01     LDY #$01
L_D99E:
$D99E: A2 00     LDX #$00
L_D9A0:
$D9A0: B5 1D     LDA $1D,X
$D9A2: D5 3D     CMP $3D,X
$D9A4: D0 08     BNE L_D9AE
$D9A6: E8        INX
$D9A7: E0 07     CPX #$07
$D9A9: F0 12     BEQ L_D9BD
$D9AB: 4C A0 D9  JMP L_D9A0
L_D9AE:
$D9AE: 30 0D     BMI L_D9BD
$D9B0: A2 00     LDX #$00
L_D9B2:
$D9B2: B5 1D     LDA $1D,X
$D9B4: 95 3D     STA $3D,X
$D9B6: E8        INX
$D9B7: E0 07     CPX #$07
$D9B9: D0 F7     BNE L_D9B2
$D9BB: A0 FF     LDY #$FF
L_D9BD:
$D9BD: 60        RTS
L_D9BE:
$D9BE: 8A        TXA
$D9BF: 0A        ASL A
$D9C0: 0A        ASL A
$D9C1: 0A        ASL A
$D9C2: 18        CLC
$D9C3: 69 06     ADC #$06
$D9C5: AA        TAX
$D9C6: A0 06     LDY #$06
$D9C8: 18        CLC
L_D9C9:
$D9C9: B9 35 00  LDA $0035,Y
$D9CC: 75 15     ADC $15,X
$D9CE: C9 0A     CMP #$0A
$D9D0: 30 07     BMI L_D9D9
$D9D2: 38        SEC
$D9D3: E9 0A     SBC #$0A
$D9D5: 38        SEC
$D9D6: 4C DA D9  JMP L_D9DA
L_D9D9:
$D9D9: 18        CLC
L_D9DA:
$D9DA: 95 15     STA $15,X
$D9DC: CA        DEX
$D9DD: 88        DEY
$D9DE: 10 E9     BPL L_D9C9
$D9E0: 60        RTS
L_D9E1:
$D9E1: 85 00     STA $00
$D9E3: A2 35     LDX #$35
$D9E5: 20 FE D9  JSR L_D9FE
$D9E8: A5 00     LDA $00
$D9EA: F0 0D     BEQ L_D9F9
$D9EC: 29 0F     AND #$0F
$D9EE: 85 3A     STA $3A
$D9F0: A5 00     LDA $00
$D9F2: 4A        LSR A
$D9F3: 4A        LSR A
$D9F4: 4A        LSR A
$D9F5: 4A        LSR A
$D9F6: 85 39     STA $39
$D9F8: 60        RTS
L_D9F9:
$D9F9: A9 01     LDA #$01
$D9FB: 85 38     STA $38
$D9FD: 60        RTS
InitRecord:
L_D9FE:
$D9FE: A9 00     LDA #$00
$DA00: 95 00     STA $00,X
$DA02: 95 01     STA $01,X
$DA04: 95 02     STA $02,X
$DA06: 95 03     STA $03,X
$DA08: 95 04     STA $04,X
$DA0A: 95 05     STA $05,X
$DA0C: 95 06     STA $06,X
$DA0E: A9 FF     LDA #$FF
$DA10: 95 07     STA $07,X
$DA12: 60        RTS
L_DA13:
$DA13: 85 00     STA $00
$DA15: A2 35     LDX #$35
$DA17: 20 FE D9  JSR L_D9FE
$DA1A: A5 00     LDA $00
L_DA1C:
$DA1C: C9 0A     CMP #$0A
$DA1E: 90 08     BCC L_DA28
$DA20: 38        SEC
$DA21: E9 0A     SBC #$0A
$DA23: E6 3A     INC $3A
$DA25: 4C 1C DA  JMP L_DA1C
L_DA28:
$DA28: 85 3B     STA $3B
$DA2A: 60        RTS
L_DA2B:
$DA2B: 8A        TXA
$DA2C: 85 47     STA $47
$DA2E: 18        CLC
$DA2F: 69 03     ADC #$03
$DA31: AA        TAX
$DA32: 98        TYA
$DA33: 38        SEC
$DA34: E9 08     SBC #$08
$DA36: 85 48     STA $48
$DA38: 20 06 D7  JSR L_D706
$DA3B: B1 11     LDA ($11),Y
$DA3D: C9 22     CMP #$22
$DA3F: D0 06     BNE L_DA47
$DA41: A5 04     LDA $04
$DA43: 05 6E     ORA $6E
$DA45: 85 04     STA $04
L_DA47:
$DA47: A6 0D     LDX $0D
$DA49: A5 48     LDA $48
$DA4B: 9D 00 02  STA $0200,X
$DA4E: A5 53     LDA $53
$DA50: 9D 01 02  STA $0201,X
$DA53: A5 04     LDA $04
$DA55: 9D 02 02  STA $0202,X
$DA58: A5 47     LDA $47
$DA5A: 9D 03 02  STA $0203,X
$DA5D: 8A        TXA
$DA5E: 18        CLC
$DA5F: 65 0E     ADC $0E
$DA61: 85 0D     STA $0D
$DA63: 60        RTS
L_DA64:
$DA64: 0A        ASL A
$DA65: 18        CLC
$DA66: 65 53     ADC $53
$DA68: 85 53     STA $53
$DA6A: 8A        TXA
$DA6B: 38        SEC
$DA6C: E9 05     SBC #$05
$DA6E: AA        TAX
$DA6F: 20 2B DA  JSR L_DA2B
$DA72: 60        RTS
L_DA73:
$DA73: 0A        ASL A
$DA74: 0A        ASL A
$DA75: 0A        ASL A
$DA76: 18        CLC
$DA77: 65 53     ADC $53
$DA79: 85 53     STA $53
L_DA7B:
$DA7B: 86 54     STX $54
$DA7D: 84 55     STY $55
$DA7F: 8A        TXA
$DA80: 38        SEC
$DA81: E9 08     SBC #$08
$DA83: AA        TAX
$DA84: 20 2B DA  JSR L_DA2B
$DA87: E6 53     INC $53
$DA89: E6 53     INC $53
$DA8B: A6 54     LDX $54
$DA8D: A4 55     LDY $55
$DA8F: 20 2B DA  JSR L_DA2B
$DA92: 60        RTS
HideSprites:
L_DA93:
$DA93: A6 0D     LDX $0D
$DA95: A5 0E     LDA $0E
$DA97: 49 FF     EOR #$FF
$DA99: 18        CLC
$DA9A: 69 01     ADC #$01
$DA9C: 85 0E     STA $0E
L_DA9E:
$DA9E: 8A        TXA
$DA9F: 18        CLC
$DAA0: 65 0E     ADC $0E
$DAA2: AA        TAX
$DAA3: A9 F0     LDA #$F0
$DAA5: 9D 00 02  STA $0200,X
$DAA8: E0 04     CPX #$04
$DAAA: D0 F2     BNE L_DA9E
$DAAC: 86 0D     STX $0D
$DAAE: 60        RTS
L_DAAF:
$DAAF: F0 09     BEQ L_DABA
$DAB1: B0 05     BCS L_DAB8
$DAB3: A9 FF     LDA #$FF
$DAB5: 4C BA DA  JMP L_DABA
L_DAB8:
$DAB8: A9 01     LDA #$01
L_DABA:
$DABA: 60        RTS
$DABB: 00        BRK
$DABC: 00        BRK
$DABD: 00        BRK
$DABE: 00        BRK
$DABF: 00        BRK
$DAC0: 03        db $03
$DAC1: 03        db $03
$DAC2: 03        db $03
$DAC3: 03        db $03
$DAC4: 03        db $03
$DAC5: 01 02     ORA ($02,X)
$DAC7: 03        db $03
$DAC8: 00        BRK
$DAC9: 00        BRK
$DACA: 00        BRK
$DACB: 00        BRK
$DACC: 0F        db $0F
$DACD: 00        BRK
$DACE: 0F        db $0F
$DACF: 00        BRK
$DAD0: 00        BRK
$DAD1: 0F        db $0F
$DAD2: 0F        db $0F
$DAD3: 0F        db $0F
$DAD4: 00        BRK
$DAD5: 0F        db $0F
$DAD6: 00        BRK
$DAD7: 0F        db $0F
$DAD8: 0F        db $0F
$DAD9: 00        BRK
$DADA: 00        BRK
$DADB: 0F        db $0F
$DADC: 0F        db $0F
$DADD: 0F        db $0F
$DADE: 0F        db $0F
$DADF: 20 10 20  JSR L_2010
$DAE2: 10 20     BPL L_DB04
$DAE4: 20 10 10  JSR L_1010
$DAE7: 10 20     BPL L_DB09
$DAE9: 10 20     BPL L_DB0B
$DAEB: 10 10     BPL L_DAFD
$DAED: 20 20 10  JSR L_1020
$DAF0: 10 10     BPL L_DB02
$DAF2: 10 12     BPL L_DB06
$DAF4: 12        db $12
$DAF5: 12        db $12
$DAF6: 12        db $12
$DAF7: 22        db $22
$DAF8: 22        db $22
$DAF9: 22        db $22
$DAFA: 22        db $22
$DAFB: 21 21     AND ($21,X)
L_DAFD:
$DAFD: 21 21     AND ($21,X)
$DAFF: 00        BRK
$DB00: 00        BRK
$DB01: 00        BRK
L_DB02:
$DB02: 00        BRK
$DB03: 00        BRK
L_DB04:
$DB04: 00        BRK
$DB05: 00        BRK
L_DB06:
$DB06: 00        BRK
$DB07: 00        BRK
$DB08: 00        BRK
L_DB09:
$DB09: 00        BRK
$DB0A: 00        BRK
L_DB0B:
$DB0B: AD 11 03  LDA $0311
$DB0E: F0 14     BEQ L_DB24
$DB10: A2 00     LDX #$00
$DB12: 20 38 DB  JSR L_DB38
$DB15: D0 20     BNE L_DB37
$DB17: A2 01     LDX #$01
$DB19: 20 38 DB  JSR L_DB38
$DB1C: D0 19     BNE L_DB37
$DB1E: A9 00     LDA #$00
$DB20: 8D 11 03  STA $0311
$DB23: 60        RTS
L_DB24:
$DB24: A2 00     LDX #$00
$DB26: 20 38 DB  JSR L_DB38
$DB29: D0 07     BNE L_DB32
$DB2B: A2 01     LDX #$01
$DB2D: 20 38 DB  JSR L_DB38
$DB30: F0 05     BEQ L_DB37
L_DB32:
$DB32: A9 01     LDA #$01
$DB34: 8D 11 03  STA $0311
L_DB37:
$DB37: 60        RTS
L_DB38:
$DB38: B5 06     LDA $06,X
$DB3A: 29 F0     AND #$F0
$DB3C: F0 07     BEQ L_DB45
$DB3E: B5 A0     LDA $A0,X
$DB40: F0 03     BEQ L_DB45
$DB42: A9 01     LDA #$01
$DB44: 60        RTS
L_DB45:
$DB45: A9 00     LDA #$00
$DB47: 60        RTS
L_DB48:
$DB48: A5 82     LDA $82
$DB4A: F0 03     BEQ L_DB4F
$DB4C: C6 82     DEC $82
$DB4E: 60        RTS
L_DB4F:
$DB4F: A5 7F     LDA $7F
$DB51: F0 21     BEQ L_DB74
$DB53: A5 6C     LDA $6C
$DB55: 85 5A     STA $5A
L_DB57:
$DB57: A6 5A     LDX $5A
$DB59: B5 A0     LDA $A0,X
$DB5B: D0 0F     BNE L_DB6C
$DB5D: A5 84     LDA $84
$DB5F: 85 82     STA $82
$DB61: 20 63 E3  JSR L_E363
$DB64: C6 7F     DEC $7F
$DB66: A5 7F     LDA $7F
$DB68: 20 B1 C8  JSR L_C8B1
$DB6B: 60        RTS
L_DB6C:
$DB6C: C6 5A     DEC $5A
$DB6E: A5 5A     LDA $5A
$DB70: C9 01     CMP #$01
$DB72: D0 E3     BNE L_DB57
L_DB74:
$DB74: 60        RTS
L_DB75:
$DB75: A5 0B     LDA $0B
$DB77: 29 01     AND #$01
$DB79: D0 06     BNE L_DB81
$DB7B: A5 0B     LDA $0B
$DB7D: 29 03     AND #$03
$DB7F: D0 6F     BNE L_DBF0
L_DB81:
$DB81: A2 01     LDX #$01
L_DB83:
$DB83: B5 A0     LDA $A0,X
$DB85: 10 66     BPL L_DBED
$DB87: C9 E0     CMP #$E0
$DB89: B0 62     BCS L_DBED
$DB8B: B5 6F     LDA $6F,X
$DB8D: F0 05     BEQ L_DB94
$DB8F: D6 6F     DEC $6F,X
$DB91: 4C A6 DB  JMP L_DBA6
L_DB94:
$DB94: BD 03 01  LDA $0103,X
$DB97: 10 04     BPL L_DB9D
$DB99: 29 10     AND #$10
$DB9B: D0 09     BNE L_DBA6
L_DB9D:
$DB9D: B5 06     LDA $06,X
$DB9F: 20 51 E4  JSR L_E451
$DBA2: 85 00     STA $00
$DBA4: 10 0E     BPL L_DBB4
L_DBA6:
$DBA6: A9 80     LDA #$80
$DBA8: 20 20 E4  JSR L_E420
$DBAB: A9 08     LDA #$08
$DBAD: 15 A0     ORA $A0,X
$DBAF: 95 A0     STA $A0,X
$DBB1: 4C ED DB  JMP L_DBED
L_DBB4:
$DBB4: BD 03 01  LDA $0103,X
$DBB7: 10 0E     BPL L_DBC7
$DBB9: 29 1F     AND #$1F
$DBBB: D0 0A     BNE L_DBC7
$DBBD: A9 9C     LDA #$9C
$DBBF: 9D 03 01  STA $0103,X
$DBC2: A9 01     LDA #$01
$DBC4: 8D 10 03  STA $0310
L_DBC7:
$DBC7: B5 A0     LDA $A0,X
$DBC9: 29 03     AND #$03
$DBCB: C5 00     CMP $00
$DBCD: F0 18     BEQ L_DBE7
$DBCF: 49 02     EOR #$02
$DBD1: C5 00     CMP $00
$DBD3: F0 12     BEQ L_DBE7
$DBD5: B5 90     LDA $90,X
$DBD7: 18        CLC
$DBD8: 69 04     ADC #$04
$DBDA: 29 F8     AND #$F8
$DBDC: 95 90     STA $90,X
$DBDE: B5 98     LDA $98,X
$DBE0: 18        CLC
$DBE1: 69 04     ADC #$04
$DBE3: 29 F8     AND #$F8
$DBE5: 95 98     STA $98,X
L_DBE7:
$DBE7: A5 00     LDA $00
$DBE9: 09 A0     ORA #$A0
$DBEB: 95 A0     STA $A0,X
L_DBED:
$DBED: CA        DEX
$DBEE: 10 93     BPL L_DB83
L_DBF0:
$DBF0: 60        RTS
L_DBF1:
$DBF1: A9 07     LDA #$07
$DBF3: 85 5A     STA $5A
$DBF5: AD 00 01  LDA $0100
$DBF8: F0 09     BEQ L_DC03
$DBFA: A5 0B     LDA $0B
$DBFC: 29 3F     AND #$3F
$DBFE: D0 03     BNE L_DC03
$DC00: CE 00 01  DEC $0100
L_DC03:
$DC03: A6 5A     LDX $5A
$DC05: E0 02     CPX #$02
$DC07: B0 0F     BCS L_DC18
$DC09: A5 0B     LDA $0B
$DC0B: 29 01     AND #$01
$DC0D: D0 26     BNE L_DC35
$DC0F: A5 0B     LDA $0B
$DC11: 29 03     AND #$03
$DC13: D0 23     BNE L_DC38
$DC15: 4C 35 DC  JMP L_DC35
L_DC18:
$DC18: AD 00 01  LDA $0100
$DC1B: F0 08     BEQ L_DC25
$DC1D: B5 A0     LDA $A0,X
$DC1F: 10 04     BPL L_DC25
$DC21: C9 E0     CMP #$E0
$DC23: 90 13     BCC L_DC38
L_DC25:
$DC25: B5 A8     LDA $A8,X
$DC27: 29 F0     AND #$F0
$DC29: C9 A0     CMP #$A0
$DC2B: F0 08     BEQ L_DC35
$DC2D: A5 5A     LDA $5A
$DC2F: 45 0B     EOR $0B
$DC31: 29 01     AND #$01
$DC33: F0 03     BEQ L_DC38
L_DC35:
$DC35: 20 3D DC  JSR L_DC3D
L_DC38:
$DC38: C6 5A     DEC $5A
$DC3A: 10 C7     BPL L_DC03
$DC3C: 60        RTS
L_DC3D:
$DC3D: B5 A0     LDA $A0,X
$DC3F: 4A        LSR A
$DC40: 4A        LSR A
$DC41: 4A        LSR A
$DC42: 29 FE     AND #$FE
$DC44: A8        TAY
$DC45: B9 98 E4  LDA $E498,Y
$DC48: 85 11     STA $11
$DC4A: B9 99 E4  LDA $E499,Y
$DC4D: 85 12     STA $12
$DC4F: 6C 11 00  JMP ($0011)
$DC52: E0 02     CPX #$02
$DC54: B0 15     BCS L_DC6B
$DC56: BD 03 01  LDA $0103,X
$DC59: 10 10     BPL L_DC6B
$DC5B: 29 7F     AND #$7F
$DC5D: F0 0C     BEQ L_DC6B
$DC5F: DE 03 01  DEC $0103,X
$DC62: B5 B0     LDA $B0,X
$DC64: 49 04     EOR #$04
$DC66: 95 B0     STA $B0,X
$DC68: 4C 97 DC  JMP L_DC97
L_DC6B:
$DC6B: B5 A0     LDA $A0,X
$DC6D: 38        SEC
$DC6E: E9 04     SBC #$04
$DC70: 95 A0     STA $A0,X
$DC72: 29 0C     AND #$0C
$DC74: D0 05     BNE L_DC7B
$DC76: A9 A0     LDA #$A0
$DC78: 20 20 E4  JSR L_E420
L_DC7B:
$DC7B: 60        RTS
$DC7C: E0 02     CPX #$02
$DC7E: 90 17     BCC L_DC97
$DC80: B5 90     LDA $90,X
$DC82: 29 07     AND #$07
$DC84: D0 11     BNE L_DC97
$DC86: B5 98     LDA $98,X
$DC88: 29 07     AND #$07
$DC8A: D0 0B     BNE L_DC97
$DC8C: 20 4D D4  JSR L_D44D
$DC8F: 29 0F     AND #$0F
$DC91: D0 04     BNE L_DC97
$DC93: 20 72 DE  JSR L_DE72
$DC96: 60        RTS
L_DC97:
$DC97: B5 A0     LDA $A0,X
$DC99: 29 03     AND #$03
$DC9B: A8        TAY
$DC9C: B9 70 E4  LDA $E470,Y
$DC9F: 0A        ASL A
$DCA0: 0A        ASL A
$DCA1: 0A        ASL A
$DCA2: 85 59     STA $59
$DCA4: B9 70 E4  LDA $E470,Y
$DCA7: 18        CLC
$DCA8: 75 98     ADC $98,X
$DCAA: 85 57     STA $57
$DCAC: B9 6C E4  LDA $E46C,Y
$DCAF: 0A        ASL A
$DCB0: 0A        ASL A
$DCB1: 0A        ASL A
$DCB2: 85 58     STA $58
$DCB4: B9 6C E4  LDA $E46C,Y
$DCB7: 18        CLC
$DCB8: 75 90     ADC $90,X
$DCBA: 85 56     STA $56
$DCBC: 18        CLC
$DCBD: 65 58     ADC $58
$DCBF: 18        CLC
$DCC0: 65 59     ADC $59
$DCC2: 20 6E DD  JSR L_DD6E
$DCC5: AA        TAX
$DCC6: A5 57     LDA $57
$DCC8: 18        CLC
$DCC9: 65 58     ADC $58
$DCCB: 18        CLC
$DCCC: 65 59     ADC $59
$DCCE: 20 76 DD  JSR L_DD76
$DCD1: A8        TAY
$DCD2: 20 06 D7  JSR L_D706
$DCD5: B1 11     LDA ($11),Y
$DCD7: 30 38     BMI L_DD11
$DCD9: F0 04     BEQ L_DCDF
$DCDB: C9 20     CMP #$20
$DCDD: 90 32     BCC L_DD11
L_DCDF:
$DCDF: A5 56     LDA $56
$DCE1: 18        CLC
$DCE2: 65 58     ADC $58
$DCE4: 38        SEC
$DCE5: E5 59     SBC $59
$DCE7: 20 6E DD  JSR L_DD6E
$DCEA: AA        TAX
$DCEB: A5 57     LDA $57
$DCED: 18        CLC
$DCEE: 65 59     ADC $59
$DCF0: 38        SEC
$DCF1: E5 58     SBC $58
$DCF3: 20 76 DD  JSR L_DD76
$DCF6: A8        TAY
$DCF7: 20 06 D7  JSR L_D706
$DCFA: B1 11     LDA ($11),Y
$DCFC: 30 13     BMI L_DD11
$DCFE: F0 04     BEQ L_DD04
$DD00: C9 20     CMP #$20
$DD02: 90 0D     BCC L_DD11
L_DD04:
$DD04: A6 5A     LDX $5A
$DD06: A5 56     LDA $56
$DD08: 95 90     STA $90,X
$DD0A: A5 57     LDA $57
$DD0C: 95 98     STA $98,X
$DD0E: 4C 29 DD  JMP L_DD29
L_DD11:
$DD11: A6 5A     LDX $5A
$DD13: E0 02     CPX #$02
$DD15: 90 12     BCC L_DD29
$DD17: 20 4D D4  JSR L_D44D
$DD1A: 29 03     AND #$03
$DD1C: F0 12     BEQ L_DD30
$DD1E: A9 80     LDA #$80
$DD20: 20 20 E4  JSR L_E420
$DD23: A9 08     LDA #$08
$DD25: 15 A0     ORA $A0,X
$DD27: 95 A0     STA $A0,X
L_DD29:
$DD29: B5 B0     LDA $B0,X
$DD2B: 49 04     EOR #$04
$DD2D: 95 B0     STA $B0,X
$DD2F: 60        RTS
L_DD30:
$DD30: B5 90     LDA $90,X
$DD32: 29 07     AND #$07
$DD34: D0 0B     BNE L_DD41
$DD36: B5 98     LDA $98,X
$DD38: 29 07     AND #$07
$DD3A: D0 05     BNE L_DD41
$DD3C: A9 90     LDA #$90
$DD3E: 20 20 E4  JSR L_E420
L_DD41:
$DD41: B5 A0     LDA $A0,X
$DD43: 49 02     EOR #$02
$DD45: 95 A0     STA $A0,X
$DD47: 60        RTS
$DD48: 20 4D D4  JSR L_D44D
$DD4B: 29 01     AND #$01
$DD4D: F0 1B     BEQ L_DD6A
$DD4F: 20 4D D4  JSR L_D44D
$DD52: 29 01     AND #$01
$DD54: F0 08     BEQ L_DD5E
$DD56: B5 A0     LDA $A0,X
$DD58: 18        CLC
$DD59: 69 01     ADC #$01
$DD5B: 4C 63 DD  JMP L_DD63
L_DD5E:
$DD5E: B5 A0     LDA $A0,X
$DD60: 38        SEC
$DD61: E9 01     SBC #$01
L_DD63:
$DD63: 29 03     AND #$03
$DD65: 09 A0     ORA #$A0
$DD67: 95 A0     STA $A0,X
$DD69: 60        RTS
L_DD6A:
$DD6A: 20 72 DE  JSR L_DE72
$DD6D: 60        RTS
L_DD6E:
$DD6E: C5 56     CMP $56
$DD70: 90 03     BCC L_DD75
$DD72: 38        SEC
$DD73: E9 01     SBC #$01
L_DD75:
$DD75: 60        RTS
L_DD76:
$DD76: C5 57     CMP $57
$DD78: 90 03     BCC L_DD7D
$DD7A: 38        SEC
$DD7B: E9 01     SBC #$01
L_DD7D:
$DD7D: 60        RTS
$DD7E: A5 90     LDA $90
$DD80: 85 71     STA $71
$DD82: A5 98     LDA $98
$DD84: 85 72     STA $72
$DD86: 4C 9C DD  JMP L_DD9C
$DD89: A5 91     LDA $91
$DD8B: 85 71     STA $71
$DD8D: A5 99     LDA $99
$DD8F: 85 72     STA $72
$DD91: 4C 9C DD  JMP L_DD9C
$DD94: A9 78     LDA #$78
$DD96: 85 71     STA $71
$DD98: A9 D8     LDA #$D8
$DD9A: 85 72     STA $72
L_DD9C:
$DD9C: 20 A2 DD  JSR L_DDA2
$DD9F: 95 A0     STA $A0,X
$DDA1: 60        RTS
L_DDA2:
$DDA2: A5 71     LDA $71
$DDA4: 38        SEC
$DDA5: F5 90     SBC $90,X
$DDA7: 20 AF DA  JSR L_DAAF
$DDAA: 18        CLC
$DDAB: 69 01     ADC #$01
$DDAD: 85 64     STA $64
$DDAF: A5 72     LDA $72
$DDB1: 38        SEC
$DDB2: F5 98     SBC $98,X
$DDB4: 20 AF DA  JSR L_DAAF
$DDB7: 18        CLC
$DDB8: 69 01     ADC #$01
$DDBA: 85 65     STA $65
$DDBC: 0A        ASL A
$DDBD: 18        CLC
$DDBE: 65 65     ADC $65
$DDC0: 18        CLC
$DDC1: 65 64     ADC $64
$DDC3: 85 64     STA $64
$DDC5: E0 02     CPX #$02
$DDC7: B0 0B     BCS L_DDD4
$DDC9: 8A        TXA
$DDCA: 0A        ASL A
$DDCB: 45 0A     EOR $0A
$DDCD: 29 02     AND #$02
$DDCF: F0 13     BEQ L_DDE4
$DDD1: 4C DB DD  JMP L_DDDB
L_DDD4:
$DDD4: 20 4D D4  JSR L_D44D
$DDD7: 29 01     AND #$01
$DDD9: F0 09     BEQ L_DDE4
L_DDDB:
$DDDB: A9 09     LDA #$09
$DDDD: 18        CLC
$DDDE: 65 64     ADC $64
$DDE0: A8        TAY
$DDE1: 4C E6 DD  JMP L_DDE6
L_DDE4:
$DDE4: A4 64     LDY $64
L_DDE6:
$DDE6: B9 86 E4  LDA $E486,Y
$DDE9: 60        RTS
$DDEA: D6 A0     DEC $A0,X
$DDEC: B5 A0     LDA $A0,X
$DDEE: 29 0F     AND #$0F
$DDF0: D0 53     BNE L_DE45
$DDF2: B5 A0     LDA $A0,X
$DDF4: 38        SEC
$DDF5: E9 10     SBC #$10
$DDF7: F0 0E     BEQ L_DE07
$DDF9: C9 10     CMP #$10
$DDFB: D0 05     BNE L_DE02
$DDFD: 09 06     ORA #$06
$DDFF: 4C 04 DE  JMP L_DE04
L_DE02:
$DE02: 09 03     ORA #$03
L_DE04:
$DE04: 95 A0     STA $A0,X
$DE06: 60        RTS
L_DE07:
$DE07: 95 A0     STA $A0,X
$DE09: E0 02     CPX #$02
$DE0B: B0 08     BCS L_DE15
$DE0D: D6 51     DEC $51,X
$DE0F: F0 07     BEQ L_DE18
$DE11: 20 63 E3  JSR L_E363
$DE14: 60        RTS
L_DE15:
$DE15: C6 80     DEC $80
$DE17: 60        RTS
L_DE18:
$DE18: A5 68     LDA $68
$DE1A: C9 80     CMP #$80
$DE1C: D0 27     BNE L_DE45
$DE1E: E0 01     CPX #$01
$DE20: F0 12     BEQ L_DE34
$DE22: A5 52     LDA $52
$DE24: F0 1F     BEQ L_DE45
$DE26: A9 03     LDA #$03
$DE28: 8D 07 01  STA $0107
$DE2B: A9 20     LDA #$20
$DE2D: 8D 05 01  STA $0105
$DE30: 20 46 DE  JSR L_DE46
$DE33: 60        RTS
L_DE34:
$DE34: A5 51     LDA $51
$DE36: F0 0D     BEQ L_DE45
$DE38: A9 01     LDA #$01
$DE3A: 8D 07 01  STA $0107
$DE3D: A9 C0     LDA #$C0
$DE3F: 8D 05 01  STA $0105
$DE42: 20 46 DE  JSR L_DE46
L_DE45:
$DE45: 60        RTS
L_DE46:
$DE46: A9 0D     LDA #$0D
$DE48: 8D 08 01  STA $0108
$DE4B: A9 D8     LDA #$D8
$DE4D: 8D 06 01  STA $0106
$DE50: A9 00     LDA #$00
$DE52: 85 0B     STA $0B
$DE54: 60        RTS
$DE55: F6 A0     INC $A0,X
$DE57: B5 A0     LDA $A0,X
$DE59: 29 0F     AND #$0F
$DE5B: C9 0E     CMP #$0E
$DE5D: D0 04     BNE L_DE63
$DE5F: A9 E0     LDA #$E0
$DE61: 95 A0     STA $A0,X
L_DE63:
$DE63: 60        RTS
$DE64: F6 A0     INC $A0,X
$DE66: B5 A0     LDA $A0,X
$DE68: 29 0F     AND #$0F
$DE6A: C9 0E     CMP #$0E
$DE6C: D0 03     BNE L_DE71
$DE6E: 20 B8 E3  JSR L_E3B8
L_DE71:
$DE71: 60        RTS
L_DE72:
$DE72: A5 84     LDA $84
$DE74: 4A        LSR A
$DE75: 4A        LSR A
$DE76: C5 0A     CMP $0A
$DE78: B0 05     BCS L_DE7F
$DE7A: A9 B0     LDA #$B0
$DE7C: 4C A2 DE  JMP L_DEA2
L_DE7F:
$DE7F: 4A        LSR A
$DE80: C5 0A     CMP $0A
$DE82: 90 0A     BCC L_DE8E
$DE84: 20 4D D4  JSR L_D44D
$DE87: 29 03     AND #$03
$DE89: 09 A0     ORA #$A0
$DE8B: 95 A0     STA $A0,X
$DE8D: 60        RTS
L_DE8E:
$DE8E: A5 A0     LDA $A0
$DE90: F0 09     BEQ L_DE9B
$DE92: 8A        TXA
$DE93: 29 01     AND #$01
$DE95: F0 09     BEQ L_DEA0
$DE97: A5 A1     LDA $A1
$DE99: F0 05     BEQ L_DEA0
L_DE9B:
$DE9B: A9 C0     LDA #$C0
$DE9D: 4C A2 DE  JMP L_DEA2
L_DEA0:
$DEA0: A9 D0     LDA #$D0
L_DEA2:
$DEA2: 20 20 E4  JSR L_E420
$DEA5: 60        RTS
L_DEA6:
$DEA6: A9 00     LDA #$00
$DEA8: 85 5A     STA $5A
L_DEAA:
$DEAA: A6 5A     LDX $5A
$DEAC: 20 B8 DE  JSR L_DEB8
$DEAF: E6 5A     INC $5A
$DEB1: A5 5A     LDA $5A
$DEB3: C9 08     CMP #$08
$DEB5: D0 F3     BNE L_DEAA
$DEB7: 60        RTS
L_DEB8:
$DEB8: B5 A0     LDA $A0,X
$DEBA: 4A        LSR A
$DEBB: 4A        LSR A
$DEBC: 4A        LSR A
$DEBD: 29 FE     AND #$FE
$DEBF: A8        TAY
$DEC0: B9 B8 E4  LDA $E4B8,Y
$DEC3: 85 11     STA $11
$DEC5: B9 B9 E4  LDA $E4B9,Y
$DEC8: 85 12     STA $12
$DECA: 6C 11 00  JMP ($0011)
$DECD: A9 00     LDA #$00
$DECF: 85 6E     STA $6E
$DED1: B5 A0     LDA $A0,X
$DED3: 48        PHA
$DED4: B4 98     LDY $98,X
$DED6: B5 90     LDA $90,X
$DED8: AA        TAX
$DED9: 68        PLA
$DEDA: 20 E2 DE  JSR L_DEE2
$DEDD: A9 20     LDA #$20
$DEDF: 85 6E     STA $6E
$DEE1: 60        RTS
L_DEE2:
$DEE2: 4A        LSR A
$DEE3: 4A        LSR A
$DEE4: 4A        LSR A
$DEE5: 4A        LSR A
$DEE6: 38        SEC
$DEE7: E9 07     SBC #$07
$DEE9: 49 FF     EOR #$FF
$DEEB: 18        CLC
$DEEC: 69 01     ADC #$01
$DEEE: 0A        ASL A
$DEEF: 0A        ASL A
L_DEF0:
$DEF0: 18        CLC
$DEF1: 69 F1     ADC #$F1
$DEF3: 85 53     STA $53
$DEF5: A9 03     LDA #$03
$DEF7: 85 04     STA $04
$DEF9: 20 7B DA  JSR L_DA7B
$DEFC: 60        RTS
$DEFD: A9 00     LDA #$00
$DEFF: 85 6E     STA $6E
$DF01: B5 A8     LDA $A8,X
$DF03: F0 1E     BEQ L_DF23
$DF05: B5 A8     LDA $A8,X
$DF07: 4A        LSR A
$DF08: 4A        LSR A
$DF09: 4A        LSR A
$DF0A: 29 FC     AND #$FC
$DF0C: 38        SEC
$DF0D: E9 10     SBC #$10
$DF0F: 18        CLC
$DF10: 69 B9     ADC #$B9
$DF12: 85 53     STA $53
$DF14: A9 03     LDA #$03
$DF16: 85 04     STA $04
$DF18: B4 98     LDY $98,X
$DF1A: B5 90     LDA $90,X
$DF1C: AA        TAX
$DF1D: 20 7B DA  JSR L_DA7B
$DF20: 4C 2E DF  JMP L_DF2E
L_DF23:
$DF23: B5 98     LDA $98,X
$DF25: A8        TAY
$DF26: B5 90     LDA $90,X
$DF28: AA        TAX
$DF29: A9 00     LDA #$00
$DF2B: 20 F0 DE  JSR L_DEF0
L_DF2E:
$DF2E: A9 20     LDA #$20
$DF30: 85 6E     STA $6E
$DF32: 60        RTS
$DF33: A9 00     LDA #$00
$DF35: 85 6E     STA $6E
$DF37: B4 98     LDY $98,X
$DF39: B5 90     LDA $90,X
$DF3B: AA        TAX
$DF3C: A9 08     LDA #$08
$DF3E: 20 F0 DE  JSR L_DEF0
$DF41: A9 20     LDA #$20
$DF43: 85 6E     STA $6E
$DF45: 60        RTS
$DF46: A9 03     LDA #$03
$DF48: 85 04     STA $04
$DF4A: A9 00     LDA #$00
$DF4C: 85 6E     STA $6E
$DF4E: 20 99 DF  JSR L_DF99
$DF51: 8A        TXA
$DF52: 38        SEC
$DF53: E9 08     SBC #$08
$DF55: AA        TAX
$DF56: 98        TYA
$DF57: 38        SEC
$DF58: E9 08     SBC #$08
$DF5A: A8        TAY
$DF5B: 20 7B DA  JSR L_DA7B
$DF5E: A9 01     LDA #$01
$DF60: 20 99 DF  JSR L_DF99
$DF63: 8A        TXA
$DF64: 18        CLC
$DF65: 69 08     ADC #$08
$DF67: AA        TAX
$DF68: 98        TYA
$DF69: 38        SEC
$DF6A: E9 08     SBC #$08
$DF6C: A8        TAY
$DF6D: 20 7B DA  JSR L_DA7B
$DF70: A9 02     LDA #$02
$DF72: 20 99 DF  JSR L_DF99
$DF75: 8A        TXA
$DF76: 38        SEC
$DF77: E9 08     SBC #$08
$DF79: AA        TAX
$DF7A: 98        TYA
$DF7B: 18        CLC
$DF7C: 69 08     ADC #$08
$DF7E: A8        TAY
$DF7F: 20 7B DA  JSR L_DA7B
$DF82: A9 03     LDA #$03
$DF84: 20 99 DF  JSR L_DF99
$DF87: 8A        TXA
$DF88: 18        CLC
$DF89: 69 08     ADC #$08
$DF8B: AA        TAX
$DF8C: 98        TYA
$DF8D: 18        CLC
$DF8E: 69 08     ADC #$08
$DF90: A8        TAY
$DF91: 20 7B DA  JSR L_DA7B
$DF94: A9 20     LDA #$20
$DF96: 85 6E     STA $6E
$DF98: 60        RTS
L_DF99:
$DF99: A6 5A     LDX $5A
$DF9B: 0A        ASL A
$DF9C: 0A        ASL A
$DF9D: 18        CLC
$DF9E: 69 D1     ADC #$D1
$DFA0: 85 00     STA $00
$DFA2: B5 A0     LDA $A0,X
$DFA4: 29 F0     AND #$F0
$DFA6: 38        SEC
$DFA7: E9 30     SBC #$30
$DFA9: 49 10     EOR #$10
$DFAB: 18        CLC
$DFAC: 65 00     ADC $00
$DFAE: 85 53     STA $53
$DFB0: B4 98     LDY $98,X
$DFB2: B5 90     LDA $90,X
$DFB4: AA        TAX
$DFB5: 60        RTS
$DFB6: E0 02     CPX #$02
$DFB8: 90 23     BCC L_DFDD
$DFBA: B5 A8     LDA $A8,X
$DFBC: 29 04     AND #$04
$DFBE: F0 0D     BEQ L_DFCD
$DFC0: A5 0B     LDA $0B
$DFC2: 4A        LSR A
$DFC3: 4A        LSR A
$DFC4: 4A        LSR A
$DFC5: 29 01     AND #$01
$DFC7: 18        CLC
$DFC8: 69 02     ADC #$02
$DFCA: 4C E9 DF  JMP L_DFE9
L_DFCD:
$DFCD: A5 0B     LDA $0B
$DFCF: 0A        ASL A
$DFD0: 0A        ASL A
$DFD1: 18        CLC
$DFD2: 75 A8     ADC $A8,X
$DFD4: 29 07     AND #$07
$DFD6: A8        TAY
$DFD7: B9 03 E0  LDA $E003,Y
$DFDA: 4C E9 DF  JMP L_DFE9
L_DFDD:
$DFDD: B5 6F     LDA $6F,X
$DFDF: F0 07     BEQ L_DFE8
$DFE1: A5 0B     LDA $0B
$DFE3: 29 08     AND #$08
$DFE5: F0 01     BEQ L_DFE8
$DFE7: 60        RTS
L_DFE8:
$DFE8: 8A        TXA
L_DFE9:
$DFE9: 85 04     STA $04
$DFEB: B5 A0     LDA $A0,X
$DFED: 29 03     AND #$03
$DFEF: 48        PHA
$DFF0: B5 A8     LDA $A8,X
$DFF2: 29 F0     AND #$F0
$DFF4: 18        CLC
$DFF5: 75 B0     ADC $B0,X
$DFF7: 85 53     STA $53
$DFF9: B4 98     LDY $98,X
$DFFB: B5 90     LDA $90,X
$DFFD: AA        TAX
$DFFE: 68        PLA
$DFFF: 20 73 DA  JSR L_DA73
$E002: 60        RTS
$E003: 02        db $02
$E004: 00        BRK
$E005: 00        BRK
$E006: 01 02     ORA ($02,X)
$E008: 01 02     ORA ($02,X)
$E00A: 02        db $02
$E00B: B5 A0     LDA $A0,X
$E00D: 29 0F     AND #$0F
$E00F: 38        SEC
$E010: E9 07     SBC #$07
$E012: 10 05     BPL L_E019
$E014: 49 FF     EOR #$FF
$E016: 18        CLC
$E017: 69 01     ADC #$01
L_E019:
$E019: 0A        ASL A
$E01A: 29 FC     AND #$FC
$E01C: 18        CLC
$E01D: 69 A1     ADC #$A1
$E01F: 85 53     STA $53
$E021: A9 03     LDA #$03
$E023: 85 04     STA $04
$E025: B4 98     LDY $98,X
$E027: B5 90     LDA $90,X
$E029: AA        TAX
$E02A: 20 7B DA  JSR L_DA7B
$E02D: 60        RTS
L_E02E:
$E02E: A9 09     LDA #$09
$E030: 85 5A     STA $5A
L_E032:
$E032: A6 5A     LDX $5A
$E034: 20 3C E0  JSR L_E03C
$E037: C6 5A     DEC $5A
$E039: 10 F7     BPL L_E032
$E03B: 60        RTS
L_E03C:
$E03C: B5 CC     LDA $CC,X
$E03E: 4A        LSR A
$E03F: 4A        LSR A
$E040: 4A        LSR A
$E041: 29 FE     AND #$FE
$E043: A8        TAY
$E044: B9 D8 E4  LDA $E4D8,Y
$E047: 85 11     STA $11
$E049: B9 D9 E4  LDA $E4D9,Y
$E04C: 85 12     STA $12
$E04E: 6C 11 00  JMP ($0011)
$E051: B5 CC     LDA $CC,X
$E053: 29 03     AND #$03
$E055: A8        TAY
$E056: 20 63 E0  JSR L_E063
$E059: B5 D6     LDA $D6,X
$E05B: 29 01     AND #$01
$E05D: F0 03     BEQ L_E062
$E05F: 20 63 E0  JSR L_E063
L_E062:
$E062: 60        RTS
L_E063:
$E063: B9 6C E4  LDA $E46C,Y
$E066: 0A        ASL A
$E067: 18        CLC
$E068: 75 B8     ADC $B8,X
$E06A: 95 B8     STA $B8,X
$E06C: B9 70 E4  LDA $E470,Y
$E06F: 0A        ASL A
$E070: 18        CLC
$E071: 75 C2     ADC $C2,X
$E073: 95 C2     STA $C2,X
$E075: 60        RTS
$E076: D6 CC     DEC $CC,X
$E078: B5 CC     LDA $CC,X
$E07A: 29 0F     AND #$0F
$E07C: D0 0D     BNE L_E08B
$E07E: B5 CC     LDA $CC,X
$E080: 29 F0     AND #$F0
$E082: 38        SEC
$E083: E9 10     SBC #$10
$E085: F0 02     BEQ L_E089
$E087: 09 03     ORA #$03
L_E089:
$E089: 95 CC     STA $CC,X
L_E08B:
$E08B: 60        RTS
L_E08C:
$E08C: B5 CC     LDA $CC,X
$E08E: D0 47     BNE L_E0D7
$E090: E0 02     CPX #$02
$E092: B0 05     BCS L_E099
$E094: A9 01     LDA #$01
$E096: 8D 0F 03  STA $030F
L_E099:
$E099: B5 A0     LDA $A0,X
$E09B: 29 03     AND #$03
$E09D: A8        TAY
$E09E: 09 40     ORA #$40
$E0A0: 95 CC     STA $CC,X
$E0A2: B9 6C E4  LDA $E46C,Y
$E0A5: 0A        ASL A
$E0A6: 0A        ASL A
$E0A7: 0A        ASL A
$E0A8: 18        CLC
$E0A9: 75 90     ADC $90,X
$E0AB: 95 B8     STA $B8,X
$E0AD: B9 70 E4  LDA $E470,Y
$E0B0: 0A        ASL A
$E0B1: 0A        ASL A
$E0B2: 0A        ASL A
$E0B3: 18        CLC
$E0B4: 75 98     ADC $98,X
$E0B6: 95 C2     STA $C2,X
$E0B8: A9 00     LDA #$00
$E0BA: 95 D6     STA $D6,X
$E0BC: B5 A8     LDA $A8,X
$E0BE: 29 F0     AND #$F0
$E0C0: F0 15     BEQ L_E0D7
$E0C2: C9 C0     CMP #$C0
$E0C4: F0 08     BEQ L_E0CE
$E0C6: C9 60     CMP #$60
$E0C8: F0 09     BEQ L_E0D3
$E0CA: 29 80     AND #$80
$E0CC: D0 09     BNE L_E0D7
L_E0CE:
$E0CE: A9 01     LDA #$01
$E0D0: 95 D6     STA $D6,X
$E0D2: 60        RTS
L_E0D3:
$E0D3: A9 03     LDA #$03
$E0D5: 95 D6     STA $D6,X
L_E0D7:
$E0D7: 60        RTS
L_E0D8:
$E0D8: A9 09     LDA #$09
$E0DA: 85 5A     STA $5A
L_E0DC:
$E0DC: A6 5A     LDX $5A
$E0DE: 20 E6 E0  JSR L_E0E6
$E0E1: C6 5A     DEC $5A
$E0E3: 10 F7     BPL L_E0DC
$E0E5: 60        RTS
L_E0E6:
$E0E6: B5 CC     LDA $CC,X
$E0E8: 4A        LSR A
$E0E9: 4A        LSR A
$E0EA: 4A        LSR A
$E0EB: 29 FE     AND #$FE
$E0ED: A8        TAY
$E0EE: B9 E2 E4  LDA $E4E2,Y
$E0F1: 85 11     STA $11
$E0F3: B9 E3 E4  LDA $E4E3,Y
$E0F6: 85 12     STA $12
$E0F8: 6C 11 00  JMP ($0011)
$E0FB: B5 CC     LDA $CC,X
$E0FD: 29 03     AND #$03
$E0FF: 48        PHA
$E100: B4 C2     LDY $C2,X
$E102: B5 B8     LDA $B8,X
$E104: AA        TAX
$E105: A9 02     LDA #$02
$E107: 85 04     STA $04
$E109: A9 B1     LDA #$B1
$E10B: 85 53     STA $53
$E10D: 68        PLA
$E10E: 20 64 DA  JSR L_DA64
$E111: 60        RTS
$E112: B5 CC     LDA $CC,X
$E114: 48        PHA
$E115: B4 C2     LDY $C2,X
$E117: B5 B8     LDA $B8,X
$E119: AA        TAX
$E11A: 68        PLA
$E11B: 18        CLC
$E11C: 69 40     ADC #$40
$E11E: 20 E2 DE  JSR L_DEE2
$E121: 60        RTS
L_E122:
$E122: A9 01     LDA #$01
$E124: 85 5A     STA $5A
L_E126:
$E126: A6 5A     LDX $5A
$E128: B5 A0     LDA $A0,X
$E12A: 10 31     BPL L_E15D
$E12C: C9 E0     CMP #$E0
$E12E: B0 2D     BCS L_E15D
$E130: B5 08     LDA $08,X
$E132: 29 03     AND #$03
$E134: F0 27     BEQ L_E15D
$E136: B5 A8     LDA $A8,X
$E138: 29 C0     AND #$C0
$E13A: C9 40     CMP #$40
$E13C: D0 1C     BNE L_E15A
$E13E: B5 CC     LDA $CC,X
$E140: F0 18     BEQ L_E15A
$E142: B5 D4     LDA $D4,X
$E144: D0 17     BNE L_E15D
$E146: B5 CC     LDA $CC,X
$E148: 95 D4     STA $D4,X
$E14A: B5 B8     LDA $B8,X
$E14C: 95 C0     STA $C0,X
$E14E: B5 C2     LDA $C2,X
$E150: 95 CA     STA $CA,X
$E152: B5 D6     LDA $D6,X
$E154: 95 DE     STA $DE,X
$E156: A9 00     LDA #$00
$E158: 95 CC     STA $CC,X
L_E15A:
$E15A: 20 8C E0  JSR L_E08C
L_E15D:
$E15D: C6 5A     DEC $5A
$E15F: 10 C5     BPL L_E126
$E161: 60        RTS
L_E162:
$E162: AD 00 01  LDA $0100
$E165: D0 19     BNE L_E180
$E167: A2 07     LDX #$07
L_E169:
$E169: B5 A0     LDA $A0,X
$E16B: 10 0E     BPL L_E17B
$E16D: C9 E0     CMP #$E0
$E16F: B0 0A     BCS L_E17B
$E171: 20 4D D4  JSR L_D44D
$E174: 29 1F     AND #$1F
$E176: D0 03     BNE L_E17B
$E178: 20 8C E0  JSR L_E08C
L_E17B:
$E17B: CA        DEX
$E17C: E0 01     CPX #$01
$E17E: D0 E9     BNE L_E169
L_E180:
$E180: 60        RTS
L_E181:
$E181: A9 07     LDA #$07
$E183: 85 5A     STA $5A
L_E185:
$E185: A6 5A     LDX $5A
$E187: B5 A0     LDA $A0,X
$E189: 10 63     BPL L_E1EE
$E18B: C9 E0     CMP #$E0
$E18D: B0 5F     BCS L_E1EE
$E18F: B5 98     LDA $98,X
$E191: 38        SEC
$E192: E9 08     SBC #$08
$E194: A8        TAY
$E195: B5 90     LDA $90,X
$E197: 38        SEC
$E198: E9 08     SBC #$08
$E19A: AA        TAX
$E19B: 20 06 D7  JSR L_D706
$E19E: A6 5A     LDX $5A
$E1A0: A5 11     LDA $11
$E1A2: 95 E0     STA $E0,X
$E1A4: A5 12     LDA $12
$E1A6: 29 03     AND #$03
$E1A8: 95 E8     STA $E8,X
$E1AA: A0 21     LDY #$21
$E1AC: E0 02     CPX #$02
$E1AE: B0 19     BCS L_E1C9
$E1B0: B1 11     LDA ($11),Y
$E1B2: C9 21     CMP #$21
$E1B4: D0 0B     BNE L_E1C1
$E1B6: A9 80     LDA #$80
$E1B8: 1D 03 01  ORA $0103,X
$E1BB: 9D 03 01  STA $0103,X
$E1BE: 4C C9 E1  JMP L_E1C9
L_E1C1:
$E1C1: BD 03 01  LDA $0103,X
$E1C4: 29 7F     AND #$7F
$E1C6: 9D 03 01  STA $0103,X
L_E1C9:
$E1C9: 20 F3 E1  JSR L_E1F3
$E1CC: B5 90     LDA $90,X
$E1CE: 29 07     AND #$07
$E1D0: D0 0B     BNE L_E1DD
$E1D2: B5 E8     LDA $E8,X
$E1D4: 09 80     ORA #$80
$E1D6: 95 E8     STA $E8,X
$E1D8: A0 20     LDY #$20
$E1DA: 20 F3 E1  JSR L_E1F3
L_E1DD:
$E1DD: B5 98     LDA $98,X
$E1DF: 29 07     AND #$07
$E1E1: D0 0B     BNE L_E1EE
$E1E3: B5 E8     LDA $E8,X
$E1E5: 09 40     ORA #$40
$E1E7: 95 E8     STA $E8,X
$E1E9: A0 01     LDY #$01
$E1EB: 20 F3 E1  JSR L_E1F3
L_E1EE:
$E1EE: C6 5A     DEC $5A
$E1F0: 10 93     BPL L_E185
$E1F2: 60        RTS
L_E1F3:
$E1F3: B1 11     LDA ($11),Y
$E1F5: 09 80     ORA #$80
$E1F7: 91 11     STA ($11),Y
$E1F9: 60        RTS
L_E1FA:
$E1FA: A9 07     LDA #$07
$E1FC: 85 5A     STA $5A
L_E1FE:
$E1FE: A6 5A     LDX $5A
$E200: B5 A0     LDA $A0,X
$E202: 10 2B     BPL L_E22F
$E204: C9 E0     CMP #$E0
$E206: B0 27     BCS L_E22F
$E208: B5 E0     LDA $E0,X
$E20A: 85 11     STA $11
$E20C: B5 E8     LDA $E8,X
$E20E: 29 03     AND #$03
$E210: 09 04     ORA #$04
$E212: 85 12     STA $12
$E214: A0 21     LDY #$21
$E216: 20 34 E2  JSR L_E234
$E219: B5 E8     LDA $E8,X
$E21B: 29 80     AND #$80
$E21D: F0 05     BEQ L_E224
$E21F: A0 20     LDY #$20
$E221: 20 34 E2  JSR L_E234
L_E224:
$E224: B5 E8     LDA $E8,X
$E226: 29 40     AND #$40
$E228: F0 05     BEQ L_E22F
$E22A: A0 01     LDY #$01
$E22C: 20 34 E2  JSR L_E234
L_E22F:
$E22F: C6 5A     DEC $5A
$E231: 10 CB     BPL L_E1FE
$E233: 60        RTS
L_E234:
$E234: B1 11     LDA ($11),Y
$E236: 29 7F     AND #$7F
$E238: 91 11     STA ($11),Y
$E23A: 60        RTS
L_E23B:
$E23B: A5 86     LDA $86
$E23D: F0 3C     BEQ L_E27B
$E23F: A5 62     LDA $62
$E241: F0 16     BEQ L_E259
$E243: C6 62     DEC $62
$E245: D0 07     BNE L_E24E
$E247: A9 00     LDA #$00
$E249: 85 86     STA $86
$E24B: 4C 7B E2  JMP L_E27B
L_E24E:
$E24E: A9 02     LDA #$02
$E250: 85 04     STA $04
$E252: A9 3B     LDA #$3B
$E254: 85 53     STA $53
$E256: 4C 6C E2  JMP L_E26C
L_E259:
$E259: A5 0B     LDA $0B
$E25B: 29 08     AND #$08
$E25D: F0 1C     BEQ L_E27B
$E25F: A9 02     LDA #$02
$E261: 85 04     STA $04
$E263: A5 88     LDA $88
$E265: 0A        ASL A
$E266: 0A        ASL A
$E267: 18        CLC
$E268: 69 81     ADC #$81
$E26A: 85 53     STA $53
L_E26C:
$E26C: A6 86     LDX $86
$E26E: A4 87     LDY $87
$E270: A9 00     LDA #$00
$E272: 85 6E     STA $6E
$E274: 20 7B DA  JSR L_DA7B
$E277: A9 20     LDA #$20
$E279: 85 6E     STA $6E
L_E27B:
$E27B: 60        RTS
L_E27C:
$E27C: A9 01     LDA #$01
$E27E: 85 5A     STA $5A
L_E280:
$E280: A6 5A     LDX $5A
$E282: B5 89     LDA $89,X
$E284: F0 1E     BEQ L_E2A4
$E286: A5 0B     LDA $0B
$E288: 29 3F     AND #$3F
$E28A: D0 02     BNE L_E28E
$E28C: D6 89     DEC $89,X
L_E28E:
$E28E: A9 02     LDA #$02
$E290: 85 04     STA $04
$E292: B4 98     LDY $98,X
$E294: B5 90     LDA $90,X
$E296: AA        TAX
$E297: A5 0B     LDA $0B
$E299: 29 02     AND #$02
$E29B: 0A        ASL A
$E29C: 18        CLC
$E29D: 69 29     ADC #$29
$E29F: 85 53     STA $53
$E2A1: 20 7B DA  JSR L_DA7B
L_E2A4:
$E2A4: C6 5A     DEC $5A
$E2A6: 10 D8     BPL L_E280
$E2A8: 60        RTS
L_E2A9:
$E2A9: A5 45     LDA $45
$E2AB: F0 25     BEQ L_E2D2
$E2AD: A5 0B     LDA $0B
$E2AF: 29 0F     AND #$0F
$E2B1: D0 1F     BNE L_E2D2
$E2B3: A5 0B     LDA $0B
$E2B5: 29 3F     AND #$3F
$E2B7: D0 04     BNE L_E2BD
$E2B9: C6 45     DEC $45
$E2BB: F0 12     BEQ L_E2CF
L_E2BD:
$E2BD: A5 45     LDA $45
$E2BF: C9 04     CMP #$04
$E2C1: B0 0F     BCS L_E2D2
$E2C3: A5 0B     LDA $0B
$E2C5: 29 10     AND #$10
$E2C7: F0 06     BEQ L_E2CF
$E2C9: 20 9E CB  JSR L_CB9E
$E2CC: 4C D2 E2  JMP L_E2D2
L_E2CF:
$E2CF: 20 F5 CA  JSR L_CAF5
L_E2D2:
$E2D2: A5 68     LDA $68
$E2D4: F0 2F     BEQ L_E305
$E2D6: 30 2D     BMI L_E305
$E2D8: A9 03     LDA #$03
$E2DA: 85 04     STA $04
$E2DC: C6 68     DEC $68
$E2DE: A5 68     LDA $68
$E2E0: 4A        LSR A
$E2E1: 4A        LSR A
$E2E2: 38        SEC
L_E2E3:
$E2E3: E9 05     SBC #$05
$E2E5: 10 05     BPL L_E2EC
$E2E7: 49 FF     EOR #$FF
$E2E9: 18        CLC
$E2EA: 69 01     ADC #$01
L_E2EC:
$E2EC: 38        SEC
$E2ED: E9 05     SBC #$05
$E2EF: 10 05     BPL L_E2F6
$E2F1: 49 FF     EOR #$FF
$E2F3: 18        CLC
$E2F4: 69 01     ADC #$01
L_E2F6:
$E2F6: 0A        ASL A
$E2F7: A8        TAY
$E2F8: B9 06 E3  LDA $E306,Y
$E2FB: 85 11     STA $11
$E2FD: B9 07 E3  LDA $E307,Y
$E300: 85 12     STA $12
$E302: 6C 11 00  JMP ($0011)
L_E305:
$E305: 60        RTS
$E306: F0 DB     BEQ L_E2E3
$E308: 12        db $12
$E309: E3        db $E3
$E30A: 17        db $17
$E30B: E3        db $E3
$E30C: 1C        db $1C
$E30D: E3        db $E3
$E30E: 2E E3 36  ROL OAMADDR_36E3
$E311: E3        db $E3
$E312: A9 F1     LDA #$F1
$E314: 4C 1E E3  JMP L_E31E
$E317: A9 F5     LDA #$F5
$E319: 4C 1E E3  JMP L_E31E
$E31C: A9 F9     LDA #$F9
L_E31E:
$E31E: A2 78     LDX #$78
$E320: A0 D8     LDY #$D8
L_E322:
$E322: 85 53     STA $53
$E324: 20 7B DA  JSR L_DA7B
$E327: 60        RTS
L_E328:
$E328: 18        CLC
$E329: 65 69     ADC $69
$E32B: 4C 22 E3  JMP L_E322
$E32E: A9 00     LDA #$00
$E330: 85 69     STA $69
$E332: 20 3E E3  JSR L_E33E
$E335: 60        RTS
$E336: A9 10     LDA #$10
$E338: 85 69     STA $69
$E33A: 20 3E E3  JSR L_E33E
$E33D: 60        RTS
L_E33E:
$E33E: A2 70     LDX #$70
$E340: A0 D0     LDY #$D0
$E342: A9 D1     LDA #$D1
$E344: 20 28 E3  JSR L_E328
$E347: A2 80     LDX #$80
$E349: A0 D0     LDY #$D0
$E34B: A9 D5     LDA #$D5
$E34D: 20 28 E3  JSR L_E328
$E350: A2 70     LDX #$70
$E352: A0 E0     LDY #$E0
$E354: A9 D9     LDA #$D9
$E356: 20 28 E3  JSR L_E328
$E359: A2 80     LDX #$80
$E35B: A0 E0     LDY #$E0
$E35D: A9 DD     LDA #$DD
$E35F: 20 28 E3  JSR L_E328
$E362: 60        RTS
L_E363:
$E363: A9 00     LDA #$00
$E365: 95 A8     STA $A8,X
$E367: E0 02     CPX #$02
$E369: B0 11     BCS L_E37C
$E36B: BD 7A E4  LDA $E47A,X
$E36E: 95 90     STA $90,X
$E370: BD 7C E4  LDA $E47C,X
$E373: 95 98     STA $98,X
$E375: A9 00     LDA #$00
$E377: 95 6F     STA $6F,X
$E379: 4C A9 E3  JMP L_E3A9
L_E37C:
$E37C: E6 6A     INC $6A
$E37E: A4 6A     LDY $6A
$E380: C0 03     CPY #$03
$E382: D0 05     BNE L_E389
$E384: A9 00     LDA #$00
$E386: 85 6A     STA $6A
$E388: A8        TAY
L_E389:
$E389: B9 74 E4  LDA $E474,Y
$E38C: 95 90     STA $90,X
$E38E: B9 77 E4  LDA $E477,Y
$E391: 95 98     STA $98,X
$E393: A5 7F     LDA $7F
$E395: C9 03     CMP #$03
$E397: F0 08     BEQ L_E3A1
$E399: C9 0A     CMP #$0A
$E39B: F0 04     BEQ L_E3A1
$E39D: C9 11     CMP #$11
$E39F: D0 08     BNE L_E3A9
L_E3A1:
$E3A1: A9 04     LDA #$04
$E3A3: 95 A8     STA $A8,X
$E3A5: A9 00     LDA #$00
$E3A7: 85 86     STA $86
L_E3A9:
$E3A9: A9 F0     LDA #$F0
$E3AB: 95 A0     STA $A0,X
$E3AD: B4 98     LDY $98,X
$E3AF: B5 90     LDA $90,X
$E3B1: AA        TAX
$E3B2: A9 0F     LDA #$0F
$E3B4: 20 0B D8  JSR L_D80B
$E3B7: 60        RTS
L_E3B8:
$E3B8: BD 7E E4  LDA $E47E,X
$E3BB: 95 A0     STA $A0,X
$E3BD: E0 02     CPX #$02
$E3BF: B0 0A     BCS L_E3CB
$E3C1: A9 03     LDA #$03
$E3C3: 95 89     STA $89,X
$E3C5: BD 01 01  LDA $0101,X
$E3C8: 4C FA E3  JMP L_E3FA
L_E3CB:
$E3CB: A4 8F     LDY $8F
$E3CD: B9 8B 00  LDA $008B,Y
$E3D0: D0 05     BNE L_E3D7
$E3D2: E6 8F     INC $8F
$E3D4: 4C CB E3  JMP L_E3CB
L_E3D7:
$E3D7: 38        SEC
$E3D8: E9 01     SBC #$01
$E3DA: 99 8B 00  STA $008B,Y
$E3DD: A5 46     LDA $46
$E3DF: F0 05     BEQ L_E3E6
$E3E1: A9 23     LDA #$23
$E3E3: 4C E8 E3  JMP L_E3E8
L_E3E6:
$E3E6: A5 85     LDA $85
L_E3E8:
$E3E8: 38        SEC
$E3E9: E9 01     SBC #$01
$E3EB: 0A        ASL A
$E3EC: 0A        ASL A
$E3ED: 18        CLC
$E3EE: 65 8F     ADC $8F
$E3F0: A8        TAY
$E3F1: B9 EC E4  LDA $E4EC,Y
$E3F4: C9 E0     CMP #$E0
$E3F6: D0 02     BNE L_E3FA
$E3F8: 09 03     ORA #$03
L_E3FA:
$E3FA: 15 A8     ORA $A8,X
$E3FC: C9 E7     CMP #$E7
$E3FE: D0 02     BNE L_E402
$E400: A9 E4     LDA #$E4
L_E402:
$E402: 95 A8     STA $A8,X
$E404: A9 00     LDA #$00
$E406: 95 B0     STA $B0,X
$E408: 60        RTS
L_E409:
$E409: A2 09     LDX #$09
$E40B: A9 00     LDA #$00
L_E40D:
$E40D: 95 CC     STA $CC,X
$E40F: CA        DEX
$E410: 10 FB     BPL L_E40D
$E412: 60        RTS
L_E413:
$E413: A9 00     LDA #$00
$E415: A2 07     LDX #$07
L_E417:
$E417: 95 A0     STA $A0,X
$E419: 9D 03 01  STA $0103,X
$E41C: CA        DEX
$E41D: 10 F8     BPL L_E417
$E41F: 60        RTS
L_E420:
$E420: 85 00     STA $00
$E422: B5 A0     LDA $A0,X
$E424: 29 0F     AND #$0F
$E426: 05 00     ORA $00
$E428: 95 A0     STA $A0,X
$E42A: 60        RTS
L_E42B:
$E42B: A5 46     LDA $46
$E42D: F0 05     BEQ L_E434
$E42F: A9 23     LDA #$23
$E431: 4C 36 E4  JMP L_E436
L_E434:
$E434: A5 85     LDA $85
L_E436:
$E436: 38        SEC
$E437: E9 01     SBC #$01
$E439: 0A        ASL A
$E43A: 0A        ASL A
$E43B: A8        TAY
$E43C: B9 78 E5  LDA $E578,Y
$E43F: 85 8B     STA $8B
$E441: B9 79 E5  LDA $E579,Y
$E444: 85 8C     STA $8C
$E446: B9 7A E5  LDA $E57A,Y
$E449: 85 8D     STA $8D
$E44B: B9 7B E5  LDA $E57B,Y
$E44E: 85 8E     STA $8E
$E450: 60        RTS
L_E451:
$E451: 0A        ASL A
$E452: 90 03     BCC L_E457
$E454: A9 03     LDA #$03
$E456: 60        RTS
L_E457:
$E457: 0A        ASL A
$E458: 90 03     BCC L_E45D
$E45A: A9 01     LDA #$01
$E45C: 60        RTS
L_E45D:
$E45D: 0A        ASL A
$E45E: 90 03     BCC L_E463
$E460: A9 02     LDA #$02
$E462: 60        RTS
L_E463:
$E463: 0A        ASL A
$E464: 90 03     BCC L_E469
$E466: A9 00     LDA #$00
$E468: 60        RTS
L_E469:
$E469: A9 FF     LDA #$FF
$E46B: 60        RTS
$E46C: 00        BRK
$E46D: FF        db $FF
$E46E: 00        BRK
$E46F: 01 FF     ORA ($FF,X)
$E471: 00        BRK
$E472: 01 00     ORA ($00,X)
$E474: 18        CLC
L_E475:
$E475: 78        SEI
$E476: D8        CLD
$E477: 18        CLC
$E478: 18        CLC
$E479: 18        CLC
$E47A: 58        CLI
$E47B: 98        TYA
$E47C: D8        CLD
$E47D: D8        CLD
$E47E: A0 A0     LDY #$A0
$E480: A2 A2     LDX #$A2
$E482: A2 A2     LDX #$A2
$E484: A2 A2     LDX #$A2
$E486: A0 A0     LDY #$A0
$E488: A0 A1     LDY #$A1
$E48A: A0 A3     LDY #$A3
$E48C: A2 A2     LDX #$A2
$E48E: A2 A1     LDX #$A1
$E490: A0 A3     LDY #$A3
$E492: A1 A0     LDA ($A0,X)
$E494: A3        db $A3
L_E495:
$E495: A1 A2     LDA ($A2,X)
$E497: A3        db $A3
$E498: F0 DB     BEQ L_E475
$E49A: EA        NOP
$E49B: DD EA DD  CMP $DDEA,X
$E49E: EA        NOP
$E49F: DD EA DD  CMP $DDEA,X
$E4A2: EA        NOP
$E4A3: DD EA DD  CMP $DDEA,X
$E4A6: EA        NOP
$E4A7: DD 52 DC  CMP $DC52,X
$E4AA: 48        PHA
$E4AB: DD 7C DC  CMP $DC7C,X
$E4AE: 94 DD     STY $DD,X
$E4B0: 89        db $89
$E4B1: DD 7E DD  CMP $DD7E,X
$E4B4: 64        db $64
$E4B5: DE 55 DE  DEC $DE55,X
$E4B8: F0 DB     BEQ L_E495
$E4BA: FD DE 33  SBC PPUADDR_33DE,X
$E4BD: DF        db $DF
$E4BE: 46 DF     LSR $DF
$E4C0: 46 DF     LSR $DF
$E4C2: CD DE CD  CMP $CDDE
$E4C5: DE CD DE  DEC $DECD,X
$E4C8: B6 DF     LDX $DF,Y
$E4CA: B6 DF     LDX $DF,Y
$E4CC: B6 DF     LDX $DF,Y
$E4CE: B6 DF     LDX $DF,Y
$E4D0: B6 DF     LDX $DF,Y
$E4D2: B6 DF     LDX $DF,Y
$E4D4: 0B        db $0B
$E4D5: E0 0B     CPX #$0B
$E4D7: E0 F0     CPX #$F0
$E4D9: DB        db $DB
$E4DA: 76 E0     ROR $E0,X
$E4DC: 76 E0     ROR $E0,X
$E4DE: 76 E0     ROR $E0,X
$E4E0: 51 E0     EOR ($E0),Y
$E4E2: F0 DB     BEQ L_E4BF
$E4E4: 12        db $12
$E4E5: E1 12     SBC ($12,X)
$E4E7: E1 12     SBC ($12,X)
$E4E9: E1 FB     SBC ($FB,X)
$E4EB: E0 80     CPX #$80
$E4ED: A0 C0     LDY #$C0
$E4EF: E0 E0     CPX #$E0
$E4F1: A0 C0     LDY #$C0
$E4F3: 80        db $80
$E4F4: 80        db $80
$E4F5: A0 C0     LDY #$C0
$E4F7: E0 C0     CPX #$C0
$E4F9: A0 80     LDY #$80
$E4FB: E0 C0     CPX #$C0
$E4FD: E0 80     CPX #$80
$E4FF: A0 C0     LDY #$C0
$E501: A0 80     LDY #$80
$E503: E0 80     CPX #$80
$E505: A0 C0     LDY #$C0
$E507: 80        db $80
$E508: C0 E0     CPY #$E0
$E50A: A0 80     LDY #$80
$E50C: 80        db $80
$E50D: A0 C0     LDY #$C0
$E50F: E0 80     CPX #$80
$E511: A0 C0     LDY #$C0
$E513: E0 A0     CPX #$A0
$E515: E0 C0     CPX #$C0
$E517: A0 C0     LDY #$C0
$E519: A0 80     LDY #$80
$E51B: E0 C0     CPX #$C0
$E51D: A0 80     LDY #$80
$E51F: E0 C0     CPX #$C0
$E521: A0 80     LDY #$80
$E523: E0 80     CPX #$80
$E525: C0 A0     CPY #$A0
$E527: E0 80     CPX #$80
$E529: C0 A0     CPY #$A0
$E52B: E0 E0     CPX #$E0
$E52D: A0 C0     LDY #$C0
$E52F: 80        db $80
$E530: E0 80     CPX #$80
$E532: C0 A0     CPY #$A0
$E534: A0 E0     LDY #$E0
$E536: 80        db $80
$E537: C0 A0     CPY #$A0
$E539: 80        db $80
$E53A: C0 E0     CPY #$E0
$E53C: C0 A0     CPY #$A0
$E53E: 80        db $80
$E53F: E0 A0     CPX #$A0
$E541: 80        db $80
$E542: C0 E0     CPY #$E0
$E544: E0 80     CPX #$80
$E546: C0 A0     CPY #$A0
$E548: C0 E0     CPY #$E0
$E54A: A0 80     LDY #$80
$E54C: C0 A0     CPY #$A0
$E54E: 80        db $80
$E54F: E0 A0     CPX #$A0
$E551: E0 80     CPX #$80
$E553: C0 C0     CPY #$C0
$E555: E0 A0     CPX #$A0
$E557: 80        db $80
$E558: A0 E0     LDY #$E0
$E55A: 80        db $80
$E55B: C0 C0     CPY #$C0
$E55D: A0 80     LDY #$80
$E55F: E0 80     CPX #$80
$E561: A0 C0     LDY #$C0
$E563: E0 C0     CPX #$C0
$E565: A0 E0     LDY #$E0
$E567: C0 E0     CPY #$E0
$E569: 80        db $80
$E56A: C0 A0     CPY #$A0
$E56C: A0 E0     LDY #$E0
$E56E: C0 A0     CPY #$A0
$E570: C0 A0     CPY #$A0
$E572: 80        db $80
$E573: E0 C0     CPX #$C0
$E575: A0 80     LDY #$80
$E577: E0 12     CPX #$12
$E579: 02        db $02
$E57A: 00        BRK
$E57B: 00        BRK
$E57C: 02        db $02
$E57D: 04        db $04
$E57E: 00        BRK
$E57F: 0E 0E 04  ASL $040E
$E582: 00        BRK
$E583: 02        db $02
$E584: 0A        ASL A
$E585: 05 02     ORA $02
$E587: 03        db $03
$E588: 05 02     ORA $02
$E58A: 08        PHP
$E58B: 05 07     ORA $07
$E58D: 02        db $02
$E58E: 09 02     ORA #$02
$E590: 03        db $03
$E591: 04        db $04
$E592: 06 07     ASL $07
$E594: 07        db $07
$E595: 02        db $02
$E596: 04        db $04
$E597: 07        db $07
$E598: 06 04     ASL $04
$E59A: 07        db $07
$E59B: 03        db $03
$E59C: 0C        db $0C
$E59D: 02        db $02
$E59E: 04        db $04
$E59F: 02        db $02
$E5A0: 05 06     ORA $06
$E5A2: 04        db $04
$E5A3: 05 08     ORA $08
$E5A5: 06 00     ASL $00
$E5A7: 06 08     ASL $08
$E5A9: 08        PHP
$E5AA: 00        BRK
$E5AB: 04        db $04
$E5AC: 0A        ASL A
$E5AD: 04        db $04
$E5AE: 00        BRK
$E5AF: 06 02     ASL $02
$E5B1: 00        BRK
$E5B2: 0A        ASL A
$E5B3: 08        PHP
$E5B4: 10 00     BPL L_E5B6
L_E5B6:
$E5B6: 02        db $02
$E5B7: 02        db $02
$E5B8: 02        db $02
$E5B9: 02        db $02
$E5BA: 08        PHP
$E5BB: 08        PHP
$E5BC: 04        db $04
$E5BD: 02        db $02
$E5BE: 06 08     ASL $08
$E5C0: 04        db $04
$E5C1: 08        PHP
$E5C2: 04        db $04
$E5C3: 04        db $04
$E5C4: 08        PHP
$E5C5: 02        db $02
$E5C6: 02        db $02
$E5C7: 08        PHP
$E5C8: 08        PHP
$E5C9: 02        db $02
$E5CA: 06 04     ASL $04
$E5CC: 08        PHP
$E5CD: 06 02     ASL $02
$E5CF: 04        db $04
$E5D0: 06 00     ASL $00
$E5D2: 04        db $04
$E5D3: 0A        ASL A
$E5D4: 04        db $04
$E5D5: 02        db $02
$E5D6: 04        db $04
$E5D7: 0A        ASL A
$E5D8: 02        db $02
$E5D9: 08        PHP
$E5DA: 00        BRK
$E5DB: 0A        ASL A
$E5DC: 06 06     ASL $06
$E5DE: 04        db $04
$E5DF: 04        db $04
$E5E0: 02        db $02
$E5E1: 08        PHP
$E5E2: 08        PHP
$E5E3: 02        db $02
$E5E4: 02        db $02
$E5E5: 01 0F     ORA ($0F,X)
$E5E7: 02        db $02
$E5E8: 0A        ASL A
$E5E9: 04        db $04
$E5EA: 00        BRK
$E5EB: 06 04     ASL $04
$E5ED: 08        PHP
$E5EE: 04        db $04
$E5EF: 04        db $04
$E5F0: 03        db $03
$E5F1: 08        PHP
$E5F2: 06 03     ASL $03
$E5F4: 08        PHP
$E5F5: 06 02     ASL $02
$E5F7: 04        db $04
$E5F8: 04        db $04
$E5F9: 08        PHP
$E5FA: 04        db $04
$E5FB: 04        db $04
$E5FC: 04        db $04
$E5FD: 0A        ASL A
$E5FE: 00        BRK
$E5FF: 06 04     ASL $04
$E601: 06 00     ASL $00
$E603: 0A        ASL A
L_E604:
$E604: A9 09     LDA #$09
$E606: 85 5A     STA $5A
L_E608:
$E608: A6 5A     LDX $5A
$E60A: B5 CC     LDA $CC,X
$E60C: 29 F0     AND #$F0
$E60E: C9 40     CMP #$40
$E610: D0 79     BNE L_E68B
$E612: B5 D6     LDA $D6,X
$E614: D0 07     BNE L_E61D
$E616: 8A        TXA
$E617: 45 0B     EOR $0B
$E619: 29 01     AND #$01
$E61B: F0 6E     BEQ L_E68B
L_E61D:
$E61D: B5 CC     LDA $CC,X
$E61F: 29 03     AND #$03
$E621: A8        TAY
$E622: B9 49 EA  LDA $EA49,Y
$E625: 10 05     BPL L_E62C
$E627: 49 FF     EOR #$FF
$E629: 18        CLC
$E62A: 69 01     ADC #$01
L_E62C:
$E62C: 85 54     STA $54
$E62E: 0A        ASL A
$E62F: 0A        ASL A
$E630: 85 64     STA $64
$E632: B9 4D EA  LDA $EA4D,Y
$E635: 10 05     BPL L_E63C
$E637: 49 FF     EOR #$FF
$E639: 18        CLC
$E63A: 69 01     ADC #$01
L_E63C:
$E63C: 85 55     STA $55
$E63E: 0A        ASL A
$E63F: 0A        ASL A
$E640: 85 65     STA $65
$E642: B4 C2     LDY $C2,X
$E644: B5 B8     LDA $B8,X
$E646: AA        TAX
$E647: 20 93 E6  JSR L_E693
$E64A: F0 13     BEQ L_E65F
$E64C: A6 5A     LDX $5A
$E64E: B5 C2     LDA $C2,X
$E650: 18        CLC
$E651: 65 64     ADC $64
$E653: 85 48     STA $48
$E655: B5 B8     LDA $B8,X
$E657: 18        CLC
$E658: 65 65     ADC $65
$E65A: 85 47     STA $47
$E65C: 20 9A E6  JSR L_E69A
L_E65F:
$E65F: A6 5A     LDX $5A
$E661: B5 C2     LDA $C2,X
$E663: 38        SEC
$E664: E5 54     SBC $54
$E666: A8        TAY
$E667: B5 B8     LDA $B8,X
$E669: 38        SEC
$E66A: E5 55     SBC $55
$E66C: AA        TAX
$E66D: 20 93 E6  JSR L_E693
$E670: F0 19     BEQ L_E68B
$E672: A6 5A     LDX $5A
$E674: B5 C2     LDA $C2,X
$E676: 38        SEC
$E677: E5 64     SBC $64
$E679: 38        SEC
$E67A: E5 54     SBC $54
$E67C: 85 48     STA $48
$E67E: B5 B8     LDA $B8,X
$E680: 38        SEC
$E681: E5 65     SBC $65
$E683: 38        SEC
$E684: E5 55     SBC $55
$E686: 85 47     STA $47
$E688: 20 9A E6  JSR L_E69A
L_E68B:
$E68B: C6 5A     DEC $5A
$E68D: 30 03     BMI L_E692
$E68F: 4C 08 E6  JMP L_E608
L_E692:
$E692: 60        RTS
L_E693:
$E693: 86 47     STX $47
$E695: 84 48     STY $48
$E697: 20 06 D7  JSR L_D706
L_E69A:
$E69A: 20 25 D7  JSR L_D725
$E69D: 20 3C D7  JSR L_D73C
$E6A0: F0 67     BEQ L_E709
$E6A2: B1 11     LDA ($11),Y
$E6A4: 29 FC     AND #$FC
$E6A6: C9 C8     CMP #$C8
$E6A8: D0 1C     BNE L_E6C6
$E6AA: A5 68     LDA $68
$E6AC: F0 18     BEQ L_E6C6
$E6AE: A9 27     LDA #$27
$E6B0: 85 68     STA $68
$E6B2: A9 01     LDA #$01
$E6B4: 8D 0B 03  STA $030B
$E6B7: 8D 07 03  STA $0307
$E6BA: 20 08 CC  JSR L_CC08
$E6BD: A6 5A     LDX $5A
$E6BF: A9 33     LDA #$33
$E6C1: 95 CC     STA $CC,X
$E6C3: 4C 09 E7  JMP L_E709
L_E6C6:
$E6C6: B1 11     LDA ($11),Y
$E6C8: C9 12     CMP #$12
$E6CA: B0 3D     BCS L_E709
$E6CC: A6 5A     LDX $5A
$E6CE: A9 33     LDA #$33
$E6D0: 95 CC     STA $CC,X
$E6D2: B1 11     LDA ($11),Y
$E6D4: C9 11     CMP #$11
$E6D6: F0 28     BEQ L_E700
$E6D8: B5 D6     LDA $D6,X
$E6DA: 29 02     AND #$02
$E6DC: F0 0D     BEQ L_E6EB
$E6DE: A9 00     LDA #$00
$E6E0: 20 84 D7  JSR L_D784
$E6E3: A9 01     LDA #$01
$E6E5: 8D 0C 03  STA $030C
$E6E8: 4C 09 E7  JMP L_E709
L_E6EB:
$E6EB: B1 11     LDA ($11),Y
$E6ED: C9 10     CMP #$10
$E6EF: F0 0F     BEQ L_E700
$E6F1: E0 02     CPX #$02
$E6F3: B0 05     BCS L_E6FA
$E6F5: A9 01     LDA #$01
$E6F7: 8D 0C 03  STA $030C
L_E6FA:
$E6FA: 20 43 D7  JSR L_D743
$E6FD: A9 01     LDA #$01
$E6FF: 60        RTS
L_E700:
$E700: E0 02     CPX #$02
$E702: B0 05     BCS L_E709
$E704: A9 01     LDA #$01
$E706: 8D 0D 03  STA $030D
L_E709:
$E709: A9 00     LDA #$00
$E70B: 60        RTS
L_E70C:
$E70C: A9 01     LDA #$01
$E70E: 85 5A     STA $5A
L_E710:
$E710: A6 5A     LDX $5A
$E712: B5 A0     LDA $A0,X
$E714: 10 04     BPL L_E71A
$E716: C9 E0     CMP #$E0
$E718: 90 03     BCC L_E71D
L_E71A:
$E71A: 4C 7A E7  JMP L_E77A
L_E71D:
$E71D: A9 07     LDA #$07
$E71F: 85 5B     STA $5B
L_E721:
$E721: A4 5B     LDY $5B
$E723: B9 CC 00  LDA $00CC,Y
$E726: 29 F0     AND #$F0
$E728: C9 40     CMP #$40
$E72A: D0 46     BNE L_E772
$E72C: B9 B8 00  LDA $00B8,Y
$E72F: 38        SEC
$E730: F5 90     SBC $90,X
$E732: 10 05     BPL L_E739
$E734: 49 FF     EOR #$FF
$E736: 18        CLC
$E737: 69 01     ADC #$01
L_E739:
$E739: C9 0A     CMP #$0A
$E73B: B0 35     BCS L_E772
$E73D: B9 C2 00  LDA $00C2,Y
$E740: 38        SEC
$E741: F5 98     SBC $98,X
$E743: 10 05     BPL L_E74A
$E745: 49 FF     EOR #$FF
$E747: 18        CLC
$E748: 69 01     ADC #$01
L_E74A:
$E74A: C9 0A     CMP #$0A
$E74C: B0 24     BCS L_E772
$E74E: A9 33     LDA #$33
$E750: 99 CC 00  STA $00CC,Y
$E753: B5 89     LDA $89,X
$E755: F0 08     BEQ L_E75F
$E757: A9 00     LDA #$00
$E759: 99 CC 00  STA $00CC,Y
$E75C: 4C 72 E7  JMP L_E772
L_E75F:
$E75F: A9 73     LDA #$73
$E761: 95 A0     STA $A0,X
$E763: A9 01     LDA #$01
$E765: 8D 07 03  STA $0307
$E768: A9 00     LDA #$00
$E76A: 9D 01 01  STA $0101,X
$E76D: 95 A8     STA $A8,X
$E76F: 4C 7A E7  JMP L_E77A
L_E772:
$E772: C6 5B     DEC $5B
$E774: A5 5B     LDA $5B
$E776: C9 01     CMP #$01
$E778: D0 A7     BNE L_E721
L_E77A:
$E77A: C6 5A     DEC $5A
$E77C: 10 92     BPL L_E710
$E77E: A9 07     LDA #$07
$E780: 85 5A     STA $5A
L_E782:
$E782: A6 5A     LDX $5A
$E784: B5 A0     LDA $A0,X
$E786: 10 04     BPL L_E78C
$E788: C9 E0     CMP #$E0
$E78A: 90 03     BCC L_E78F
L_E78C:
$E78C: 4C 34 E8  JMP L_E834
L_E78F:
$E78F: A9 09     LDA #$09
$E791: 85 5B     STA $5B
L_E793:
$E793: A5 5B     LDA $5B
$E795: 29 06     AND #$06
$E797: F0 03     BEQ L_E79C
$E799: 4C 2D E8  JMP L_E82D
L_E79C:
$E79C: A4 5B     LDY $5B
$E79E: B9 CC 00  LDA $00CC,Y
$E7A1: 29 F0     AND #$F0
$E7A3: C9 40     CMP #$40
$E7A5: F0 03     BEQ L_E7AA
$E7A7: 4C 2D E8  JMP L_E82D
L_E7AA:
$E7AA: B9 B8 00  LDA $00B8,Y
$E7AD: 38        SEC
$E7AE: F5 90     SBC $90,X
$E7B0: 10 05     BPL L_E7B7
$E7B2: 49 FF     EOR #$FF
$E7B4: 18        CLC
$E7B5: 69 01     ADC #$01
L_E7B7:
$E7B7: C9 0A     CMP #$0A
$E7B9: B0 72     BCS L_E82D
$E7BB: B9 C2 00  LDA $00C2,Y
$E7BE: 38        SEC
$E7BF: F5 98     SBC $98,X
$E7C1: 10 05     BPL L_E7C8
$E7C3: 49 FF     EOR #$FF
$E7C5: 18        CLC
$E7C6: 69 01     ADC #$01
L_E7C8:
$E7C8: C9 0A     CMP #$0A
$E7CA: B0 61     BCS L_E82D
$E7CC: A9 33     LDA #$33
$E7CE: 99 CC 00  STA $00CC,Y
$E7D1: B5 A8     LDA $A8,X
$E7D3: 29 04     AND #$04
$E7D5: F0 0B     BEQ L_E7E2
$E7D7: 20 BE E8  JSR L_E8BE
$E7DA: B5 A8     LDA $A8,X
$E7DC: C9 E4     CMP #$E4
$E7DE: D0 02     BNE L_E7E2
$E7E0: D6 A8     DEC $A8,X
L_E7E2:
$E7E2: B5 A8     LDA $A8,X
$E7E4: 29 03     AND #$03
$E7E6: F0 0A     BEQ L_E7F2
$E7E8: D6 A8     DEC $A8,X
$E7EA: A9 01     LDA #$01
$E7EC: 8D 0E 03  STA $030E
$E7EF: 4C 2D E8  JMP L_E82D
L_E7F2:
$E7F2: A9 73     LDA #$73
$E7F4: 95 A0     STA $A0,X
$E7F6: A9 01     LDA #$01
$E7F8: 8D 0A 03  STA $030A
$E7FB: B5 A8     LDA $A8,X
$E7FD: 4A        LSR A
$E7FE: 4A        LSR A
$E7FF: 4A        LSR A
$E800: 4A        LSR A
$E801: 4A        LSR A
$E802: 38        SEC
$E803: E9 04     SBC #$04
$E805: AA        TAX
$E806: A5 5B     LDA $5B
$E808: 29 01     AND #$01
$E80A: 85 47     STA $47
$E80C: D0 05     BNE L_E813
$E80E: F6 73     INC $73,X
$E810: 4C 15 E8  JMP L_E815
L_E813:
$E813: F6 77     INC $77,X
L_E815:
$E815: A5 46     LDA $46
$E817: C9 02     CMP #$02
$E819: F0 19     BEQ L_E834
$E81B: BD BA E8  LDA $E8BA,X
$E81E: 20 E1 D9  JSR L_D9E1
$E821: A5 47     LDA $47
$E823: AA        TAX
$E824: 20 BE D9  JSR L_D9BE
$E827: 20 38 D1  JSR L_D138
$E82A: 4C 34 E8  JMP L_E834
L_E82D:
$E82D: C6 5B     DEC $5B
$E82F: 30 03     BMI L_E834
$E831: 4C 93 E7  JMP L_E793
L_E834:
$E834: C6 5A     DEC $5A
$E836: A5 5A     LDA $5A
$E838: C9 01     CMP #$01
$E83A: F0 03     BEQ L_E83F
$E83C: 4C 82 E7  JMP L_E782
L_E83F:
$E83F: A9 01     LDA #$01
$E841: 85 5A     STA $5A
L_E843:
$E843: A6 5A     LDX $5A
$E845: B5 A0     LDA $A0,X
$E847: 10 04     BPL L_E84D
$E849: C9 E0     CMP #$E0
$E84B: 90 03     BCC L_E850
L_E84D:
$E84D: 4C B5 E8  JMP L_E8B5
L_E850:
$E850: A9 09     LDA #$09
$E852: 85 5B     STA $5B
L_E854:
$E854: A5 5B     LDA $5B
$E856: 29 06     AND #$06
$E858: D0 57     BNE L_E8B1
$E85A: A4 5B     LDY $5B
$E85C: B9 CC 00  LDA $00CC,Y
$E85F: 29 F0     AND #$F0
$E861: C9 40     CMP #$40
$E863: D0 4C     BNE L_E8B1
$E865: A5 5A     LDA $5A
$E867: 45 5B     EOR $5B
$E869: 29 01     AND #$01
$E86B: F0 44     BEQ L_E8B1
$E86D: B9 B8 00  LDA $00B8,Y
$E870: 38        SEC
$E871: F5 90     SBC $90,X
$E873: 10 05     BPL L_E87A
$E875: 49 FF     EOR #$FF
$E877: 18        CLC
$E878: 69 01     ADC #$01
L_E87A:
$E87A: C9 0A     CMP #$0A
$E87C: B0 33     BCS L_E8B1
$E87E: B9 C2 00  LDA $00C2,Y
$E881: 38        SEC
$E882: F5 98     SBC $98,X
$E884: 10 05     BPL L_E88B
$E886: 49 FF     EOR #$FF
$E888: 18        CLC
$E889: 69 01     ADC #$01
L_E88B:
$E88B: C9 0A     CMP #$0A
$E88D: B0 22     BCS L_E8B1
$E88F: A9 33     LDA #$33
$E891: 99 CC 00  STA $00CC,Y
$E894: B5 89     LDA $89,X
$E896: F0 08     BEQ L_E8A0
$E898: A9 00     LDA #$00
$E89A: 99 CC 00  STA $00CC,Y
$E89D: 4C B1 E8  JMP L_E8B1
L_E8A0:
$E8A0: B5 6F     LDA $6F,X
$E8A2: D0 0D     BNE L_E8B1
$E8A4: A5 46     LDA $46
$E8A6: C9 02     CMP #$02
$E8A8: F0 07     BEQ L_E8B1
$E8AA: A9 C8     LDA #$C8
$E8AC: 95 6F     STA $6F,X
$E8AE: 4C B5 E8  JMP L_E8B5
L_E8B1:
$E8B1: C6 5B     DEC $5B
$E8B3: 10 9F     BPL L_E854
L_E8B5:
$E8B5: C6 5A     DEC $5A
$E8B7: 10 8A     BPL L_E843
$E8B9: 60        RTS
$E8BA: 10 20     BPL L_E8DC
$E8BC: 30 40     BMI L_E8FE
L_E8BE:
$E8BE: A9 01     LDA #$01
$E8C0: 8D 09 03  STA $0309
L_E8C3:
$E8C3: 20 4D D4  JSR L_D44D
$E8C6: 29 03     AND #$03
$E8C8: 20 02 E9  JSR L_E902
$E8CB: 85 86     STA $86
$E8CD: 20 4D D4  JSR L_D44D
$E8D0: 29 03     AND #$03
$E8D2: 20 02 E9  JSR L_E902
$E8D5: 85 87     STA $87
$E8D7: A9 FF     LDA #$FF
$E8D9: 85 88     STA $88
$E8DB: A9 00     LDA #$00
$E8DD: 85 62     STA $62
$E8DF: 20 72 E9  JSR L_E972
$E8E2: A5 62     LDA $62
$E8E4: D0 DD     BNE L_E8C3
$E8E6: 20 4D D4  JSR L_D44D
$E8E9: 29 07     AND #$07
$E8EB: A8        TAY
$E8EC: B9 FA E8  LDA $E8FA,Y
$E8EF: 85 88     STA $88
$E8F1: A9 00     LDA #$00
$E8F3: 85 62     STA $62
$E8F5: A6 5A     LDX $5A
$E8F7: A4 5B     LDY $5B
$E8F9: 60        RTS
$E8FA: 00        BRK
$E8FB: 01 02     ORA ($02,X)
$E8FD: 03        db $03
L_E8FE:
$E8FE: 04        db $04
$E8FF: 05 04     ORA $04
$E901: 03        db $03
L_E902:
$E902: 85 00     STA $00
$E904: 0A        ASL A
$E905: 18        CLC
$E906: 65 00     ADC $00
$E908: 0A        ASL A
$E909: 18        CLC
$E90A: 69 06     ADC #$06
$E90C: 0A        ASL A
$E90D: 0A        ASL A
$E90E: 0A        ASL A
$E90F: 60        RTS
L_E910:
$E910: A9 09     LDA #$09
$E912: 85 5A     STA $5A
L_E914:
$E914: A5 5A     LDA $5A
$E916: 29 06     AND #$06
$E918: D0 53     BNE L_E96D
$E91A: A6 5A     LDX $5A
$E91C: B5 CC     LDA $CC,X
$E91E: 29 F0     AND #$F0
$E920: C9 40     CMP #$40
$E922: D0 49     BNE L_E96D
$E924: A9 09     LDA #$09
$E926: 85 5B     STA $5B
L_E928:
$E928: A5 5B     LDA $5B
$E92A: A8        TAY
$E92B: 29 07     AND #$07
$E92D: 85 00     STA $00
$E92F: A5 5A     LDA $5A
$E931: 29 07     AND #$07
$E933: C5 00     CMP $00
$E935: F0 32     BEQ L_E969
$E937: B9 CC 00  LDA $00CC,Y
$E93A: 29 F0     AND #$F0
$E93C: C9 40     CMP #$40
$E93E: D0 29     BNE L_E969
$E940: B9 B8 00  LDA $00B8,Y
$E943: 38        SEC
$E944: F5 B8     SBC $B8,X
$E946: 10 05     BPL L_E94D
$E948: 49 FF     EOR #$FF
$E94A: 18        CLC
$E94B: 69 01     ADC #$01
L_E94D:
$E94D: C9 06     CMP #$06
$E94F: B0 18     BCS L_E969
$E951: B9 C2 00  LDA $00C2,Y
$E954: 38        SEC
$E955: F5 C2     SBC $C2,X
$E957: 10 05     BPL L_E95E
$E959: 49 FF     EOR #$FF
$E95B: 18        CLC
$E95C: 69 01     ADC #$01
L_E95E:
$E95E: C9 06     CMP #$06
$E960: B0 07     BCS L_E969
$E962: A9 00     LDA #$00
$E964: 95 CC     STA $CC,X
$E966: 99 CC 00  STA $00CC,Y
L_E969:
$E969: C6 5B     DEC $5B
$E96B: 10 BB     BPL L_E928
L_E96D:
$E96D: C6 5A     DEC $5A
$E96F: 10 A3     BPL L_E914
$E971: 60        RTS
L_E972:
$E972: A5 86     LDA $86
$E974: F0 6B     BEQ L_E9E1
$E976: A5 62     LDA $62
$E978: D0 67     BNE L_E9E1
$E97A: A9 01     LDA #$01
$E97C: 85 49     STA $49
L_E97E:
$E97E: A6 49     LDX $49
$E980: B5 A0     LDA $A0,X
$E982: 10 59     BPL L_E9DD
$E984: C9 E0     CMP #$E0
$E986: B0 55     BCS L_E9DD
$E988: B5 90     LDA $90,X
$E98A: 38        SEC
$E98B: E5 86     SBC $86
$E98D: 10 05     BPL L_E994
$E98F: 49 FF     EOR #$FF
$E991: 18        CLC
$E992: 69 01     ADC #$01
L_E994:
$E994: C9 0C     CMP #$0C
$E996: B0 45     BCS L_E9DD
$E998: B5 98     LDA $98,X
$E99A: 38        SEC
$E99B: E5 87     SBC $87
$E99D: 10 05     BPL L_E9A4
$E99F: 49 FF     EOR #$FF
$E9A1: 18        CLC
$E9A2: 69 01     ADC #$01
L_E9A4:
$E9A4: C9 0C     CMP #$0C
$E9A6: B0 35     BCS L_E9DD
$E9A8: A9 32     LDA #$32
$E9AA: 85 62     STA $62
$E9AC: A5 88     LDA $88
$E9AE: 30 31     BMI L_E9E1
$E9B0: A5 46     LDA $46
$E9B2: C9 02     CMP #$02
$E9B4: F0 14     BEQ L_E9CA
$E9B6: A9 50     LDA #$50
$E9B8: 20 E1 D9  JSR L_D9E1
$E9BB: A6 49     LDX $49
$E9BD: 20 BE D9  JSR L_D9BE
$E9C0: 20 38 D1  JSR L_D138
$E9C3: A6 49     LDX $49
$E9C5: A9 01     LDA #$01
$E9C7: 8D 06 03  STA $0306
L_E9CA:
$E9CA: A5 88     LDA $88
$E9CC: 0A        ASL A
L_E9CD:
$E9CD: A8        TAY
$E9CE: B9 E2 E9  LDA $E9E2,Y
$E9D1: 85 11     STA $11
$E9D3: B9 E3 E9  LDA $E9E3,Y
$E9D6: 85 12     STA $12
$E9D8: 68        PLA
$E9D9: 68        PLA
$E9DA: 6C 11 00  JMP ($0011)
L_E9DD:
$E9DD: C6 49     DEC $49
$E9DF: 10 9D     BPL L_E97E
L_E9E1:
$E9E1: 60        RTS
$E9E2: F0 E9     BEQ L_E9CD
$E9E4: F5 E9     SBC $E9,X
$E9E6: FB        db $FB
$E9E7: E9 07     SBC #$07
$E9E9: EA        NOP
$E9EA: 17        db $17
$E9EB: EA        NOP
$E9EC: 3E EA 48  ROL $48EA,X
$E9EF: EA        NOP
$E9F0: A9 0A     LDA #$0A
$E9F2: 95 89     STA $89,X
$E9F4: 60        RTS
$E9F5: A9 0A     LDA #$0A
$E9F7: 8D 00 01  STA $0100
$E9FA: 60        RTS
$E9FB: A5 68     LDA $68
$E9FD: 10 07     BPL L_EA06
$E9FF: 20 9E CB  JSR L_CB9E
$EA02: A9 14     LDA #$14
$EA04: 85 45     STA $45
L_EA06:
$EA06: 60        RTS
$EA07: BD 01 01  LDA $0101,X
$EA0A: C9 60     CMP #$60
$EA0C: F0 08     BEQ L_EA16
$EA0E: 18        CLC
$EA0F: 69 20     ADC #$20
$EA11: 9D 01 01  STA $0101,X
$EA14: 95 A8     STA $A8,X
L_EA16:
$EA16: 60        RTS
$EA17: A9 07     LDA #$07
$EA19: 85 5A     STA $5A
$EA1B: A9 01     LDA #$01
$EA1D: 8D 0A 03  STA $030A
L_EA20:
$EA20: A4 5A     LDY $5A
$EA22: B9 A0 00  LDA $00A0,Y
$EA25: 10 0E     BPL L_EA35
$EA27: C9 E0     CMP #$E0
$EA29: B0 0A     BCS L_EA35
$EA2B: A9 73     LDA #$73
$EA2D: 99 A0 00  STA $00A0,Y
$EA30: A9 00     LDA #$00
$EA32: 99 A8 00  STA $00A8,Y
L_EA35:
$EA35: C6 5A     DEC $5A
$EA37: A5 5A     LDA $5A
$EA39: C9 01     CMP #$01
$EA3B: D0 E3     BNE L_EA20
$EA3D: 60        RTS
$EA3E: F6 51     INC $51,X
$EA40: A9 01     LDA #$01
$EA42: 8D 04 03  STA $0304
$EA45: 8D 05 03  STA $0305
$EA48: 60        RTS
$EA49: 00        BRK
$EA4A: FF        db $FF
$EA4B: 00        BRK
$EA4C: 01 FF     ORA ($FF,X)
$EA4E: 00        BRK
$EA4F: 01 00     ORA ($00,X)
InitAudio:
L_EA51:
$EA51: A9 0F     LDA #$0F
$EA53: 8D 15 40  STA APU_STATUS
$EA56: A9 C0     LDA #$C0
$EA58: 8D 17 40  STA JOY2_APU_FRAME
$EA5B: A9 1C     LDA #$1C
$EA5D: 85 F0     STA $F0
$EA5F: A9 03     LDA #$03
$EA61: 85 F1     STA $F1
$EA63: A2 00     LDX #$00
$EA65: A0 00     LDY #$00
L_EA67:
$EA67: 98        TYA
$EA68: 91 F0     STA ($F0),Y
$EA6A: 9D 00 03  STA $0300,X
$EA6D: 18        CLC
$EA6E: A5 F0     LDA $F0
$EA70: 69 08     ADC #$08
$EA72: 85 F0     STA $F0
$EA74: 90 02     BCC L_EA78
$EA76: E6 F1     INC $F1
L_EA78:
$EA78: E8        INX
$EA79: E0 1C     CPX #$1C
$EA7B: D0 EA     BNE L_EA67
$EA7D: 60        RTS
L_EA7E:
$EA7E: A5 6D     LDA $6D
$EA80: D0 06     BNE L_EA88
$EA82: A9 1C     LDA #$1C
$EA84: 85 F5     STA $F5
$EA86: 10 04     BPL L_EA8C
L_EA88:
$EA88: A9 01     LDA #$01
$EA8A: 85 F5     STA $F5
L_EA8C:
$EA8C: A9 00     LDA #$00
$EA8E: A2 03     LDX #$03
L_EA90:
$EA90: 95 F9     STA $F9,X
$EA92: CA        DEX
$EA93: 10 FB     BPL L_EA90
$EA95: A9 00     LDA #$00
$EA97: 85 F4     STA $F4
$EA99: A9 1C     LDA #$1C
$EA9B: 85 F0     STA $F0
$EA9D: A9 03     LDA #$03
$EA9F: 85 F1     STA $F1
L_EAA1:
$EAA1: A6 F4     LDX $F4
$EAA3: BD 00 03  LDA $0300,X
$EAA6: F0 3B     BEQ L_EAE3
$EAA8: A0 00     LDY #$00
$EAAA: B1 F0     LDA ($F0),Y
$EAAC: F0 35     BEQ L_EAE3
$EAAE: C9 05     CMP #$05
$EAB0: 90 0B     BCC L_EABD
$EAB2: 38        SEC
$EAB3: E9 05     SBC #$05
$EAB5: AA        TAX
$EAB6: A9 01     LDA #$01
$EAB8: 95 F9     STA $F9,X
$EABA: 4C E3 EA  JMP L_EAE3
L_EABD:
$EABD: AA        TAX
$EABE: CA        DEX
$EABF: B5 F9     LDA $F9,X
$EAC1: D0 20     BNE L_EAE3
$EAC3: A9 01     LDA #$01
$EAC5: 95 F9     STA $F9,X
$EAC7: 8A        TXA
$EAC8: A8        TAY
$EAC9: 18        CLC
$EACA: 69 05     ADC #$05
$EACC: A0 00     LDY #$00
$EACE: 91 F0     STA ($F0),Y
$EAD0: 8A        TXA
$EAD1: 0A        ASL A
$EAD2: 0A        ASL A
$EAD3: AA        TAX
$EAD4: A9 04     LDA #$04
$EAD6: 85 FD     STA $FD
L_EAD8:
$EAD8: C8        INY
$EAD9: B1 F0     LDA ($F0),Y
$EADB: 9D 00 40  STA PULSE1_CTRL,X
$EADE: E8        INX
$EADF: C6 FD     DEC $FD
$EAE1: D0 F5     BNE L_EAD8
L_EAE3:
$EAE3: 18        CLC
$EAE4: A5 F0     LDA $F0
$EAE6: 69 08     ADC #$08
$EAE8: 85 F0     STA $F0
$EAEA: 90 02     BCC L_EAEE
$EAEC: E6 F1     INC $F1
L_EAEE:
$EAEE: E6 F4     INC $F4
$EAF0: A5 F4     LDA $F4
$EAF2: C5 F5     CMP $F5
$EAF4: 90 AB     BCC L_EAA1
$EAF6: A2 00     LDX #$00
L_EAF8:
$EAF8: 86 FD     STX $FD
$EAFA: B5 F9     LDA $F9,X
$EAFC: D0 0C     BNE L_EB0A
$EAFE: 8A        TXA
$EAFF: 0A        ASL A
$EB00: 0A        ASL A
$EB01: AA        TAX
$EB02: 0A        ASL A
$EB03: 29 10     AND #$10
$EB05: 49 10     EOR #$10
$EB07: 9D 00 40  STA PULSE1_CTRL,X
L_EB0A:
$EB0A: A6 FD     LDX $FD
$EB0C: E8        INX
$EB0D: E0 04     CPX #$04
$EB0F: 90 E7     BCC L_EAF8
$EB11: A0 00     LDY #$00
$EB13: 84 F4     STY $F4
$EB15: A9 1C     LDA #$1C
$EB17: 85 F0     STA $F0
$EB19: A9 03     LDA #$03
$EB1B: 85 F1     STA $F1
L_EB1D:
$EB1D: A6 F4     LDX $F4
$EB1F: BD 00 03  LDA $0300,X
$EB22: F0 0A     BEQ L_EB2E
$EB24: C9 01     CMP #$01
$EB26: D0 1A     BNE L_EB42
$EB28: FE 00 03  INC $0300,X
$EB2B: 4C 4F EB  JMP L_EB4F
L_EB2E:
$EB2E: 18        CLC
$EB2F: A5 F0     LDA $F0
$EB31: 69 08     ADC #$08
$EB33: 85 F0     STA $F0
$EB35: 90 02     BCC L_EB39
$EB37: E6 F1     INC $F1
L_EB39:
$EB39: E6 F4     INC $F4
$EB3B: A5 F4     LDA $F4
$EB3D: C5 F5     CMP $F5
$EB3F: 90 DC     BCC L_EB1D
$EB41: 60        RTS
L_EB42:
$EB42: A0 07     LDY #$07
$EB44: B1 F0     LDA ($F0),Y
$EB46: 38        SEC
$EB47: E9 01     SBC #$01
$EB49: 91 F0     STA ($F0),Y
$EB4B: F0 38     BEQ L_EB85
$EB4D: D0 DF     BNE L_EB2E
L_EB4F:
$EB4F: A9 00     LDA #$00
$EB51: A0 05     LDY #$05
$EB53: 91 F0     STA ($F0),Y
$EB55: 20 AF EC  JSR L_ECAF
$EB58: 20 BE EC  JSR L_ECBE
$EB5B: A0 00     LDY #$00
$EB5D: 91 F0     STA ($F0),Y
$EB5F: 20 BE EC  JSR L_ECBE
$EB62: A0 01     LDY #$01
$EB64: 91 F0     STA ($F0),Y
$EB66: 20 BE EC  JSR L_ECBE
$EB69: A0 02     LDY #$02
$EB6B: 91 F0     STA ($F0),Y
$EB6D: 20 BE EC  JSR L_ECBE
$EB70: A0 04     LDY #$04
$EB72: 91 F0     STA ($F0),Y
$EB74: A0 00     LDY #$00
$EB76: B1 F0     LDA ($F0),Y
$EB78: C9 04     CMP #$04
$EB7A: D0 0C     BNE L_EB88
$EB7C: 20 BE EC  JSR L_ECBE
$EB7F: A0 03     LDY #$03
$EB81: 91 F0     STA ($F0),Y
$EB83: 10 03     BPL L_EB88
L_EB85:
$EB85: 20 AF EC  JSR L_ECAF
L_EB88:
$EB88: 20 BE EC  JSR L_ECBE
$EB8B: C9 E8     CMP #$E8
$EB8D: B0 52     BCS L_EBE1
$EB8F: C9 60     CMP #$60
$EB91: F0 44     BEQ L_EBD7
$EB93: 90 09     BCC L_EB9E
$EB95: E9 60     SBC #$60
$EB97: A0 06     LDY #$06
$EB99: 91 F0     STA ($F0),Y
$EB9B: 4C 88 EB  JMP L_EB88
L_EB9E:
$EB9E: 48        PHA
$EB9F: 29 F8     AND #$F8
$EBA1: 4A        LSR A
$EBA2: 4A        LSR A
$EBA3: AA        TAX
$EBA4: BD E6 EC  LDA $ECE6,X
$EBA7: 85 FD     STA $FD
$EBA9: BD E7 EC  LDA $ECE7,X
$EBAC: 85 FE     STA $FE
$EBAE: 68        PLA
$EBAF: 29 07     AND #$07
$EBB1: F0 08     BEQ L_EBBB
$EBB3: AA        TAX
L_EBB4:
$EBB4: 46 FD     LSR $FD
$EBB6: 66 FE     ROR $FE
$EBB8: CA        DEX
$EBB9: D0 F9     BNE L_EBB4
L_EBBB:
$EBBB: A0 04     LDY #$04
$EBBD: B1 F0     LDA ($F0),Y
$EBBF: 29 F8     AND #$F8
$EBC1: 05 FD     ORA $FD
$EBC3: 91 F0     STA ($F0),Y
$EBC5: A5 FE     LDA $FE
$EBC7: 88        DEY
$EBC8: 91 F0     STA ($F0),Y
$EBCA: A0 00     LDY #$00
$EBCC: B1 F0     LDA ($F0),Y
$EBCE: C9 05     CMP #$05
$EBD0: 90 05     BCC L_EBD7
$EBD2: 38        SEC
$EBD3: E9 04     SBC #$04
$EBD5: 91 F0     STA ($F0),Y
L_EBD7:
$EBD7: A0 06     LDY #$06
$EBD9: B1 F0     LDA ($F0),Y
$EBDB: C8        INY
$EBDC: 91 F0     STA ($F0),Y
$EBDE: 4C 2E EB  JMP L_EB2E
L_EBE1:
$EBE1: E9 E8     SBC #$E8
$EBE3: 20 D0 EC  JSR L_ECD0
$EBE6: 0A        ASL A
$EBE7: EC 21 EC  CPX $EC21
$EBEA: 33        db $33
$EBEB: EC 45 EC  CPX $EC45
$EBEE: 57        db $57
$EBEF: EC 61 EC  CPX $EC61
$EBF2: 6B        db $6B
$EBF3: EC 75 EC  CPX $EC75
$EBF6: 81 EC     STA ($EC,X)
$EBF8: 85 EC     STA $EC
$EBFA: 88        DEY
$EBFB: EC 99 EC  CPX $EC99
$EBFE: 99 EC 99  STA L_99EC,Y
$EC01: EC 99 EC  CPX $EC99
$EC04: 99 EC 99  STA L_99EC,Y
$EC07: EC A5 EC  CPX $ECA5
$EC0A: A6 F4     LDX $F4
$EC0C: A9 00     LDA #$00
$EC0E: 9D 00 03  STA $0300,X
$EC11: A0 00     LDY #$00
$EC13: 91 F0     STA ($F0),Y
$EC15: A0 05     LDY #$05
$EC17: B1 F0     LDA ($F0),Y
$EC19: 38        SEC
$EC1A: E9 01     SBC #$01
$EC1C: 91 F0     STA ($F0),Y
$EC1E: 4C 2E EB  JMP L_EB2E
$EC21: 20 BE EC  JSR L_ECBE
$EC24: 85 FD     STA $FD
$EC26: A0 01     LDY #$01
$EC28: B1 F0     LDA ($F0),Y
$EC2A: 29 3F     AND #$3F
$EC2C: 05 FD     ORA $FD
$EC2E: 91 F0     STA ($F0),Y
$EC30: 4C 88 EB  JMP L_EB88
$EC33: 20 BE EC  JSR L_ECBE
$EC36: 85 FD     STA $FD
$EC38: A0 01     LDY #$01
$EC3A: B1 F0     LDA ($F0),Y
$EC3C: 29 C0     AND #$C0
$EC3E: 05 FD     ORA $FD
$EC40: 91 F0     STA ($F0),Y
$EC42: 4C 88 EB  JMP L_EB88
$EC45: 20 BE EC  JSR L_ECBE
$EC48: 85 FD     STA $FD
$EC4A: A0 01     LDY #$01
$EC4C: B1 F0     LDA ($F0),Y
$EC4E: 29 F0     AND #$F0
$EC50: 05 FD     ORA $FD
$EC52: 91 F0     STA ($F0),Y
$EC54: 4C 88 EB  JMP L_EB88
$EC57: 20 BE EC  JSR L_ECBE
$EC5A: A0 02     LDY #$02
$EC5C: 91 F0     STA ($F0),Y
$EC5E: 4C 88 EB  JMP L_EB88
$EC61: 20 BE EC  JSR L_ECBE
$EC64: A0 04     LDY #$04
$EC66: 91 F0     STA ($F0),Y
$EC68: 4C 88 EB  JMP L_EB88
$EC6B: 20 BE EC  JSR L_ECBE
$EC6E: A0 01     LDY #$01
$EC70: 91 F0     STA ($F0),Y
$EC72: 4C 88 EB  JMP L_EB88
$EC75: A9 00     LDA #$00
$EC77: A2 02     LDX #$02
L_EC79:
$EC79: 95 F6     STA $F6,X
$EC7B: CA        DEX
$EC7C: 10 FB     BPL L_EC79
$EC7E: 4C 88 EB  JMP L_EB88
$EC81: A2 00     LDX #$00
$EC83: F0 05     BEQ L_EC8A
$EC85: A2 01     LDX #$01
$EC87: 2C A2 02  BIT $02A2
L_EC8A:
$EC8A: 20 BE EC  JSR L_ECBE
$EC8D: F6 F6     INC $F6,X
$EC8F: D5 F6     CMP $F6,X
$EC91: D0 12     BNE L_ECA5
$EC93: A9 00     LDA #$00
$EC95: 95 F6     STA $F6,X
$EC97: F0 00     BEQ L_EC99
L_EC99:
$EC99: A0 05     LDY #$05
$EC9B: B1 F0     LDA ($F0),Y
$EC9D: 18        CLC
$EC9E: 69 01     ADC #$01
$ECA0: 91 F0     STA ($F0),Y
$ECA2: 4C 88 EB  JMP L_EB88
L_ECA5:
$ECA5: 20 BE EC  JSR L_ECBE
$ECA8: A0 05     LDY #$05
$ECAA: 91 F0     STA ($F0),Y
$ECAC: 4C 88 EB  JMP L_EB88
L_ECAF:
$ECAF: A5 F4     LDA $F4
$ECB1: 0A        ASL A
$ECB2: AA        TAX
$ECB3: BD FE EC  LDA $ECFE,X
$ECB6: 85 F2     STA $F2
$ECB8: BD FF EC  LDA $ECFF,X
$ECBB: 85 F3     STA $F3
$ECBD: 60        RTS
L_ECBE:
$ECBE: A5 F4     LDA $F4
$ECC0: A0 05     LDY #$05
$ECC2: B1 F0     LDA ($F0),Y
$ECC4: A8        TAY
$ECC5: B1 F2     LDA ($F2),Y
$ECC7: 48        PHA
$ECC8: C8        INY
$ECC9: 98        TYA
$ECCA: A0 05     LDY #$05
$ECCC: 91 F0     STA ($F0),Y
$ECCE: 68        PLA
$ECCF: 60        RTS
L_ECD0:
$ECD0: 0A        ASL A
$ECD1: A8        TAY
$ECD2: C8        INY
$ECD3: 68        PLA
$ECD4: 85 FD     STA $FD
$ECD6: 68        PLA
$ECD7: 85 FE     STA $FE
$ECD9: B1 FD     LDA ($FD),Y
$ECDB: AA        TAX
$ECDC: C8        INY
$ECDD: B1 FD     LDA ($FD),Y
$ECDF: 85 FE     STA $FE
$ECE1: 86 FD     STX $FD
$ECE3: 6C FD 00  JMP ($00FD)
$ECE6: 07        db $07
$ECE7: F2        db $F2
$ECE8: 07        db $07
$ECE9: 80        db $80
$ECEA: 07        db $07
$ECEB: 14        db $14
$ECEC: 06 AE     ASL $AE
$ECEE: 06 43     ASL $43
$ECF0: 05 F4     ORA $F4
$ECF2: 05 9E     ORA $9E
$ECF4: 05 4E     ORA $4E
$ECF6: 05 02     ORA $02
$ECF8: 04        db $04
$ECF9: BA        TSX
$ECFA: 04        db $04
$ECFB: 76 04     ROR $04,X
$ECFD: 36 2C     ROL $2C,X
$ECFF: EE 36 ED  INC $ED36
$ED02: 5D ED 88  EOR L_88ED,X
$ED05: ED 9F EE  SBC $EE9F
$ED08: AE EE 19  LDX $19EE
$ED0B: EE B3 ED  INC $EDB3
$ED0E: D5 ED     CMP $ED,X
$ED10: 48        PHA
$ED11: EE 03 EE  INC $EE03
$ED14: F4        db $F4
$ED15: ED 5E EE  SBC $EE5E
$ED18: 56 EE     LSR $EE,X
$ED1A: 67        db $67
$ED1B: EE 12 EE  INC $EE12
$ED1E: 95 EE     STA $EE,X
$ED20: 8C EE 82  STY L_82EE
$ED23: EE 73 EE  INC $EE73
$ED26: 7A        db $7A
$ED27: EE C1 EE  INC $EEC1
$ED2A: DF        db $DF
$ED2B: EE 0A EF  INC $EF0A
$ED2E: 3C        db $3C
$ED2F: EF        db $EF
$ED30: 4F        db $4F
$ED31: EF        db $EF
$ED32: 62        db $62
$ED33: EF        db $EF
$ED34: 3A        db $3A
$ED35: EE 01 81  INC L_8101
$ED38: 7F        db $7F
$ED39: 40        RTI
$ED3A: EF        db $EF
$ED3B: 68        PLA
$ED3C: 1B        db $1B
$ED3D: 2B        db $2B
$ED3E: 33        db $33
$ED3F: F0 02     BEQ L_ED43
$ED41: 06 33     ASL $33
L_ED43:
$ED43: 43        db $43
$ED44: 53        db $53
$ED45: F0 02     BEQ L_ED49
$ED47: 0C        db $0C
$ED48: 43        db $43
L_ED49:
$ED49: 53        db $53
$ED4A: 04        db $04
$ED4B: F0 02     BEQ L_ED4F
$ED4D: 12        db $12
$ED4E: 5B        db $5B
L_ED4F:
$ED4F: 0C        db $0C
$ED50: 1C        db $1C
$ED51: F0 02     BEQ L_ED55
$ED53: 18        CLC
$ED54: 78        SEI
L_ED55:
$ED55: 1C        db $1C
$ED56: 68        PLA
$ED57: 1C        db $1C
$ED58: 1C        db $1C
$ED59: 1C        db $1C
$ED5A: 78        SEI
$ED5B: 1C        db $1C
$ED5C: E8        INX
$ED5D: 03        db $03
$ED5E: 10 7F     BPL L_EDDF
$ED60: 08        PHP
$ED61: 78        SEI
$ED62: 1A        db $1A
$ED63: 68        PLA
$ED64: 1A        db $1A
$ED65: F1 03     SBC ($03),Y
$ED67: 07        db $07
$ED68: 78        SEI
$ED69: 32        db $32
$ED6A: 68        PLA
$ED6B: 32        db $32
$ED6C: F1 03     SBC ($03),Y
$ED6E: 0E 78 42  ASL $4278
$ED71: 68        PLA
$ED72: 42        db $42
$ED73: F1 03     SBC ($03),Y
$ED75: 15 5A     ORA $5A,X
$ED77: F1 03     SBC ($03),Y
$ED79: 19 0B F1  ORA $F10B,Y
$ED7C: 03        db $03
$ED7D: 1D 78 52  ORA $5278,X
$ED80: 68        PLA
$ED81: 52        db $52
$ED82: F1 03     SBC ($03),Y
$ED84: 24 78     BIT $78
$ED86: 52        db $52
$ED87: E8        INX
$ED88: 02        db $02
$ED89: 81 7F     STA ($7F,X)
$ED8B: 40        RTI
$ED8C: 78        SEI
$ED8D: 51 68     EOR ($68),Y
$ED8F: 51 F2     EOR ($F2),Y
$ED91: 03        db $03
$ED92: 07        db $07
$ED93: 78        SEI
$ED94: 0A        ASL A
$ED95: 68        PLA
$ED96: 0A        ASL A
$ED97: F2        db $F2
$ED98: 03        db $03
$ED99: 0E 78 1A  ASL $1A78
$ED9C: 68        PLA
$ED9D: 1A        db $1A
$ED9E: F2        db $F2
$ED9F: 03        db $03
$EDA0: 15 32     ORA $32,X
$EDA2: F2        db $F2
$EDA3: 03        db $03
$EDA4: 19 42 F2  ORA $F242,Y
$EDA7: 03        db $03
$EDA8: 1D 78 3A  ORA PPUCTRL_3A78,X
$EDAB: 68        PLA
$EDAC: 3A        db $3A
$EDAD: F2        db $F2
$EDAE: 03        db $03
$EDAF: 24 78     BIT $78
$EDB1: 3A        db $3A
$EDB2: E8        INX
$EDB3: 04        db $04
$EDB4: 1F        db $1F
$EDB5: 7F        db $7F
$EDB6: 30 0A     BMI L_EDC2
$EDB8: 62        db $62
$EDB9: 49 49     EOR #$49
$EDBB: EA        NOP
$EDBC: 1E 49 49  ASL $4949,X
$EDBF: EA        NOP
$EDC0: 1D 49 49  ORA $4949,X
$EDC3: EA        NOP
$EDC4: 1C        db $1C
$EDC5: 49 49     EOR #$49
$EDC7: EA        NOP
$EDC8: 1B        db $1B
$EDC9: 49 49     EOR #$49
$EDCB: EA        NOP
$EDCC: 1A        db $1A
$EDCD: 49 EA     EOR #$EA
$EDCF: 19 49 EA  ORA $EA49,Y
$EDD2: 18        CLC
$EDD3: 49 E8     EOR #$E8
$EDD5: 02        db $02
$EDD6: 1F        db $1F
$EDD7: 7F        db $7F
$EDD8: 30 62     BMI L_EE3C
$EDDA: 00        BRK
$EDDB: 01 00     ORA ($00,X)
$EDDD: EA        NOP
$EDDE: 1E 01 00  ASL $0001,X
$EDE1: EA        NOP
$EDE2: 1D 01 00  ORA $0001,X
$EDE5: 01 00     ORA ($00,X)
$EDE7: EA        NOP
$EDE8: 1C        db $1C
$EDE9: 01 EA     ORA ($EA,X)
$EDEB: 1B        db $1B
$EDEC: 00        BRK
$EDED: EA        NOP
$EDEE: 1A        db $1A
$EDEF: 01 EA     ORA ($EA,X)
$EDF1: 19 00 E8  ORA $E800,Y
$EDF4: 02        db $02
$EDF5: 20 7F 30  JSR L_307F
$EDF8: 63        db $63
$EDF9: 1A        db $1A
$EDFA: 12        db $12
$EDFB: 51 31     EOR ($31),Y
$EDFD: 19 11 50  ORA $5011,Y
$EE00: 30 18     BMI L_EE1A
$EE02: E8        INX
$EE03: 04        db $04
$EE04: 1F        db $1F
$EE05: 7F        db $7F
$EE06: 40        RTI
$EE07: 0A        ASL A
$EE08: 62        db $62
$EE09: 51 EA     EOR ($EA),Y
$EE0B: 1E 51 EA  ASL $EA51,X
$EE0E: 08        PHP
$EE0F: 6A        ROR A
$EE10: 51 E8     EOR ($E8),Y
$EE12: 01 8F     ORA ($8F,X)
$EE14: 82        db $82
$EE15: 10 6F     BPL L_EE86
$EE17: 2C E8 02  BIT $02E8
L_EE1A:
$EE1A: 80        db $80
$EE1B: 7F        db $7F
$EE1C: 40        RTI
$EE1D: 63        db $63
$EE1E: 52        db $52
$EE1F: 1B        db $1B
$EE20: 3B        db $3B
$EE21: 53        db $53
$EE22: 4A        LSR A
$EE23: 13        db $13
$EE24: 33        db $33
$EE25: 4B        db $4B
$EE26: 1B        db $1B
$EE27: 3B        db $3B
$EE28: 53        db $53
$EE29: 1C        db $1C
$EE2A: 3C        db $3C
$EE2B: E8        INX
$EE2C: 02        db $02
$EE2D: 82        db $82
$EE2E: 7F        db $7F
$EE2F: 40        RTI
$EE30: 64        db $64
$EE31: 1B        db $1B
$EE32: 2B        db $2B
$EE33: 3B        db $3B
$EE34: 1C        db $1C
$EE35: 2C 3C 6C  BIT $6C3C
$EE38: 53        db $53
$EE39: E8        INX
$EE3A: 02        db $02
$EE3B: 82        db $82
L_EE3C:
$EE3C: 7F        db $7F
$EE3D: 40        RTI
$EE3E: 63        db $63
$EE3F: 53        db $53
$EE40: 1B        db $1B
$EE41: 1C        db $1C
$EE42: 3B        db $3B
$EE43: 3C        db $3C
$EE44: 53        db $53
$EE45: 6A        ROR A
$EE46: 54        db $54
$EE47: E8        INX
$EE48: 02        db $02
$EE49: 60        RTS
$EE4A: 7F        db $7F
$EE4B: 40        RTI
$EE4C: 64        db $64
$EE4D: 52        db $52
$EE4E: 3A        db $3A
$EE4F: 52        db $52
$EE50: 03        db $03
$EE51: 52        db $52
$EE52: 03        db $03
$EE53: 13        db $13
$EE54: 1B        db $1B
$EE55: E8        INX
$EE56: 02        db $02
$EE57: D5 7F     CMP $7F,X
$EE59: 00        BRK
$EE5A: 62        db $62
$EE5B: 1C        db $1C
$EE5C: 1D E8 03  ORA $03E8,X
$EE5F: 07        db $07
$EE60: 7F        db $7F
$EE61: 08        PHP
$EE62: 61 3A     ADC ($3A,X)
$EE64: 13        db $13
$EE65: 22        db $22
$EE66: E8        INX
$EE67: 02        db $02
$EE68: 40        RTI
$EE69: 7F        db $7F
$EE6A: 00        BRK
$EE6B: 61 3D     ADC ($3D,X)
$EE6D: 62        db $62
$EE6E: 45 EA     EOR $EA
$EE70: 10 28     BPL L_EE9A
$EE72: E8        INX
$EE73: 02        db $02
$EE74: 80        db $80
$EE75: 7F        db $7F
$EE76: 18        CLC
$EE77: 61 39     ADC ($39,X)
$EE79: E8        INX
$EE7A: 04        db $04
$EE7B: 00        BRK
$EE7C: 7F        db $7F
$EE7D: 28        PLP
$EE7E: 0A        ASL A
$EE7F: 61 28     ADC ($28,X)
$EE81: E8        INX
$EE82: 02        db $02
$EE83: 8C 94 40  STY $4094
L_EE86:
$EE86: 61 10     ADC ($10,X)
$EE88: 64        db $64
L_EE89:
$EE89: 18        CLC
$EE8A: F9 05 02  SBC $0205,Y
$EE8D: 80        db $80
$EE8E: 94 48     STY $48,X
$EE90: 62        db $62
$EE91: 40        RTI
$EE92: 48        PHA
$EE93: F9 05 01  SBC $0105,Y
$EE96: 1F        db $1F
$EE97: 7F        db $7F
$EE98: 28        PLP
$EE99: 61 22     ADC ($22,X)
$EE9B: 42        db $42
$EE9C: 5A        db $5A
$EE9D: 1B        db $1B
$EE9E: E8        INX
$EE9F: 01 A0     ORA ($A0,X)
$EEA1: 7F        db $7F
$EEA2: 40        RTI
$EEA3: 66 1C     ROR $1C
$EEA5: 3C        db $3C
$EEA6: 1C        db $1C
$EEA7: 53        db $53
$EEA8: 1C        db $1C
$EEA9: 3C        db $3C
$EEAA: 05 72     ORA $72
$EEAC: 54        db $54
$EEAD: E8        INX
$EEAE: 02        db $02
$EEAF: 90 7F     BCC L_EF30
$EEB1: 40        RTI
$EEB2: 62        db $62
$EEB3: 38        SEC
$EEB4: 66 EA     ROR $EA
$EEB6: 20 3B 53  JSR L_533B
$EEB9: 3B        db $3B
$EEBA: 1B        db $1B
$EEBB: 3B        db $3B
$EEBC: 53        db $53
$EEBD: 1C        db $1C
$EEBE: 6A        ROR A
$EEBF: 14        db $14
$EEC0: E8        INX
L_EEC1:
$EEC1: 01 B8     ORA ($B8,X)
$EEC3: 7F        db $7F
$EEC4: 40        RTI
L_EEC5:
$EEC5: EF        db $EF
$EEC6: 65 0C     ADC $0C
$EEC8: 53        db $53
$EEC9: F0 0C     BEQ L_EED7
$EECB: 05 0C     ORA $0C
$EECD: 53        db $53
$EECE: F0 0C     BEQ L_EEDC
$EED0: 0B        db $0B
$EED1: 34        db $34
$EED2: 24 F0     BIT $F0
$EED4: 08        PHP
$EED5: 10 EA     BPL L_EEC1
L_EED7:
$EED7: 30 B0     BMI L_EE89
$EED9: 50 EA     BVC L_EEC5
$EEDB: 20 9C 54  JSR L_549C
$EEDE: E8        INX
$EEDF: 02        db $02
$EEE0: B8        CLV
$EEE1: 7F        db $7F
$EEE2: 40        RTI
$EEE3: 65 43     ADC $43
$EEE5: 33        db $33
$EEE6: F1 0C     SBC ($0C),Y
$EEE8: 04        db $04
$EEE9: 43        db $43
$EEEA: 33        db $33
$EEEB: F1 0C     SBC ($0C),Y
$EEED: 0A        ASL A
$EEEE: 14        db $14
$EEEF: 4B        db $4B
$EEF0: F1 08     SBC ($08),Y
$EEF2: 0F        db $0F
$EEF3: EA        NOP
$EEF4: 3A        db $3A
$EEF5: 30 50     BMI L_EF47
$EEF7: 09 29     ORA #$29
$EEF9: 31 51     AND ($51),Y
$EEFB: 0A        ASL A
$EEFC: 2A        ROL A
$EEFD: 32        db $32
$EEFE: 52        db $52
$EEFF: 0B        db $0B
$EF00: 2B        db $2B
$EF01: 33        db $33
$EF02: 53        db $53
$EF03: 0C        db $0C
$EF04: 2C 9C EA  BIT $EA9C
$EF07: 20 2C E8  JSR L_E82C
$EF0A: 03        db $03
$EF0B: 00        BRK
$EF0C: 7F        db $7F
$EF0D: 08        PHP
$EF0E: A1 01     LDA ($01,X)
$EF10: 01 EE     ORA ($EE,X)
$EF12: 15 6A     ORA $6A,X
$EF14: 0B        db $0B
$EF15: 0B        db $0B
$EF16: 0B        db $0B
$EF17: EE 22 6F  INC $6F22
$EF1A: 33        db $33
$EF1B: 65 43     ADC $43
$EF1D: 7E EE 33  ROR PPUADDR_33EE,X
$EF20: 53        db $53
$EF21: 6A        ROR A
$EF22: EE 15 43  INC $4315
$EF25: 33        db $33
$EF26: 53        db $53
$EF27: 6F        db $6F
$EF28: EE 22 13  INC $1322
$EF2B: 65 23     ADC $23
$EF2D: 7E EE 33  ROR PPUADDR_33EE,X
L_EF30:
$EF30: 33        db $33
$EF31: 6A        ROR A
$EF32: EE 15 23  INC PPUSCROLL_2315
$EF35: 13        db $13
$EF36: 4A        LSR A
$EF37: 9C        db $9C
$EF38: EE FF 32  INC PPUDATA_32FF
$EF3B: E8        INX
$EF3C: 01 42     ORA ($42,X)
$EF3E: 7F        db $7F
$EF3F: 40        RTI
$EF40: 66 1B     ROR $1B
$EF42: 0B        db $0B
$EF43: 78        SEI
$EF44: 1B        db $1B
$EF45: 68        PLA
$EF46: 52        db $52
L_EF47:
$EF47: 42        db $42
$EF48: 32        db $32
$EF49: 1A        db $1A
$EF4A: 1A        db $1A
$EF4B: 1A        db $1A
$EF4C: 78        SEI
$EF4D: 1A        db $1A
$EF4E: E8        INX
$EF4F: 02        db $02
$EF50: 82        db $82
$EF51: 7F        db $7F
$EF52: 40        RTI
$EF53: 66 52     ROR $52
$EF55: 52        db $52
$EF56: 78        SEI
$EF57: 52        db $52
$EF58: 68        PLA
$EF59: 32        db $32
$EF5A: 2A        ROL A
$EF5B: 12        db $12
$EF5C: 1A        db $1A
$EF5D: 1A        db $1A
$EF5E: 1A        db $1A
$EF5F: 78        SEI
$EF60: 1A        db $1A
$EF61: E8        INX
$EF62: 03        db $03
$EF63: 10 7F     BPL L_EFE4
$EF65: 08        PHP
$EF66: 66 3B     ROR $3B
$EF68: 33        db $33
$EF69: 78        SEI
$EF6A: 3B        db $3B
$EF6B: 68        PLA
$EF6C: 1B        db $1B
$EF6D: 0B        db $0B
$EF6E: 52        db $52
$EF6F: 52        db $52
$EF70: 52        db $52
$EF71: 52        db $52
$EF72: 78        SEI
$EF73: 52        db $52
$EF74: E8        INX
$EF75: FF        db $FF
$EF76: FF        db $FF
$EF77: FF        db $FF
$EF78: FF        db $FF
$EF79: FF        db $FF
$EF7A: FF        db $FF
$EF7B: FF        db $FF
$EF7C: FF        db $FF
$EF7D: FF        db $FF
$EF7E: FF        db $FF
$EF7F: FF        db $FF
$EF80: FF        db $FF
$EF81: FF        db $FF
$EF82: FF        db $FF
$EF83: FF        db $FF
$EF84: FF        db $FF
$EF85: FF        db $FF
$EF86: FF        db $FF
$EF87: FF        db $FF
$EF88: FF        db $FF
$EF89: FF        db $FF
$EF8A: FF        db $FF
$EF8B: FF        db $FF
$EF8C: FF        db $FF
$EF8D: FF        db $FF
$EF8E: FF        db $FF
$EF8F: FF        db $FF
$EF90: FF        db $FF
$EF91: FF        db $FF
$EF92: FF        db $FF
$EF93: FF        db $FF
$EF94: FF        db $FF
$EF95: FF        db $FF
$EF96: FF        db $FF
$EF97: FF        db $FF
$EF98: FF        db $FF
$EF99: FF        db $FF
$EF9A: FF        db $FF
$EF9B: FF        db $FF
$EF9C: FF        db $FF
$EF9D: FF        db $FF
$EF9E: FF        db $FF
$EF9F: FF        db $FF
$EFA0: FF        db $FF
$EFA1: FF        db $FF
$EFA2: FF        db $FF
$EFA3: FF        db $FF
$EFA4: FF        db $FF
$EFA5: FF        db $FF
$EFA6: FF        db $FF
$EFA7: FF        db $FF
$EFA8: FF        db $FF
$EFA9: FF        db $FF
$EFAA: FF        db $FF
$EFAB: FF        db $FF
$EFAC: FF        db $FF
$EFAD: FF        db $FF
$EFAE: FF        db $FF
$EFAF: FF        db $FF
$EFB0: FF        db $FF
$EFB1: FF        db $FF
$EFB2: FF        db $FF
$EFB3: FF        db $FF
$EFB4: FF        db $FF
$EFB5: FF        db $FF
$EFB6: FF        db $FF
$EFB7: FF        db $FF
$EFB8: FF        db $FF
$EFB9: FF        db $FF
$EFBA: FF        db $FF
$EFBB: FF        db $FF
$EFBC: FF        db $FF
$EFBD: FF        db $FF
$EFBE: FF        db $FF
$EFBF: FF        db $FF
$EFC0: FF        db $FF
$EFC1: FF        db $FF
$EFC2: FF        db $FF
$EFC3: FF        db $FF
$EFC4: FF        db $FF
$EFC5: FF        db $FF
$EFC6: FF        db $FF
$EFC7: FF        db $FF
$EFC8: FF        db $FF
$EFC9: FF        db $FF
$EFCA: FF        db $FF
$EFCB: FF        db $FF
$EFCC: FF        db $FF
$EFCD: FF        db $FF
$EFCE: FF        db $FF
$EFCF: FF        db $FF
$EFD0: FF        db $FF
$EFD1: FF        db $FF
$EFD2: FF        db $FF
$EFD3: FF        db $FF
$EFD4: FF        db $FF
$EFD5: FF        db $FF
$EFD6: FF        db $FF
$EFD7: FF        db $FF
$EFD8: FF        db $FF
$EFD9: FF        db $FF
$EFDA: FF        db $FF
$EFDB: FF        db $FF
$EFDC: FF        db $FF
$EFDD: FF        db $FF
$EFDE: FF        db $FF
$EFDF: FF        db $FF
$EFE0: FF        db $FF
$EFE1: FF        db $FF
$EFE2: FF        db $FF
$EFE3: FF        db $FF
L_EFE4:
$EFE4: FF        db $FF
$EFE5: FF        db $FF
$EFE6: FF        db $FF
$EFE7: FF        db $FF
$EFE8: FF        db $FF
$EFE9: FF        db $FF
$EFEA: FF        db $FF
$EFEB: FF        db $FF
$EFEC: FF        db $FF
$EFED: FF        db $FF
$EFEE: FF        db $FF
$EFEF: FF        db $FF
$EFF0: FF        db $FF
$EFF1: FF        db $FF
$EFF2: FF        db $FF
$EFF3: FF        db $FF
$EFF4: FF        db $FF
$EFF5: FF        db $FF
$EFF6: FF        db $FF
$EFF7: FF        db $FF
$EFF8: FF        db $FF
$EFF9: FF        db $FF
$EFFA: FF        db $FF
$EFFB: FF        db $FF
$EFFC: FF        db $FF
$EFFD: FF        db $FF
$EFFE: FF        db $FF
$EFFF: FF        db $FF
L_F000:
$F000: C9 FF     CMP #$FF
$F002: D0 05     BNE L_F009
$F004: A9 24     LDA #$24
$F006: 4C 10 F0  JMP L_F010
L_F009:
$F009: C9 24     CMP #$24
$F00B: 90 03     BCC L_F010
$F00D: 38        SEC
$F00E: E9 23     SBC #$23
L_F010:
$F010: 85 00     STA $00
$F012: A9 F0     LDA #$F0
$F014: 85 12     STA $12
$F016: A9 7A     LDA #$7A
$F018: 85 11     STA $11
L_F01A:
$F01A: C6 00     DEC $00
$F01C: F0 08     BEQ L_F026
$F01E: A9 5B     LDA #$5B
$F020: 20 AA D7  JSR L_D7AA
$F023: 4C 1A F0  JMP L_F01A
L_F026:
$F026: A9 00     LDA #$00
$F028: 85 5A     STA $5A
$F02A: A5 11     LDA $11
$F02C: 85 13     STA $13
$F02E: A5 12     LDA $12
$F030: 85 14     STA $14
$F032: A9 10     LDA #$10
$F034: 85 57     STA $57
L_F036:
$F036: 20 F6 D8  JSR L_D8F6
$F039: A9 10     LDA #$10
$F03B: 85 56     STA $56
L_F03D:
$F03D: A5 5A     LDA $5A
$F03F: 4A        LSR A
$F040: A8        TAY
$F041: A5 5A     LDA $5A
$F043: 29 01     AND #$01
$F045: F0 07     BEQ L_F04E
$F047: B1 13     LDA ($13),Y
$F049: 29 0F     AND #$0F
$F04B: 4C 54 F0  JMP L_F054
L_F04E:
$F04E: B1 13     LDA ($13),Y
$F050: 4A        LSR A
$F051: 4A        LSR A
$F052: 4A        LSR A
$F053: 4A        LSR A
L_F054:
$F054: A6 56     LDX $56
$F056: A4 57     LDY $57
$F058: 20 0B D8  JSR L_D80B
$F05B: A9 00     LDA #$00
$F05D: 85 0C     STA $0C
$F05F: E6 5A     INC $5A
$F061: A5 56     LDA $56
$F063: 18        CLC
$F064: 69 10     ADC #$10
$F066: 85 56     STA $56
$F068: C9 E0     CMP #$E0
$F06A: D0 D1     BNE L_F03D
$F06C: E6 5A     INC $5A
$F06E: A5 57     LDA $57
$F070: 18        CLC
$F071: 69 10     ADC #$10
$F073: 85 57     STA $57
$F075: C9 E0     CMP #$E0
$F077: D0 BD     BNE L_F036
$F079: 60        RTS
$F07A: DD DD DD  CMP $DDDD,X
$F07D: DD DD DD  CMP $DDDD,X
$F080: DD D4 D4  CMP $D4D4,X
$F083: D4        db $D4
$F084: D4        db $D4
$F085: D4        db $D4
$F086: D4        db $D4
$F087: DD D4 D4  CMP $D4D4,X
$F08A: D4        db $D4
$F08B: D4        db $D4
$F08C: D4        db $D4
$F08D: D4        db $D4
$F08E: DD D4 D4  CMP $D4D4,X
$F091: D4        db $D4
$F092: 94 D4     STY $D4,X
$F094: D4        db $D4
$F095: DD D4 D4  CMP $D4D4,X
$F098: D3        db $D3
$F099: D3        db $D3
$F09A: D4        db $D4
$F09B: D4        db $D4
$F09C: DD D3 D3  CMP $D3D3,X
$F09F: D1 D1     CMP ($D1),Y
$F0A1: D3        db $D3
$F0A2: D3        db $D3
$F0A3: DD 1D 11  CMP $111D,X
$F0A6: D3        db $D3
$F0A7: D3        db $D3
$F0A8: D1 1D     CMP ($1D),Y
$F0AA: 1D 8D 33  ORA PPUSCROLL_338D,X
$F0AD: D1 D1     CMP ($D1),Y
$F0AF: D3        db $D3
$F0B0: 3D 8D D1  AND $D18D,X
$F0B3: D1 D4     CMP ($D4),Y
$F0B5: 44        db $44
$F0B6: D1 D1     CMP ($D1),Y
$F0B8: DD D4 D4  CMP $D4D4,X
$F0BB: D4        db $D4
$F0BC: D4        db $D4
$F0BD: D4        db $D4
$F0BE: D4        db $D4
$F0BF: DD D4 D4  CMP $D4D4,X
$F0C2: D3        db $D3
$F0C3: D3        db $D3
$F0C4: D4        db $D4
$F0C5: D4        db $D4
$F0C6: DD D4 D4  CMP $D4D4,X
$F0C9: DD DD D4  CMP $D4DD,X
$F0CC: D4        db $D4
$F0CD: DD DD DD  CMP $DDDD,X
$F0D0: DD DD DD  CMP $DDDD,X
$F0D3: DD DD DD  CMP $DDDD,X
$F0D6: D9 DD D9  CMP $D9DD,Y
$F0D9: DD DD DD  CMP $DDDD,X
$F0DC: D4        db $D4
$F0DD: D9 DD D4  CMP $D4DD,Y
$F0E0: D4        db $D4
$F0E1: D4        db $D4
$F0E2: DD D4 DD  CMP $DDD4,X
$F0E5: DD 44 D4  CMP $D444,X
$F0E8: 94 DD     STY $DD,X
$F0EA: DD D4 DD  CMP $DDD4,X
$F0ED: DD D9 DD  CMP $DDD9,X
$F0F0: DD BD D4  CMP $D4BD,X
$F0F3: DD 9D D4  CMP $D49D,X
$F0F6: B4 9D     LDY $9D,X
$F0F8: BB        db $BB
$F0F9: DD D4 DD  CMP $DDD4,X
$F0FC: 9D BD DD  STA $DDBD,X
$F0FF: D4        db $D4
$F100: 44        db $44
$F101: BB        db $BB
$F102: B9 DD B4  LDA L_B4DD,Y
$F105: DD DD D9  CMP $D9DD,X
$F108: B4 D4     LDY $D4,X
$F10A: D4        db $D4
$F10B: D4        db $D4
$F10C: DD 94 D9  CMP $D994,X
$F10F: D4        db $D4
$F110: D4        db $D4
$F111: DD D4 DD  CMP $DDD4,X
$F114: D4        db $D4
$F115: D4        db $D4
$F116: D4        db $D4
$F117: 44        db $44
$F118: D4        db $D4
$F119: 94 DD     STY $DD,X
$F11B: D4        db $D4
$F11C: D4        db $D4
$F11D: D4        db $D4
$F11E: 44        db $44
$F11F: DD DD DD  CMP $DDDD,X
$F122: D4        db $D4
$F123: DD DD DD  CMP $DDDD,X
$F126: D4        db $D4
$F127: D4        db $D4
$F128: DD D4 D4  CMP $D4D4,X
$F12B: DD DD D4  CMP $D4DD,X
$F12E: 44        db $44
$F12F: DD DD DD  CMP $DDDD,X
$F132: 4D DD 4D  EOR $4DDD
$F135: DD DD DB  CMP $DBDD,X
$F138: BB        db $BB
$F139: 4D DD DD  EOR $DDDD
$F13C: 66 6D     ROR $6D
$F13E: 4B        db $4B
$F13F: BB        db $BB
$F140: DD DD DD  CMP $DDDD,X
$F143: DD DD BB  CMP L_BBDD,X
$F146: BB        db $BB
$F147: DD D4 D4  CMP $D4D4,X
$F14A: 44        db $44
$F14B: 2D BB BB  AND L_BBBB
$F14E: 44        db $44
$F14F: 43        db $43
$F150: D4        db $D4
$F151: D0 DD     BNE L_F130
$F153: BB        db $BB
$F154: BB        db $BB
$F155: DD 4D DD  CMP $DD4D,X
$F158: D0 DD     BNE L_F137
$F15A: DB        db $DB
$F15B: DD DD 99  CMP L_99DD,X
$F15E: 9D DB DD  STA $DDDB,X
$F161: D1 D1     CMP ($D1),Y
$F163: DD DD DB  CMP $DBDD,X
$F166: BB        db $BB
$F167: BD 42 04  LDA $0442,X
$F16A: 20 33 3B  JSR L_3B33
$F16D: BB        db $BB
$F16E: BD DD DD  LDA $DDDD,X
$F171: D4        db $D4
$F172: D1 1B     CMP ($1B),Y
$F174: BB        db $BB
$F175: BD 4D D7  LDA $D74D,X
$F178: DD D3 3B  CMP OAMADDR_3BD3,X
$F17B: BB        db $BB
$F17C: DD 44 D7  CMP $D744,X
$F17F: DD DD DB  CMP $DBDD,X
$F182: BB        db $BB
$F183: DD 94 4D  CMP $4D94,X
$F186: DD DD D4  CMP $D4DD,X
$F189: DD DD DB  CMP $DBDD,X
$F18C: BD DD DD  LDA $DDDD,X
$F18F: DD DB DD  CMP $DDDB,X
$F192: BB        db $BB
$F193: DD 14 41  CMP $4114,X
$F196: 1D DD BD  ORA L_BDDD,X
$F199: BD D0 44  LDA $44D0,X
$F19C: 44        db $44
$F19D: 44        db $44
$F19E: 1D 8D 8D  ORA L_8D8D,X
$F1A1: D4        db $D4
$F1A2: 44        db $44
$F1A3: 44        db $44
$F1A4: 44        db $44
$F1A5: 42        db $42
$F1A6: DD DD 03  CMP $03DD,X
$F1A9: DD D3 44  CMP $44D3,X
$F1AC: D2        db $D2
$F1AD: DD AD 0D  CMP $0DAD,X
$F1B0: 7D 7D 42  ADC $427D,X
$F1B3: DD DD DD  CMP $DDDD,X
$F1B6: 4D 11 DD  EOR $DD11
$F1B9: 42        db $42
$F1BA: DA        db $DA
$F1BB: AD DD 44  LDA $44DD
$F1BE: 44        db $44
$F1BF: 44        db $44
$F1C0: 44        db $44
$F1C1: DD DD D0  CMP $D0DD,X
$F1C4: 44        db $44
$F1C5: 44        db $44
$F1C6: 44        db $44
$F1C7: 44        db $44
$F1C8: 2D DD D3  AND $D3DD
$F1CB: 34        db $34
$F1CC: 44        db $44
$F1CD: 44        db $44
$F1CE: 43        db $43
$F1CF: 3D DD D4  AND $D4DD,X
$F1D2: 41 34     EOR ($34,X)
$F1D4: 43        db $43
$F1D5: 14        db $14
$F1D6: 4D BD BD  EOR L_BDBD
$F1D9: 33        db $33
$F1DA: DD DD 33  CMP PPUSCROLL_33DD,X
$F1DD: DB        db $DB
$F1DE: BD 9B DD  LDA $DD9B,X
$F1E1: DD DD DD  CMP $DDDD,X
$F1E4: BB        db $BB
$F1E5: 9D DD DD  STA $DDDD,X
$F1E8: 44        db $44
$F1E9: 4D DD DD  EOR $DDDD
$F1EC: DD 6D 1D  CMP $1D6D,X
$F1EF: 4D DD 88  EOR L_88DD
$F1F2: 9D DD 9D  STA L_9DDD,X
$F1F5: 4D DD 4D  EOR $4DDD
$F1F8: DD DD DD  CMP $DDDD,X
$F1FB: 4D 44 4D  EOR $4D44
$F1FE: 44        db $44
$F1FF: DA        db $DA
$F200: AD AD 3D  LDA PPUSCROLL_3DAD
$F203: DD 3D DD  CMP $DD3D,X
$F206: DA        db $DA
$F207: DD DD DD  CMP $DDDD,X
$F20A: 1D AA DA  ORA $DAAA,X
$F20D: AA        TAX
$F20E: D4        db $D4
$F20F: 4D 44 DD  EOR $DD44
$F212: A4 D4     LDY $D4
$F214: 2D DD DD  AND $DDDD
$F217: DD DD AD  CMP L_ADDD,X
$F21A: DD DD 57  CMP $57DD,X
$F21D: DD AA AD  CMP L_ADAA,X
$F220: AD 9D 4D  LDA $4D9D
$F223: 5D DD DD  EOR $DDDD,X
$F226: D1 1D     CMP ($1D),Y
$F228: DD DD 54  CMP $54DD,X
$F22B: 4D DD DD  EOR $DDDD
$F22E: 43        db $43
$F22F: 33        db $33
$F230: 41 DD     EOR ($DD,X)
$F232: DD 44 3D  CMP OAMDATA_3D44,X
$F235: DD DD D3  CMP $D3DD,X
$F238: 4D DD 3D  EOR PPUSCROLL_3DDD
$F23B: DD DD DD  CMP $DDDD,X
$F23E: DD DD DD  CMP $DDDD,X
$F241: DD DD D0  CMP $D0DD,X
$F244: D2        db $D2
$F245: BB        db $BB
$F246: DD DD D2  CMP $D2DD,X
$F249: 5D 2D DD  EOR $DD2D,X
$F24C: 0B        db $0B
$F24D: 20 BD D2  JSR L_D2BD
$F250: 5D 2D 4D  EOR $4D2D,X
$F253: 0B        db $0B
$F254: 20 BD D4  JSR L_D4BD
$F257: DD 4D 9D  CMP L_9D4D,X
$F25A: 4B        db $4B
$F25B: D4        db $D4
$F25C: BD DD D0  LDA $D0DD,X
$F25F: 8D 4D 37  STA PPUSCROLL_374D
$F262: DB        db $DB
$F263: BD 44 2D  LDA OAMDATA_2D44,X
$F266: DB        db $DB
$F267: 4B        db $4B
$F268: DD 04 4D  CMP $4D04,X
$F26B: DD DD 0B  CMP $0BDD,X
$F26E: BB        db $BB
$F26F: 2D DD DD  AND $DDDD
$F272: 94 4D     STY $4D,X
$F274: 3B        db $3B
$F275: BB        db $BB
$F276: 30 44     BMI L_F2BC
$F278: 9D 88 8D  STA L_8D88,X
$F27B: 1D BD 1D  ORA $1DBD,X
$F27E: 88        DEY
$F27F: 8D D4 DD  STA $DDD4
$F282: 4D DD 4D  EOR $4DDD
$F285: DD DD D4  CMP $D4DD,X
$F288: 2D D3 D3  AND $D3D3
$F28B: DD 04 BD  CMP L_BD04,X
$F28E: DD 3D DD  CMP $DD3D,X
$F291: DD DD BB  CMP L_BBDD,X
$F294: BD DD 1D  LDA $1DDD,X
$F297: DD DD DD  CMP $DDDD,X
$F29A: 1B        db $1B
$F29B: BD DD DD  LDA $DDDD,X
$F29E: DD D8 8D  CMP L_8DD8,X
$F2A1: DD DD DD  CMP $DDDD,X
$F2A4: 98        TYA
$F2A5: 88        DEY
$F2A6: DD DD 9D  CMP L_9DDD,X
$F2A9: DD DD 9D  CMP L_9DDD,X
$F2AC: DD BD 89  CMP L_89BD,X
$F2AF: 9D DD D9  STA $D9DD,X
$F2B2: DD DB 9D  CMP L_9DDB,X
$F2B5: DD 9D DD  CMP $DD9D,X
$F2B8: DD DD B9  CMP L_B9DD,X
$F2BB: 9D DD 89  STA L_89DD,X
$F2BE: DD D9 DB  CMP $DBD9,X
$F2C1: 99 9D 9D  STA L_9D9D,Y
$F2C4: DD DD D5  CMP $D5DD,X
$F2C7: D9 9D DD  CMP $DD9D,Y
$F2CA: 99 DD DD  STA $DDDD,Y
$F2CD: 7D DD 9D  ADC L_9DDD,X
$F2D0: 99 9D D5  STA $D59D,Y
$F2D3: DD D5 9D  CMP L_9DD5,X
$F2D6: DD 99 BD  CMP L_BD99,X
$F2D9: D9 DD D9  CMP $D9DD,Y
$F2DC: DD DD 9B  CMP L_9BDD,X
$F2DF: DD 99 DD  CMP $DD99,X
$F2E2: D8        CLD
$F2E3: 89        db $89
$F2E4: DD BD D9  CMP $D9BD,X
$F2E7: DD DD DD  CMP $DDDD,X
$F2EA: DD DD DD  CMP $DDDD,X
$F2ED: D8        CLD
$F2EE: D6 9D     DEC $9D,X
$F2F0: 66 DD     ROR $DD
$F2F2: DD DD DD  CMP $DDDD,X
$F2F5: DD DD DD  CMP $DDDD,X
$F2F8: 4D D4 D1  EOR $D1D4
$F2FB: D4        db $D4
$F2FC: DD DD B4  CMP L_B4DD,X
$F2FF: 44        db $44
$F300: D4        db $D4
$F301: D6 D4     DEC $D4,X
$F303: 2D DD BB  AND L_BBDD
$F306: BD D3 D4  LDA $D4D3,X
$F309: D3        db $D3
$F30A: D0 2D     BNE L_F339
$F30C: BA        TSX
$F30D: AA        TAX
$F30E: AA        TAX
$F30F: AA        TAX
$F310: AA        TAX
$F311: AD AD D4  LDA $D4AD
$F314: DD DD 11  CMP $11DD,X
$F317: DD DD DD  CMP $DDDD,X
$F31A: DD 4D D0  CMP $D04D,X
$F31D: 44        db $44
$F31E: 34        db $34
$F31F: 38        SEC
$F320: 8D 44 D4  STA $D444
$F323: D0 44     BNE L_F369
$F325: B4 66     LDY $66,X
$F327: 4D DD D9  EOR $D9DD
$F32A: D6 DB     DEC $DB,X
$F32C: BB        db $BB
$F32D: BD DD AA  LDA L_AADD,X
$F330: DA        db $DA
$F331: AA        TAX
$F332: AA        TAX
$F333: DA        db $DA
$F334: AA        TAX
$F335: AD BB D0  LDA $D0BB
$F338: DD 11 DD  CMP $DD11,X
$F33B: DD DD BB  CMP L_BBDD,X
$F33E: 4D 2D D0  EOR $D02D
$F341: D6 14     DEC $14,X
$F343: DD B6 4D  CMP $4DB6,X
$F346: 2D DD D3  AND $D3DD
$F349: D4        db $D4
$F34A: DD DD DD  CMP $DDDD,X
$F34D: DD DD D1  CMP $D1DD,X
$F350: D3        db $D3
$F351: DD DD D4  CMP $D4DD,X
$F354: DD DD D6  CMP $D6DD,X
$F357: BD DD 4D  LDA $4DDD,X
$F35A: DD DD 6B  CMP $6BDD,X
$F35D: 59 7D 4D  EOR $4D7D,Y
$F360: DD D6 B5  CMP L_B5D6,X
$F363: 97        db $97
$F364: D8        CLD
$F365: BD DD DD  LDA $DDDD,X
$F368: 59 7D 8B  EOR L_8B7D,Y
$F36B: DD DD DD  CMP $DDDD,X
$F36E: DD D8 BD  CMP L_BDD8,X
$F371: DD DD DD  CMP $DDDD,X
$F374: DD DD DB  CMP $DBDD,X
$F377: 6B        db $6B
$F378: DB        db $DB
$F379: 6B        db $6B
$F37A: DD DD 94  CMP L_94DD,X
$F37D: D5 97     CMP $97,X
$F37F: D5 97     CMP $97,X
$F381: D4        db $D4
$F382: 9D DD DB  STA $DBDD,X
$F385: 8B        db $8B
$F386: DB        db $DB
$F387: 8B        db $8B
$F388: DD DD DD  CMP $DDDD,X
$F38B: DD 6D DD  CMP $DD6D,X
$F38E: 6D DD DD  ADC $DDDD
$F391: 4D D5 97  EOR L_97D5
$F394: D5 97     CMP $97,X
$F396: DD 4D 4D  CMP $4D4D,X
$F399: DB        db $DB
$F39A: 8B        db $8B
$F39B: DB        db $DB
$F39C: 8B        db $8B
$F39D: DD 4D DD  CMP $DD4D,X
$F3A0: 1D DD DD  ORA $DDDD,X
$F3A3: DD 1D DD  CMP $DD1D,X
$F3A6: DD 44 DD  CMP $DD44,X
$F3A9: DD D4 4D  CMP $4DD4,X
$F3AC: DD DD DD  CMP $DDDD,X
$F3AF: DD DD DD  CMP $DDDD,X
$F3B2: DD DD D0  CMP $D0DD,X
$F3B5: 34        db $34
$F3B6: DD DD DD  CMP $DDDD,X
$F3B9: 43        db $43
$F3BA: 2D 03 DD  AND $DD03
$F3BD: 4D BB D4  EOR $D4BB
$F3C0: DD 0D 4D  CMP $4D0D,X
$F3C3: DD 4B BB  CMP L_BB4B,X
$F3C6: B4 DD     LDY $DD,X
$F3C8: 0D 4D D0  ORA $D04D
$F3CB: 4B        db $4B
$F3CC: 99 B4 2D  STA OAMDATA_2DB4,Y
$F3CF: 4D 01 14  EOR $1401
$F3D2: AA        TAX
$F3D3: AA        TAX
$F3D4: AA        TAX
$F3D5: 44        db $44
$F3D6: 4D D4 44  EOR $44D4
$F3D9: 99 49 94  STA L_9449,Y
$F3DC: 44        db $44
$F3DD: 2D DD 44  AND $44DD
$F3E0: 9D 4D 94  STA L_944D,X
$F3E3: 42        db $42
$F3E4: DD DD 44  CMP $44DD,X
$F3E7: 44        db $44
$F3E8: 44        db $44
$F3E9: 44        db $44
$F3EA: 42        db $42
$F3EB: DD 4B 33  CMP OAMADDR_334B,X
$F3EE: 39 93 33  AND OAMADDR_3393,Y
$F3F1: 3B        db $3B
$F3F2: 4D 4B BB  EOR L_BB4B
$F3F5: BB        db $BB
$F3F6: BB        db $BB
$F3F7: BB        db $BB
$F3F8: BB        db $BB
$F3F9: 4D DD BB  EOR L_BBDD
L_F3FC:
$F3FC: B1 11     LDA ($11),Y
$F3FE: BB        db $BB
$F3FF: BB        db $BB
$F400: DD DD D2  CMP $D2DD,X
$F403: D4        db $D4
$F404: D4        db $D4
$F405: DD 2D DD  CMP $DD2D,X
$F408: DD DD D9  CMP $D9DD,X
$F40B: D4        db $D4
$F40C: D4        db $D4
$F40D: 4D DD D0  EOR $D0DD
$F410: 44        db $44
$F411: 44        db $44
$F412: D4        db $D4
$F413: DD DD DD  CMP $DDDD,X
$F416: DD D2 D4  CMP $D4D2,X
$F419: D4        db $D4
$F41A: 4D BB BD  EOR L_BDBB
$F41D: D0 DD     BNE L_F3FC
$F41F: DD D9 DB  CMP $DBD9,X
$F422: BB        db $BB
$F423: BD D0 D4  LDA $D4D0,X
$F426: 44        db $44
$F427: 94 4B     STY $4B,X
$F429: B3        db $B3
$F42A: 9D D3 33  STA OAMADDR_33D3,X
$F42D: 9D D4 DB  STA $DBD4,X
$F430: BD 0D 04  LDA $040D,X
$F433: 44        db $44
$F434: D9 BB BB  CMP L_BBBB,Y
$F437: BD DD DD  LDA $DDDD,X
$F43A: D9 DD BB  CMP L_BBDD,Y
$F43D: BB        db $BB
$F43E: B4 DD     LDY $DD,X
$F440: 94 DB     STY $DB,X
$F442: BB        db $BB
$F443: B9 BB B4  LDA L_B4BB,Y
$F446: DD 04 BB  CMP L_BB04,X
$F449: BB        db $BB
$F44A: BD DD D4  LDA $D4DD,X
$F44D: 2D D4 BB  AND L_BBD4
$F450: DD DD 84  CMP L_84DD,X
$F453: 44        db $44
$F454: DD DD BB  CMP L_BBDD,X
$F457: DD DD D4  CMP $D4DD,X
$F45A: D0 DD     BNE L_F439
$F45C: D1 BB     CMP ($BB),Y
$F45E: DD DD DD  CMP $DDDD,X
$F461: DD DD DD  CMP $DDDD,X
$F464: DD DD 44  CMP $44DD,X
$F467: 44        db $44
$F468: DD DD D4  CMP $D4DD,X
$F46B: 44        db $44
$F46C: 1D 1D D4  ORA $D41D,X
$F46F: DD DD DD  CMP $DDDD,X
$F472: DD 4D 3D  CMP PPUSCROLL_3D4D,X
$F475: DD D4 4D  CMP $4DD4,X
$F478: DA        db $DA
$F479: AA        TAX
$F47A: AA        TAX
$F47B: D4        db $D4
$F47C: 2D D4 8D  AND L_8DD4
$F47F: DD 66 6A  CMP $6A66,X
$F482: D4        db $D4
$F483: D9 74 DD  CMP $DD74,Y
$F486: 4D 44 4A  EOR $4A44
$F489: AA        TAX
$F48A: DA        db $DA
$F48B: 44        db $44
$F48C: DD DD DD  CMP $DDDD,X
$F48F: 9A        TXS
$F490: DD DA 8D  CMP L_8DDA,X
$F493: DD AA AD  CMP L_ADAA,X
$F496: AA        TAX
$F497: 44        db $44
$F498: DA        db $DA
$F499: DD DD DD  CMP $DDDD,X
$F49C: DD D4 88  CMP L_88D4,X
$F49F: DA        db $DA
$F4A0: AA        TAX
$F4A1: DD 44 4D  CMP $4D44,X
$F4A4: DD DD DD  CMP $DDDD,X
$F4A7: DD DD DD  CMP $DDDD,X
$F4AA: 4D 88 DD  EOR $DD88
$F4AD: D4        db $D4
$F4AE: 4D 0D 4D  EOR $4D0D
$F4B1: DD DD DD  CMP $DDDD,X
$F4B4: D4        db $D4
$F4B5: DD 4D DD  CMP $DD4D,X
$F4B8: DD DD DD  CMP $DDDD,X
$F4BB: DD DD DD  CMP $DDDD,X
$F4BE: DD DD 1D  CMP $1DDD,X
$F4C1: DD 1D DD  CMP $DD1D,X
$F4C4: DD D4 44  CMP $44D4,X
$F4C7: 4D DD 44  EOR $44DD
$F4CA: 44        db $44
$F4CB: DD D4 DD  CMP $DDD4,X
$F4CE: DD 4D DD  CMP $DD4D,X
$F4D1: D9 DD D9  CMP $D9DD,Y
$F4D4: D4        db $D4
$F4D5: 3D DD 34  AND PPUSCROLL_34DD,X
$F4D8: D4        db $D4
$F4D9: 4D D4 D2  EOR $D2D4
$F4DC: B6 96     LDX $96,Y
$F4DE: B0 D9     BCS L_F4B9
$F4E0: 4D D3 DD  EOR $DDD3
$F4E3: BB        db $BB
$F4E4: BB        db $BB
$F4E5: BD D8 4D  LDA $4DD8,X
$F4E8: 46 DD     LSR $DD
$F4EA: BB        db $BB
$F4EB: BB        db $BB
$F4EC: BD D1 4D  LDA $4DD1,X
$F4EF: 49 D2     EOR #$D2
$F4F1: B8        CLV
$F4F2: 98        TYA
$F4F3: B0 D4     BCS L_F4C9
$F4F5: DD 44 D4  CMP $D444,X
$F4F8: 1D DD 14  ORA $14DD,X
$F4FB: D9 DD 49  CMP $49DD,Y
$F4FE: DD DD 4D  CMP $4DDD,X
$F501: DD D4 DD  CMP $DDD4,X
$F504: 44        db $44
$F505: 44        db $44
$F506: 4D DD 44  EOR $44DD
$F509: 49 9D     EOR #$9D
$F50B: 44        db $44
$F50C: DD 3D DD  CMP $DD3D,X
$F50F: 3D D4 DD  AND $DDD4,X
$F512: 44        db $44
$F513: DD DD DD  CMP $DDDD,X
$F516: DD DD DD  CMP $DDDD,X
$F519: DD DD DD  CMP $DDDD,X
$F51C: DD DD DD  CMP $DDDD,X
$F51F: DD BB DD  CMP $DDBB,X
$F522: 14        db $14
$F523: 44        db $44
$F524: 1D DB BD  ORA L_BDDB,X
$F527: BD D0 44  LDA $44D0,X
$F52A: 44        db $44
$F52B: 42        db $42
$F52C: DD BD DD  CMP $DDBD,X
$F52F: D4        db $D4
$F530: 4B        db $4B
$F531: 4B        db $4B
$F532: 44        db $44
$F533: DD DD DD  CMP $DDDD,X
$F536: D4        db $D4
$F537: BB        db $BB
$F538: 4B        db $4B
$F539: B4 DD     LDY $DD,X
$F53B: DD BD D4  CMP $D4BD,X
$F53E: 44        db $44
$F53F: 44        db $44
$F540: 44        db $44
$F541: DD BD BB  CMP L_BBBD,X
$F544: DD 4B 4B  CMP $4B4B,X
$F547: 4D DB BD  EOR L_BDDB
$F54A: AA        TAX
$F54B: AD 44 44  LDA $4444
$F54E: 4D AA AD  EOR L_ADAA
$F551: DD DD 00  CMP $00DD,X
$F554: 00        BRK
$F555: 0D DD DD  ORA $DDDD
$F558: DD DD 22  CMP PPUSCROLL_22DD,X
$F55B: 22        db $22
$F55C: 2D DD DD  AND $DDDD
$F55F: 55 5D     EOR $5D,X
$F561: DD DD DD  CMP $DDDD,X
$F564: 77        db $77
$F565: 7D 22 2D  ADC PPUSTATUS_2D22,X
$F568: DD DD DD  CMP $DDDD,X
$F56B: 00        BRK
$F56C: 0D 77 75  ORA $7577
$F56F: DD DD D7  CMP $D7DD,X
$F572: 55 5D     EOR $5D,X
$F574: DD DD 44  CMP $44DD,X
$F577: DD 4D DD  CMP $DD4D,X
$F57A: DD DB B4  CMP L_B4DB,X
$F57D: 4D DD 4D  EOR $4DDD
$F580: DD DD BB  CMP L_BBDD,X
$F583: BB        db $BB
$F584: BB        db $BB
$F585: BB        db $BB
$F586: 44        db $44
$F587: DD DD B8  CMP L_B8DD,X
$F58A: 4B        db $4B
$F58B: 44        db $44
$F58C: 4B        db $4B
$F58D: BB        db $BB
$F58E: B4 9D     LDY $9D,X
$F590: BB        db $BB
$F591: 4B        db $4B
$F592: BB        db $BB
$F593: 8B        db $8B
$F594: B4 74     LDY $74,X
$F596: DD DB B4  CMP L_B4DB,X
$F599: 6B        db $6B
$F59A: BB        db $BB
$F59B: B4 D4     LDY $D4,X
$F59D: DD D4 44  CMP $44D4,X
$F5A0: 44        db $44
$F5A1: BB        db $BB
$F5A2: 44        db $44
$F5A3: 2B        db $2B
$F5A4: BD 58 44  LDA $4458,X
$F5A7: DD D4 3D  CMP OAMDATA_3DD4,X
$F5AA: DD BD D4  CMP $D4BD,X
$F5AD: D4        db $D4
$F5AE: D6 13     DEC $13,X
$F5B0: BB        db $BB
$F5B1: 42        db $42
$F5B2: BD D4 DD  LDA $DDD4,X
$F5B5: 04        db $04
$F5B6: 3B        db $3B
$F5B7: B4 DD     LDY $DD,X
$F5B9: BD D4 42  LDA $42D4,X
$F5BC: 03        db $03
$F5BD: BB        db $BB
$F5BE: 1B        db $1B
$F5BF: 4B        db $4B
$F5C0: BD DD 4D  LDA $4DDD,X
$F5C3: BD DD 4B  LDA $4BDD,X
$F5C6: 3B        db $3B
$F5C7: DD DD 3D  CMP PPUSCROLL_3DDD,X
$F5CA: BD DD DB  LDA $DBDD,X
$F5CD: BB        db $BB
$F5CE: DD DD DD  CMP $DDDD,X
$F5D1: DD DD DD  CMP $DDDD,X
$F5D4: DD DD DD  CMP $DDDD,X
$F5D7: 9B        db $9B
$F5D8: 9D DD DD  STA $DDDD,X
$F5DB: DD DD DD  CMP $DDDD,X
$F5DE: DB        db $DB
$F5DF: DB        db $DB
$F5E0: 6D DD DD  ADC $DDDD
$F5E3: DD DB DD  CMP $DDDB,X
$F5E6: DD B1 DD  CMP $DDB1,X
$F5E9: DD DD DB  CMP $DBDD,X
$F5EC: BD DB DB  LDA $DBDB,X
$F5EF: 6D DD DD  ADC $DDDD
$F5F2: DB        db $DB
$F5F3: DB        db $DB
$F5F4: DB        db $DB
$F5F5: DD B1 DD  CMP $DDB1,X
$F5F8: DD DB DD  CMP $DDDB,X
$F5FB: BD DD BB  LDA L_BBDD,X
$F5FE: 6D DD DD  ADC $DDDD
$F601: BD DD DB  LDA $DBDD,X
$F604: BB        db $BB
$F605: B1 DD     LDA ($DD),Y
$F607: DD DB DD  CMP $DDDB,X
$F60A: BD BB BB  LDA L_BBBB,X
$F60D: DD 4D DD  CMP $DD4D,X
$F610: DD BD DB  CMP $DBBD,X
$F613: BB        db $BB
$F614: 9D 44 DD  STA $DD44,X
$F617: DD DB DB  CMP $DBDB,X
$F61A: BB        db $BB
$F61B: BD 94 4D  LDA $4D94,X
$F61E: DD DD BD  CMP L_BDDD,X
$F621: BB        db $BB
$F622: BD 99 44  LDA $4499,X
$F625: DD DD BD  CMP L_BDDD,X
$F628: DB        db $DB
$F629: BD DD DD  LDA $DDDD,X
$F62C: 1D DD DD  ORA $DDDD,X
$F62F: 1D DD D4  ORA $D4DD,X
$F632: D4        db $D4
$F633: 4D DC CC  EOR $CCDC
$F636: 44        db $44
$F637: DD D4 DD  CMP $DDD4,X
$F63A: 4D 9C CC  EOR $CC9C
$F63D: CC DD CC  CPY $CCDD
$F640: C7        db $C7
$F641: 4D D4 CC  EOR $CCD4
$F644: CC DD CC  CPY $CCDD
$F647: CC CC 44  CPY $44CC
$F64A: 02        db $02
$F64B: DD DD DD  CMP $DDDD,X
$F64E: 5C        db $5C
$F64F: CC C4 02  CPY $02C4
$F652: D8        CLD
$F653: 8D 44 44  STA $4444
$F656: CC CC CC  CPY $CCCC
$F659: C4 4D     CPY $4D
$F65B: DD D4 4C  CMP $4CD4,X
$F65E: CC C7 DD  CPY $DDC7
$F661: DD D4 44  CMP $44D4,X
$F664: DC        db $DC
$F665: CC 44 D4  CPY $D444
$F668: DD CC C4  CMP $C4CC,X
$F66B: CD DD D4  CMP $D4DD
$F66E: D4        db $D4
$F66F: DD CC CC  CMP $CCCC,X
$F672: C8        INY
$F673: D8        CLD
$F674: DD 14 DD  CMP $DD14,X
$F677: 4C CC CD  JMP L_CDCC
$F67A: DD D4 DD  CMP $DDD4,X
$F67D: DD 44 7D  CMP $7D44,X
$F680: DD DD D4  CMP $D4DD,X
$F683: D4        db $D4
$F684: DD DD DD  CMP $DDDD,X
$F687: DD DD 99  CMP L_99DD,X
$F68A: 9B        db $9B
$F68B: DD D4 DD  CMP $DDD4,X
$F68E: DD DD 9D  CMP L_9DDD,X
$F691: D9 DD 4B  CMP $4BDD,Y
$F694: 4D DD 44  EOR $44DD
$F697: 44        db $44
$F698: D9 DD D4  CMP $D4DD,Y
$F69B: B4 DD     LDY $DD,X
$F69D: 4D B4 99  EOR L_99B4
$F6A0: DD DD 4D  CMP $4DDD,X
$F6A3: B9 4B D4  LDA $D44B,Y
$F6A6: DD DD DD  CMP $DDDD,X
$F6A9: DD 9D 49  CMP $499D,X
$F6AC: 44        db $44
$F6AD: DD DD DD  CMP $DDDD,X
$F6B0: 44        db $44
$F6B1: 94 D9     STY $D9,X
$F6B3: DD DD DD  CMP $DDDD,X
$F6B6: DD 4D B4  CMP L_B44D,X
$F6B9: 9B        db $9B
$F6BA: DD DD DD  CMP $DDDD,X
$F6BD: 99 9B D4  STA $D49B,Y
$F6C0: DD 44 DD  CMP $DD44,X
$F6C3: DD 9D 44  CMP $449D,X
$F6C6: 44        db $44
$F6C7: DD 49 9D  CMP L_9D49,X
$F6CA: DD 9D D9  CMP $D99D,X
$F6CD: DD DD D9  CMP $D9DD,X
$F6D0: 44        db $44
$F6D1: DD B9 99  CMP L_99B9,X
$F6D4: DD DD DD  CMP $DDDD,X
$F6D7: 49 9D     EOR #$9D
$F6D9: DD DD DD  CMP $DDDD,X
$F6DC: DD DD D9  CMP $D9DD,X
$F6DF: 9D D4 D4  STA $D4D4,X
$F6E2: D4        db $D4
$F6E3: D4        db $D4
$F6E4: D4        db $D4
$F6E5: D4        db $D4
$F6E6: DD D4 D4  CMP $D4D4,X
$F6E9: D4        db $D4
$F6EA: D4        db $D4
$F6EB: D4        db $D4
$F6EC: D4        db $D4
$F6ED: DD D8 D8  CMP $D8D8,X
$F6F0: D8        CLD
$F6F1: D8        CLD
$F6F2: D8        CLD
$F6F3: D8        CLD
$F6F4: DD 1D 1D  CMP $1D1D,X
$F6F7: 4D DD 4D  EOR $4DDD
$F6FA: 1D 1D 4D  ORA $4D1D,X
$F6FD: 43        db $43
$F6FE: 4D 4D 43  EOR $434D
$F701: 4D 4D 8D  EOR L_8D4D
$F704: 8D 9D 8D  STA L_8D9D
$F707: 9D 8D 8D  STA L_8D8D,X
$F70A: BB        db $BB
$F70B: DD 4D BD  CMP L_BD4D,X
$F70E: 4D DB BD  EOR L_BDDB
$F711: BB        db $BB
$F712: BB        db $BB
$F713: 43        db $43
$F714: B3        db $B3
$F715: 4B        db $4B
$F716: BB        db $BB
$F717: BD BB BB  LDA L_BBBB,X
$F71A: BB        db $BB
$F71B: BB        db $BB
$F71C: BB        db $BB
$F71D: BB        db $BB
$F71E: BD 1D 1D  LDA $1D1D,X
$F721: 4B        db $4B
$F722: BB        db $BB
$F723: 4D 1D 1D  EOR $1D1D
$F726: D4        db $D4
$F727: D4        db $D4
$F728: DD BD D4  CMP $D4BD,X
$F72B: D4        db $D4
$F72C: DD D4 D4  CMP $D4D4,X
$F72F: DD DD D4  CMP $D4DD,X
$F732: D4        db $D4
$F733: DD D3 D3  CMP $D3D3,X
$F736: DD DD D3  CMP $D3DD,X
$F739: D3        db $D3
$F73A: DD DD DA  CMP $DADD,X
$F73D: D4        db $D4
$F73E: DD 4D 4D  CMP $4D4D,X
$F741: DD DD DD  CMP $DDDD,X
$F744: DD DD 4D  CMP $4DDD,X
$F747: 9D DD DD  STA $DDDD,X
$F74A: DA        db $DA
$F74B: D1 9D     CMP ($9D),Y
$F74D: 4D 4D DD  EOR $DD4D
$F750: 8D 4A D9  STA $D94A
$F753: D1 3D     CMP ($3D),Y
$F755: 4D DD DD  EOR $DDDD
$F758: 4A        LSR A
$F759: DD D4 DD  CMP $DDD4,X
$F75C: DD DD 4D  CMP $4DDD,X
$F75F: 4A        LSR A
$F760: AD AA AA  LDA L_AAAA
$F763: DD 4D DD  CMP $DD4D,X
$F766: D1 DD     CMP ($DD),Y
$F768: DB        db $DB
$F769: DA        db $DA
$F76A: D8        CLD
$F76B: 8D 44 04  STA $0444
$F76E: D9 BB BA  CMP L_BABB,Y
$F771: D1 1D     CMP ($1D),Y
$F773: 3D 0D D4  AND $D40D,X
$F776: BB        db $BB
$F777: BA        TSX
$F778: D4        db $D4
$F779: DD D6 DD  CMP $DDD6,X
$F77C: D4        db $D4
$F77D: DB        db $DB
$F77E: DA        db $DA
$F77F: DB        db $DB
$F780: DD D4 D6  CMP $D6D4,X
$F783: D3        db $D3
$F784: 33        db $33
$F785: DD BB BD  CMP L_BDBB,X
$F788: D4        db $D4
$F789: D4        db $D4
$F78A: DD DD DA  CMP $DADD,X
$F78D: BB        db $BB
$F78E: BD DD DD  LDA $DDDD,X
$F791: DD DD DA  CMP $DADD,X
$F794: DB        db $DB
$F795: DD DD D1  CMP $D1DD,X
$F798: 11 DD     ORA ($DD),Y
$F79A: 1D DD DD  ORA $DDDD,X
$F79D: D1 44     CMP ($44),Y
$F79F: 44        db $44
$F7A0: 44        db $44
$F7A1: 44        db $44
$F7A2: DD DD DB  CMP $DBDD,X
$F7A5: BB        db $BB
$F7A6: BB        db $BB
$F7A7: BB        db $BB
$F7A8: B4 4D     LDY $4D,X
$F7AA: DD BB DD  CMP $DDBB,X
$F7AD: DD DD BB  CMP L_BBDD,X
$F7B0: 44        db $44
$F7B1: DD BD 9D  CMP L_9DBD,X
$F7B4: D9 DD DB  CMP $DBDD,Y
$F7B7: BB        db $BB
$F7B8: DD BD 9D  CMP L_9DBD,X
$F7BB: D9 DD DB  CMP $DBDD,Y
$F7BE: BB        db $BB
$F7BF: DD BD DB  CMP $DBBD,X
$F7C2: DD DD BB  CMP L_BBDD,X
$F7C5: 44        db $44
$F7C6: 2D BB BB  AND L_BBBB
$F7C9: BB        db $BB
$F7CA: BB        db $BB
$F7CB: B4 44     LDY $44,X
$F7CD: 2D 4B B4  AND L_B44B
$F7D0: 4B        db $4B
$F7D1: BB        db $BB
$F7D2: 44        db $44
$F7D3: 44        db $44
$F7D4: DD D4 44  CMP $44D4,X
$F7D7: 44        db $44
$F7D8: 44        db $44
$F7D9: 44        db $44
$F7DA: 4D 9D 9D  EOR L_9D9D
$F7DD: 49 44     EOR #$44
$F7DF: 44        db $44
$F7E0: 44        db $44
$F7E1: 2D 9D D9  AND $D99D
$F7E4: 43        db $43
$F7E5: 94 44     STY $44,X
$F7E7: 44        db $44
$F7E8: 99 9D DD  STA $DD9D,Y
$F7EB: DD DD DD  CMP $DDDD,X
$F7EE: DD DD DD  CMP $DDDD,X
$F7F1: DD DD DB  CMP $DBDD,X
$F7F4: DD DD DD  CMP $DDDD,X
$F7F7: DD DD DD  CMP $DDDD,X
$F7FA: B9 BD DD  LDA $DDBD,Y
$F7FD: DD DD DD  CMP $DDDD,X
$F800: BD DB DD  LDA $DDDB,X
$F803: BB        db $BB
$F804: DD DD DB  CMP $DBDD,X
$F807: 4B        db $4B
$F808: DD DB 44  CMP $44DB,X
$F80B: BD DD DD  LDA $DDDD,X
$F80E: B4 BD     LDY $BD,X
$F810: DD BB DD  CMP $DDBB,X
$F813: BD BD DB  LDA $DBBD,X
$F816: DD BD DD  CMP $DDBD,X
$F819: DB        db $DB
$F81A: 9D 4B DD  STA $DD4B,X
$F81D: DB        db $DB
$F81E: 9B        db $9B
$F81F: DD BD BD  CMP L_BDBD,X
$F822: 94 BD     STY $BD,X
$F824: DD BD DB  CMP $DBBD,X
$F827: 9B        db $9B
$F828: DD 4B DD  CMP $DD4B,X
$F82B: BD DD BD  LDA L_BDDD,X
$F82E: BD DD BD  LDA L_BDDD,X
$F831: DB        db $DB
$F832: 4B        db $4B
$F833: DB        db $DB
$F834: 4B        db $4B
$F835: DD DD DD  CMP $DDDD,X
$F838: DB        db $DB
$F839: 4B        db $4B
$F83A: DD BD DB  CMP $DBBD,X
$F83D: DD DB DD  CMP $DDDB,X
$F840: BD DD DD  LDA $DDDD,X
$F843: B9 BD B9  LDA L_B9BD,Y
$F846: BD DD DD  LDA $DDDD,X
$F849: DB        db $DB
$F84A: 4B        db $4B
$F84B: DD DD DD  CMP $DDDD,X
$F84E: DD DD DD  CMP $DDDD,X
$F851: DD DD DD  CMP $DDDD,X
$F854: DD D9 9D  CMP L_9DD9,X
$F857: DD DD DD  CMP $DDDD,X
$F85A: DD DD DD  CMP $DDDD,X
$F85D: 9D DD DD  STA $DDDD,X
$F860: DD D9 9B  CMP L_9BD9,X
$F863: B4 94     LDY $94,X
$F865: BB        db $BB
$F866: 99 DD DD  STA $DDDD,Y
$F869: D9 BB 9B  CMP L_9BBB,Y
$F86C: B9 DD DD  LDA $DDDD,Y
$F86F: BD DD 9B  LDA L_9BDD,X
$F872: BB        db $BB
$F873: 9D DD BD  STA L_BDDD,X
$F876: 9B        db $9B
$F877: DD DB BB  CMP L_BBDB,X
$F87A: DD DB 9D  CMP L_9DDB,X
$F87D: BD DD 68  LDA $68DD,X
$F880: B8        CLV
$F881: 6D DD BD  ADC L_BDDD
$F884: DD DD 9D  CMP L_9DDD,X
$F887: 6D 9D DD  ADC $DD9D
$F88A: DD DD D9  CMP $D9DD,X
$F88D: DD 9D D9  CMP $D99D,X
$F890: DD DD DD  CMP $DDDD,X
$F893: DD DD DD  CMP $DDDD,X
$F896: DD DD DD  CMP $DDDD,X
$F899: DD DD DD  CMP $DDDD,X
$F89C: DD DD DD  CMP $DDDD,X
$F89F: DD DD 9D  CMP L_9DDD,X
$F8A2: DD DD DD  CMP $DDDD,X
$F8A5: 9D DD DD  STA $DDDD,X
$F8A8: 9D 48 DD  STA $DD48,X
$F8AB: DD 0D DD  CMP $DD0D,X
$F8AE: DD 4D 4B  CMP $4B4D,X
$F8B1: D3        db $D3
$F8B2: 44        db $44
$F8B3: 4D DD DB  EOR $DBDD
$F8B6: BD 4B 02  LDA $024B,X
$F8B9: DD D9 9D  CMP L_9DD9,X
$F8BC: BB        db $BB
$F8BD: BB        db $BB
$F8BE: BB        db $BB
$F8BF: 44        db $44
$F8C0: 4D 04 DD  EOR $DD04
$F8C3: DD BB 11  CMP $11BB,X
$F8C6: 84 D0     STY $D0
$F8C8: 43        db $43
$F8C9: 0D 48 D1  ORA $D148
$F8CC: 33        db $33
$F8CD: DD D4 3D  CMP OAMDATA_3DD4,X
$F8D0: 0D 0D 14  ORA $140D
$F8D3: CC CC CC  CPY $CCCC
$F8D6: CC CD 0D  CPY $0DCD
$F8D9: 3D CC CC  AND $CCCC,X
$F8DC: CC CC CD  CPY $CDCC
$F8DF: DD 9D CC  CMP $CC9D,X
$F8E2: CC CC CC  CPY $CCCC
$F8E5: CD 4D 4D  CMP $4D4D
$F8E8: CC CC CC  CPY $CCCC
$F8EB: CC CD 0D  CPY $0DCD
$F8EE: 4D CC CC  EOR $CCCC
$F8F1: CC CC CD  CPY $CDCC
$F8F4: 0D 4D DD  ORA $DD4D
$F8F7: DD CC CC  CMP $CCCC,X
$F8FA: CD DD 3D  CMP PPUSCROLL_3DDD
$F8FD: DD DD DC  CMP $DCDD,X
$F900: CC CD DD  CPY $DDCD
$F903: D9 D4 D4  CMP $D4D4,Y
$F906: D4        db $D4
$F907: D9 DD D4  CMP $D4DD,Y
$F90A: D4        db $D4
$F90B: DD DD D9  CMP $D9DD,X
$F90E: DD DD D4  CMP $D4DD,X
$F911: D4        db $D4
$F912: DD 9D D9  CMP $D99D,X
$F915: D9 9D D4  CMP $D49D,Y
$F918: DD D4 D9  CMP $D9D4,X
$F91B: 4D DD 9D  EOR L_9DDD
$F91E: DD DD 44  CMP $44DD,X
$F921: D4        db $D4
$F922: 4D 9D DD  EOR $DD9D
$F925: DD 9D 4D  CMP $4D9D,X
$F928: D4        db $D4
$F929: 4D 44 DD  EOR $DD44
$F92C: 9D 9D D4  STA $D49D,X
$F92F: D9 DD 94  CMP L_94DD,Y
$F932: DD DD 44  CMP $44DD,X
$F935: D4        db $D4
$F936: DD D4 9D  CMP L_9DD4,X
$F939: DD D9 44  CMP $44D9,X
$F93C: D4        db $D4
$F93D: 4D 44 DD  EOR $DD44
$F940: 4D D4 DD  EOR $DDD4
$F943: D4        db $D4
$F944: 9D DD D4  STA $D4DD,X
$F947: 4D DD D4  EOR $D4DD
$F94A: D4        db $D4
$F94B: 49 D9     EOR #$D9
$F94D: DD 4D 4D  CMP $4D4D,X
$F950: 44        db $44
$F951: DD DD D4  CMP $D4DD,X
$F954: 9D DD 4D  STA $4DDD,X
$F957: 4D DD DD  EOR $DDDD
$F95A: D4        db $D4
$F95B: 44        db $44
$F95C: DD DD AA  CMP L_AADD,X
$F95F: DD DD DD  CMP $DDDD,X
$F962: DD DD 6D  CMP $6DDD,X
$F965: DA        db $DA
$F966: BD 2D DD  LDA $DD2D,X
$F969: DD DD B6  CMP L_B6DD,X
$F96C: DD DD 7D  CMP $7DDD,X
$F96F: 2D AA DD  AND $DDAA
$F972: BB        db $BB
$F973: D8        CLD
$F974: 10 DD     BPL L_F953
$F976: 7B        db $7B
$F977: AD DD BB  LDA L_BBDD
$F97A: BD D9 10  LDA $10D9,X
$F97D: DD DD 6D  CMP $6DDD,X
$F980: BB        db $BB
$F981: 86 D0     STX $D0
$F983: D9 1D D6  CMP $D61D,Y
$F986: BD B8 DD  LDA $DDB8,X
$F989: 39 D0 D8  AND $D8D0,Y
$F98C: DB        db $DB
$F98D: BD DD DD  LDA $DDDD,X
$F990: D2        db $D2
$F991: 39 DD BB  AND L_BBDD,Y
$F994: BD DD AB  LDA L_ABDD,X
$F997: 5D D2 36  EOR PPUSTATUS_36D2,X
$F99A: 8B        db $8B
$F99B: BD DA AD  LDA L_ADDA,X
$F99E: 0D 5D DD  ORA $DD5D
$F9A1: DD BD DD  CMP $DDBD,X
$F9A4: DD DD 0D  CMP $0DDD,X
$F9A7: BA        TSX
$F9A8: DD 8D 9D  CMP L_9D8D,X
$F9AB: DD DD DD  CMP $DDDD,X
$F9AE: DA        db $DA
$F9AF: AD DD 99  LDA L_99DD
$F9B2: DD DD DD  CMP $DDDD,X
$F9B5: DD DD 9D  CMP L_9DDD,X
$F9B8: DD DD 9D  CMP L_9DDD,X
$F9BB: DD DD DD  CMP $DDDD,X
$F9BE: DD 99 DD  CMP $DD99,X
$F9C1: 9D D9 9D  STA L_9DD9,X
$F9C4: DD DD D9  CMP $D9DD,X
$F9C7: DD 9D DD  CMP $DD9D,X
$F9CA: 9D 99 BD  STA L_BD99,X
$F9CD: D9 DD 99  CMP L_99DD,Y
$F9D0: 9D BD 9D  STA L_9DBD,X
$F9D3: DD D4 DD  CMP $DDD4,X
$F9D6: DD 9D 99  CMP L_999D,X
$F9D9: 9D DD B9  STA L_B9DD,X
$F9DC: 9D 94 94  STA L_9494,X
$F9DF: 4D DD DD  EOR $DDDD
$F9E2: DD 9B 9B  CMP L_9B9B,X
$F9E5: DD 4D D9  CMP $D94D,X
$F9E8: 9D DD 9D  STA L_9DDD,X
$F9EB: DB        db $DB
$F9EC: DD 9D D9  CMP $D99D,X
$F9EF: DD DD 4D  CMP $4DDD,X
$F9F2: D9 DD 99  CMP L_99DD,Y
$F9F5: 49 DD     EOR #$DD
$F9F7: B9 99 BB  LDA L_BB99,Y
$F9FA: 49 9D     EOR #$9D
$F9FC: 49 DD     EOR #$DD
$F9FE: DD D4 DD  CMP $DDD4,X
$FA01: DD BB D4  CMP $D4BB,X
$FA04: DD DD D9  CMP $D9DD,X
$FA07: DD DD DB  CMP $DBDD,X
$FA0A: D4        db $D4
$FA0B: DD DD D9  CMP $D9DD,X
$FA0E: DD DD D9  CMP $D9DD,X
$FA11: D4        db $D4
$FA12: DD DD DD  CMP $DDDD,X
$FA15: DD DD DD  CMP $DDDD,X
$FA18: 57        db $57
$FA19: DD DD DD  CMP $DDDD,X
$FA1C: DD 6D DD  CMP $DD6D,X
$FA1F: 9D DD DD  STA $DDDD,X
$FA22: DD D1 B1  CMP L_B1D1,X
$FA25: D4        db $D4
$FA26: 2D DD DD  AND $DDDD
$FA29: DD 6B BB  CMP L_BB6B,X
$FA2C: 64        db $64
$FA2D: 2D DD DD  AND $DDDD
$FA30: D1 BB     CMP ($BB),Y
$FA32: CB        db $CB
$FA33: B4 2D     LDY $2D,X
$FA35: DD DD 6B  CMP $6BDD,X
$FA38: BC CC BB  LDY L_BBCC,X
$FA3B: 2D DD D1  AND $D1DD
$FA3E: BB        db $BB
$FA3F: CC CC CB  CPY $CBCC
$FA42: B1 DD     LDA ($DD),Y
$FA44: 6B        db $6B
$FA45: BC CC CC  LDY $CCCC,X
$FA48: CC BB 6D  CPY $6DBB
$FA4B: BB        db $BB
$FA4C: CC CC CC  CPY $CCCC
$FA4F: CC CB BD  CPY L_BDCB
$FA52: DB        db $DB
$FA53: CC CC CC  CPY $CCCC
$FA56: CC CB DD  CPY $DDCB
$FA59: DB        db $DB
$FA5A: CC CC CC  CPY $CCCC
$FA5D: CC CB DD  CPY $DDCB
$FA60: DB        db $DB
$FA61: CC CD DD  CPY $DDCD
$FA64: CC CB DD  CPY $DDCB
$FA67: DB        db $DB
$FA68: CC DD DD  CPY $DDDD
$FA6B: DC        db $DC
$FA6C: CB        db $CB
$FA6D: DD DD DD  CMP $DDDD,X
$FA70: DD DD DD  CMP $DDDD,X
$FA73: 4D DD D4  EOR $D4DD
$FA76: AA        TAX
$FA77: D9 D4 DD  CMP $DDD4,Y
$FA7A: DD DD DD  CMP $DDDD,X
$FA7D: AA        TAX
$FA7E: 4B        db $4B
$FA7F: BB        db $BB
$FA80: AA        TAX
$FA81: D9 DD DD  CMP $DDDD,Y
$FA84: DD DB BB  CMP L_BBDB,X
$FA87: AA        TAX
$FA88: 4D DD D9  EOR $D9DD
$FA8B: DD AA DB  CMP $DBAA,X
$FA8E: DD DD DD  CMP $DDDD,X
$FA91: BB        db $BB
$FA92: 4D AA 9D  EOR L_9DAA
$FA95: DD D4 DD  CMP $DDD4,X
$FA98: BB        db $BB
$FA99: BD DD DD  LDA $DDDD,X
$FA9C: D9 DD 9D  CMP L_9DDD,Y
$FA9F: D4        db $D4
$FAA0: AA        TAX
$FAA1: D4        db $D4
$FAA2: DD DD DD  CMP $DDDD,X
$FAA5: DD 9D AA  CMP L_AA9D,X
$FAA8: BB        db $BB
$FAA9: AA        TAX
$FAAA: BB        db $BB
$FAAB: D4        db $D4
$FAAC: DD DD DD  CMP $DDDD,X
$FAAF: BD AA BB  LDA L_BBAA,X
$FAB2: AA        TAX
$FAB3: DD DD D9  CMP $D9DD,X
$FAB6: BD DD BB  LDA L_BBDD,X
$FAB9: AA        TAX
$FABA: DD DD 4D  CMP $4DDD,X
$FABD: 4D DD DD  EOR $DDDD
$FAC0: DD DD 4D  CMP $4DDD,X
$FAC3: DD DD DD  CMP $DDDD,X
$FAC6: D4        db $D4
$FAC7: 9D DD DD  STA $DDDD,X
$FACA: DD DD DD  CMP $DDDD,X
$FACD: DD DD DD  CMP $DDDD,X
$FAD0: DD DD D1  CMP $D1DD,X
$FAD3: 1D DD 6D  ORA $6DDD,X
$FAD6: DD D6 6D  CMP $6DD6,X
$FAD9: 1B        db $1B
$FADA: B6 D1     LDX $D1,Y
$FADC: B1 DD     LDA ($DD),Y
$FADE: 1B        db $1B
$FADF: B1 BB     LDA ($BB),Y
$FAE1: BB        db $BB
$FAE2: 1B        db $1B
$FAE3: BB        db $BB
$FAE4: 1D BB BB  ORA L_BBBB,X
$FAE7: BB        db $BB
$FAE8: BB        db $BB
$FAE9: BB        db $BB
$FAEA: BB        db $BB
$FAEB: BD 9B AB  LDA L_AB9B,X
$FAEE: BB        db $BB
$FAEF: BB        db $BB
$FAF0: AB        db $AB
$FAF1: BB        db $BB
$FAF2: BD BB AA  LDA L_AABB,X
$FAF5: AB        db $AB
$FAF6: BB        db $BB
$FAF7: AA        TAX
$FAF8: AB        db $AB
$FAF9: 9D BB BB  STA L_BBBB,X
$FAFC: AB        db $AB
$FAFD: 9B        db $9B
$FAFE: BB        db $BB
$FAFF: AB        db $AB
$FB00: BD BB BB  LDA L_BBBB,X
$FB03: BB        db $BB
$FB04: BB        db $BB
$FB05: BB        db $BB
$FB06: BB        db $BB
$FB07: BD BB BB  LDA L_BBBB,X
$FB0A: B3        db $B3
$FB0B: 3B        db $3B
$FB0C: BB        db $BB
$FB0D: BB        db $BB
$FB0E: 8D 8B BB  STA L_BB8B
$FB11: 3D D3 BB  AND L_BBD3,X
$FB14: B8        CLV
$FB15: DD D8 33  CMP PPUCTRL_33D8,X
$FB18: DD DD 33  CMP PPUSCROLL_33DD,X
$FB1B: 3D DD DD  AND $DDDD,X
$FB1E: DD DD DD  CMP $DDDD,X
$FB21: DD DD DD  CMP $DDDD,X
$FB24: DD DA DD  CMP $DDDA,X
$FB27: DD AD DD  CMP $DDAD,X
$FB2A: DD AA DA  CMP $DAAA,X
$FB2D: DA        db $DA
$FB2E: AA        TAX
$FB2F: AD AA AD  LDA L_ADAA
$FB32: BB        db $BB
$FB33: 4D D4 DD  EOR $DDD4
$FB36: AD AB AD  LDA L_ADAB
$FB39: BA        TSX
$FB3A: AA        TAX
$FB3B: AD 9D D4  LDA $D49D
$FB3E: BB        db $BB
$FB3F: BD BB DA  LDA $DABB,X
$FB42: DD AD AA  CMP L_AAAD,X
$FB45: AA        TAX
$FB46: BD AA DA  LDA $DAAA,X
$FB49: DA        db $DA
$FB4A: AD DA DD  LDA $DDDA
$FB4D: DD DD 4B  CMP $4BDD,X
$FB50: 4D 4B DA  EOR $DA4B
$FB53: DD AD DA  CMP $DAAD,X
$FB56: AB        db $AB
$FB57: AA        TAX
$FB58: AA        TAX
$FB59: DB        db $DB
$FB5A: 4D AD 4D  EOR $4DAD
$FB5D: D4        db $D4
$FB5E: DD AD BB  CMP L_BBAD,X
$FB61: AD AD AA  LDA L_AAAD
$FB64: DA        db $DA
$FB65: AD A4 AA  LDA L_AAA4
$FB68: AD DD DD  LDA $DDDD
$FB6B: 4D BB DD  EOR $DDBB
$FB6E: BA        TSX
$FB6F: DD AD DA  CMP $DAAD,X
$FB72: AA        TAX
$FB73: BD DD DA  LDA $DADD,X
$FB76: DA        db $DA
$FB77: AD DA DD  LDA $DDDA
$FB7A: DD DD DD  CMP $DDDD,X
$FB7D: DD DD CC  CMP $CCDD,X
$FB80: CC CC CC  CPY $CCCC
$FB83: CC CC CD  CPY $CDCC
$FB86: CC CC CC  CPY $CCCC
$FB89: CC CC CC  CPY $CCCC
$FB8C: CD CC C4  CMP $C4CC
$FB8F: CC CC C4  CPY $C4CC
$FB92: CC CD C4  CPY $C4CD
$FB95: D4        db $D4
$FB96: D4        db $D4
$FB97: C4 D4     CPY $D4
$FB99: D4        db $D4
$FB9A: CD C3 34  CMP OAMADDR_34C3
$FB9D: DD DD D4  CMP $D4DD,X
$FBA0: 33        db $33
$FBA1: CD CC C4  CMP $C4CC
$FBA4: 14        db $14
$FBA5: 94 14     STY $14,X
$FBA7: CC CD 9C  CPY L_9CCD
$FBAA: CC D8 D8  CPY $D8D8
$FBAD: DC        db $DC
$FBAE: CC 9D CC  CPY $CC9D
$FBB1: CC D1 D1  CPY $D1D1
$FBB4: DC        db $DC
$FBB5: CC CD CC  CPY $CCCD
$FBB8: CC D4 D4  CPY $D4D4
$FBBB: DC        db $DC
$FBBC: CC CD CC  CPY $CCCD
$FBBF: C4 DD     CPY $DD
$FBC1: 1D D4 CC  ORA $CCD4,X
$FBC4: CD C4 C4  CMP $C4C4
$FBC7: D8        CLD
$FBC8: 88        DEY
$FBC9: D4        db $D4
$FBCA: C4 CD     CPY $CD
$FBCC: D4        db $D4
$FBCD: 14        db $14
$FBCE: DD DD D4  CMP $D4DD,X
$FBD1: 14        db $14
$FBD2: DD D3 DD  CMP $DDD3,X
$FBD5: DD DD DD  CMP $DDDD,X
$FBD8: D3        db $D3
$FBD9: DD DD DD  CMP $DDDD,X
$FBDC: 9D DD D9  STA $D9DD,X
$FBDF: DD DD D9  CMP $D9DD,X
$FBE2: DD D9 DD  CMP $DDD9,X
$FBE5: 9B        db $9B
$FBE6: BD DD DD  LDA $DDDD,X
$FBE9: 9D DD D9  STA $D9DD,X
$FBEC: B6 7D     LDX $7D,Y
$FBEE: DD DD D9  CMP $D9DD,X
$FBF1: DB        db $DB
$FBF2: BB        db $BB
$FBF3: BB        db $BB
$FBF4: D5 DD     CMP $DD,X
$FBF6: D7        db $D7
$FBF7: DD 9B B9  CMP L_B99B,X
$FBFA: BD D9 DD  LDA $DDD9,X
$FBFD: D8        CLD
$FBFE: 7B        db $7B
$FBFF: D9 BB 9D  CMP L_9DBB,Y
$FC02: D5 DD     CMP $DD,X
$FC04: DD BB BB  CMP L_BBBB,X
$FC07: BD D9 DD  LDA $DDD9,X
$FC0A: DD D6 7B  CMP $7BD6,X
$FC0D: D9 BD DD  CMP $DDBD,Y
$FC10: 9D DD DB  STA $DBDD,X
$FC13: BB        db $BB
$FC14: 9D 9D 6D  STA $6D9D,X
$FC17: D9 DD BB  CMP L_BBDD,Y
$FC1A: B9 DD DD  LDA $DDDD,Y
$FC1D: 5D DD DD  EOR $DDDD,X
$FC20: DD 9D DD  CMP $DD9D,X
$FC23: DD DD D5  CMP $D5DD,X
$FC26: 9D DD DD  STA $DDDD,X
$FC29: DD DD D6  CMP $D6DD,X
$FC2C: 7D DD 7D  ADC $7DDD,X
$FC2F: 6D DD DD  ADC $DDDD
$FC32: DD DD DD  CMP $DDDD,X
$FC35: DD DD 20  CMP PPUSCROLL_20DD,X
$FC38: DD DD DD  CMP $DDDD,X
$FC3B: DD 22 20  CMP PPUSTATUS_2022,X
$FC3E: D2        db $D2
$FC3F: DD 22 DD  CMP $DD22,X
$FC42: DD 22 24  CMP PPUSTATUS_2422,X
$FC45: 4D DD 24  EOR PPUSCROLL_24DD
$FC48: 2D DD 00  AND $00DD
$FC4B: D4        db $D4
$FC4C: 2D D0 24  AND PPUCTRL_24D0
$FC4F: 4D DD D2  EOR $D2DD
$FC52: D4        db $D4
$FC53: 02        db $02
$FC54: D2        db $D2
$FC55: 44        db $44
$FC56: 4D DD D2  EOR $D2DD
$FC59: 0D D4 24  ORA OAMDATA_24D4
$FC5C: 00        BRK
$FC5D: 4D DD D2  EOR $D2DD
$FC60: DD 04 42  CMP $4204,X
$FC63: D2        db $D2
$FC64: 4D DD D0  EOR $D0DD
$FC67: DD 24 42  CMP $4224,X
$FC6A: D2        db $D2
$FC6B: 4D DD D0  EOR $D0DD
$FC6E: 33        db $33
$FC6F: D4        db $D4
$FC70: 44        db $44
$FC71: D2        db $D2
$FC72: 23        db $23
$FC73: 4D D0 DD  EOR $DDD0
$FC76: 02        db $02
$FC77: 40        RTI
$FC78: 22        db $22
$FC79: 20 0D DD  JSR L_DD0D
$FC7C: 2D 40 24  AND PPUCTRL_2440
$FC7F: 4D D0 DD  EOR $DDD0
$FC82: DD 20 2D  CMP PPUCTRL_2D20,X
$FC85: DD 42 D2  CMP $D242,X
$FC88: DD DD 20  CMP PPUSCROLL_20DD,X
$FC8B: DD DD D4  CMP $D4DD,X
$FC8E: 4D DD DD  EOR $DDDD
$FC91: DD DD DD  CMP $DDDD,X
$FC94: DD DD DD  CMP $DDDD,X
$FC97: DD DD 4D  CMP $4DDD,X
$FC9A: 4D DD DD  EOR $DDDD
$FC9D: DD BD DB  CMP $DBBD,X
$FCA0: 4B        db $4B
$FCA1: 4B        db $4B
$FCA2: DD BD DD  CMP $DDBD,X
$FCA5: 4B        db $4B
$FCA6: B4 44     LDY $44,X
$FCA8: 44        db $44
$FCA9: BB        db $BB
$FCAA: 4B        db $4B
$FCAB: DD 44 44  CMP $4444,X
$FCAE: 94 94     STY $94,X
$FCB0: 44        db $44
$FCB1: 4B        db $4B
$FCB2: DD AA A4  CMP L_A4AA,X
$FCB5: 44        db $44
$FCB6: 44        db $44
$FCB7: AA        TAX
$FCB8: AB        db $AB
$FCB9: DD A4 44  CMP $44A4,X
$FCBC: 44        db $44
$FCBD: 44        db $44
$FCBE: 44        db $44
$FCBF: AA        TAX
$FCC0: BD 44 4A  LDA $4A44,X
$FCC3: 44        db $44
$FCC4: 4A        LSR A
$FCC5: 44        db $44
$FCC6: 4B        db $4B
$FCC7: BD 44 AA  LDA L_AA44,X
$FCCA: A4 AA     LDY $AA
$FCCC: A4 4A     LDY $4A
$FCCE: AD BA AB  LDA L_ABBA
$FCD1: BB        db $BB
$FCD2: BB        db $BB
$FCD3: AA        TAX
$FCD4: BA        TSX
$FCD5: BD DB BD  LDA L_BDDB,X
$FCD8: DD DD BB  CMP L_BBDD,X
$FCDB: DB        db $DB
$FCDC: DD DD DD  CMP $DDDD,X
$FCDF: DD DD DD  CMP $DDDD,X
$FCE2: DD DD DD  CMP $DDDD,X
$FCE5: DD DD DD  CMP $DDDD,X
$FCE8: DD DD DD  CMP $DDDD,X
$FCEB: DD DD DD  CMP $DDDD,X
$FCEE: DD DD DD  CMP $DDDD,X
$FCF1: DD 6D DD  CMP $DD6D,X
$FCF4: DD 6D DD  CMP $DD6D,X
$FCF7: DD 6D DD  CMP $DD6D,X
$FCFA: DD DD DD  CMP $DDDD,X
$FCFD: DD DD DD  CMP $DDDD,X
$FD00: DD DD DD  CMP $DDDD,X
$FD03: DD DD DD  CMP $DDDD,X
$FD06: DD DD DD  CMP $DDDD,X
$FD09: DD DD DD  CMP $DDDD,X
$FD0C: DD DD DD  CMP $DDDD,X
$FD0F: DD DD DD  CMP $DDDD,X
$FD12: DD DD DD  CMP $DDDD,X
$FD15: DD DD DD  CMP $DDDD,X
$FD18: DD DD DD  CMP $DDDD,X
$FD1B: DD DD DD  CMP $DDDD,X
$FD1E: DD DD DD  CMP $DDDD,X
$FD21: DD DD DD  CMP $DDDD,X
$FD24: DD DD DD  CMP $DDDD,X
$FD27: DD DD DD  CMP $DDDD,X
$FD2A: BD DD DD  LDA $DDDD,X
$FD2D: DD DD DD  CMP $DDDD,X
$FD30: BD BB DD  LDA $DDBB,X
$FD33: DD DD DD  CMP $DDDD,X
$FD36: DB        db $DB
$FD37: BD 9B BD  LDA L_BD9B,X
$FD3A: DD DD DD  CMP $DDDD,X
$FD3D: BB        db $BB
$FD3E: 9D 99 BB  STA L_BB99,X
$FD41: DD DD DB  CMP $DBDD,X
$FD44: B9 9D FF  LDA $FF9D,Y
$FD47: FF        db $FF
$FD48: FF        db $FF
$FD49: FF        db $FF
$FD4A: FF        db $FF
$FD4B: FF        db $FF
$FD4C: FF        db $FF
$FD4D: FF        db $FF
$FD4E: FF        db $FF
$FD4F: FF        db $FF
$FD50: 2E 2E 2E  ROL PPUADDR_2E2E
$FD53: 2E 2E 2E  ROL PPUADDR_2E2E
$FD56: 2E 2E 2E  ROL PPUADDR_2E2E
$FD59: 2E 2E 2E  ROL PPUADDR_2E2E
$FD5C: 2E 2E 2E  ROL PPUADDR_2E2E
$FD5F: 2E 2E 2E  ROL PPUADDR_2E2E
$FD62: 2E 40 2E  ROL PPUCTRL_2E40
$FD65: 2E 2E 2E  ROL PPUADDR_2E2E
$FD68: 2E 2E 2E  ROL PPUADDR_2E2E
$FD6B: 40        RTI
$FD6C: 40        RTI
$FD6D: 40        RTI
$FD6E: 40        RTI
$FD6F: 2E 40 40  ROL $4040
$FD72: 40        RTI
$FD73: 40        RTI
$FD74: 40        RTI
$FD75: 40        RTI
$FD76: 40        RTI
$FD77: 2E 2E 2E  ROL PPUADDR_2E2E
$FD7A: 40        RTI
$FD7B: 2E 2E 40  ROL $402E
$FD7E: 2E 2E 2E  ROL PPUADDR_2E2E
$FD81: 2E 2E 40  ROL $402E
$FD84: 2E 2E 2E  ROL PPUADDR_2E2E
$FD87: 2E 2E 40  ROL $402E
$FD8A: 2E 2E 40  ROL $402E
$FD8D: 2E 2E 2E  ROL PPUADDR_2E2E
$FD90: 2E 2E 40  ROL $402E
$FD93: 2E 40 2E  ROL PPUCTRL_2E40
$FD96: 2E 2E 2E  ROL PPUADDR_2E2E
$FD99: 2E 2E 40  ROL $402E
$FD9C: 2E 40 2E  ROL PPUCTRL_2E40
$FD9F: 2E 40 40  ROL $4040
$FDA2: 2E 2E 2E  ROL PPUADDR_2E2E
$FDA5: 40        RTI
$FDA6: 40        RTI
$FDA7: 2E 2E 40  ROL $402E
$FDAA: 40        RTI
$FDAB: 2E 2E 2E  ROL PPUADDR_2E2E
$FDAE: 40        RTI
$FDAF: 40        RTI
$FDB0: 2E 2E 2E  ROL PPUADDR_2E2E
$FDB3: 2E 2E 2E  ROL PPUADDR_2E2E
$FDB6: 2E 2E 2E  ROL PPUADDR_2E2E
$FDB9: 2E 2E 2E  ROL PPUADDR_2E2E
$FDBC: 2E 2E 2E  ROL PPUADDR_2E2E
$FDBF: 2E 2E 2E  ROL PPUADDR_2E2E
$FDC2: 2E 2E 2E  ROL PPUADDR_2E2E
$FDC5: 40        RTI
$FDC6: 2E 40 40  ROL $4040
$FDC9: 40        RTI
$FDCA: 40        RTI
$FDCB: 40        RTI
$FDCC: 40        RTI
$FDCD: 40        RTI
$FDCE: 2E 2E 2E  ROL PPUADDR_2E2E
$FDD1: 2E 2E 2E  ROL PPUADDR_2E2E
$FDD4: 40        RTI
$FDD5: 2E 2E 40  ROL $402E
$FDD8: 2E 2E 2E  ROL PPUADDR_2E2E
$FDDB: 2E 2E 40  ROL $402E
$FDDE: 2E 2E 2E  ROL PPUADDR_2E2E
$FDE1: 2E 2E 40  ROL $402E
$FDE4: 2E 2E 2E  ROL PPUADDR_2E2E
$FDE7: 40        RTI
$FDE8: 40        RTI
$FDE9: 40        RTI
$FDEA: 40        RTI
$FDEB: 40        RTI
$FDEC: 40        RTI
$FDED: 40        RTI
$FDEE: 2E 2E 2E  ROL PPUADDR_2E2E
$FDF1: 2E 40 2E  ROL PPUCTRL_2E40
$FDF4: 40        RTI
$FDF5: 2E 2E 2E  ROL PPUADDR_2E2E
$FDF8: 2E 2E 40  ROL $402E
$FDFB: 2E 2E 2E  ROL PPUADDR_2E2E
$FDFE: 2E 2E 2E  ROL PPUADDR_2E2E
$FE01: 40        RTI
$FE02: 2E 2E 40  ROL $402E
$FE05: 2E 40 40  ROL $4040
$FE08: 40        RTI
$FE09: 40        RTI
$FE0A: 40        RTI
$FE0B: 40        RTI
$FE0C: 40        RTI
$FE0D: 40        RTI
$FE0E: 40        RTI
$FE0F: 2E 2E 2E  ROL PPUADDR_2E2E
$FE12: 2E 2E 40  ROL $402E
$FE15: 2E 2E 2E  ROL PPUADDR_2E2E
$FE18: 40        RTI
$FE19: 2E 40 2E  ROL PPUCTRL_2E40
$FE1C: 40        RTI
$FE1D: 2E 2E 2E  ROL PPUADDR_2E2E
$FE20: 2E 2E 2E  ROL PPUADDR_2E2E
$FE23: 2E 40 2E  ROL PPUCTRL_2E40
$FE26: 2E 40 2E  ROL PPUCTRL_2E40
$FE29: 2E 40 2E  ROL PPUCTRL_2E40
$FE2C: 2E 40 2E  ROL PPUCTRL_2E40
$FE2F: 2E 2E 2E  ROL PPUADDR_2E2E
$FE32: 2E 2E 40  ROL $402E
$FE35: 2E 40 2E  ROL PPUCTRL_2E40
$FE38: 2E 2E 40  ROL $402E
$FE3B: 2E 2E 2E  ROL PPUADDR_2E2E
$FE3E: 40        RTI
$FE3F: 2E 2E 2E  ROL PPUADDR_2E2E
$FE42: 2E 2E 2E  ROL PPUADDR_2E2E
$FE45: 2E 2E 2E  ROL PPUADDR_2E2E
$FE48: 2E 2E 2E  ROL PPUADDR_2E2E
$FE4B: 2E 2E 2E  ROL PPUADDR_2E2E
$FE4E: 2E 2E 2E  ROL PPUADDR_2E2E
$FE51: 2E 2E 2E  ROL PPUADDR_2E2E
$FE54: 40        RTI
$FE55: 2E 2E 2E  ROL PPUADDR_2E2E
$FE58: 2E 2E 2E  ROL PPUADDR_2E2E
$FE5B: 2E 2E 2E  ROL PPUADDR_2E2E
$FE5E: 2E 2E 40  ROL $402E
$FE61: 40        RTI
$FE62: 40        RTI
$FE63: 40        RTI
$FE64: 40        RTI
$FE65: 40        RTI
$FE66: 40        RTI
$FE67: 40        RTI
$FE68: 2E 40 40  ROL $4040
$FE6B: 40        RTI
$FE6C: 40        RTI
$FE6D: 40        RTI
$FE6E: 40        RTI
$FE6F: 40        RTI
$FE70: 40        RTI
$FE71: 2E 2E 2E  ROL PPUADDR_2E2E
$FE74: 2E 2E 2E  ROL PPUADDR_2E2E
$FE77: 40        RTI
$FE78: 2E 40 2E  ROL PPUCTRL_2E40
$FE7B: 2E 40 2E  ROL PPUCTRL_2E40
$FE7E: 2E 40 2E  ROL PPUCTRL_2E40
$FE81: 40        RTI
$FE82: 40        RTI
$FE83: 40        RTI
$FE84: 40        RTI
$FE85: 40        RTI
$FE86: 40        RTI
$FE87: 2E 2E 40  ROL $402E
$FE8A: 2E 2E 40  ROL $402E
$FE8D: 2E 2E 40  ROL $402E
$FE90: 2E 2E 2E  ROL PPUADDR_2E2E
$FE93: 2E 40 2E  ROL PPUCTRL_2E40
$FE96: 2E 2E 2E  ROL PPUADDR_2E2E
$FE99: 40        RTI
$FE9A: 40        RTI
$FE9B: 40        RTI
$FE9C: 40        RTI
$FE9D: 40        RTI
$FE9E: 40        RTI
$FE9F: 40        RTI
$FEA0: 2E 40 40  ROL $4040
$FEA3: 40        RTI
$FEA4: 40        RTI
$FEA5: 40        RTI
$FEA6: 40        RTI
$FEA7: 2E 2E 40  ROL $402E
$FEAA: 2E 2E 40  ROL $402E
$FEAD: 2E 2E 40  ROL $402E
$FEB0: 2E 2E 2E  ROL PPUADDR_2E2E
$FEB3: 2E 40 2E  ROL PPUCTRL_2E40
$FEB6: 2E 2E 2E  ROL PPUADDR_2E2E
$FEB9: 40        RTI
$FEBA: 2E 2E 40  ROL $402E
$FEBD: 2E 2E 40  ROL $402E
$FEC0: 2E 2E 40  ROL $402E
$FEC3: 40        RTI
$FEC4: 40        RTI
$FEC5: 2E 2E 2E  ROL PPUADDR_2E2E
$FEC8: 2E 40 40  ROL $4040
$FECB: 40        RTI
$FECC: 40        RTI
$FECD: 40        RTI
$FECE: 40        RTI
$FECF: 40        RTI
$FED0: 2E 2E 2E  ROL PPUADDR_2E2E
$FED3: 2E 2E 2E  ROL PPUADDR_2E2E
$FED6: 2E 2E 2E  ROL PPUADDR_2E2E
$FED9: 2E 2E 2E  ROL PPUADDR_2E2E
$FEDC: 2E 2E 2E  ROL PPUADDR_2E2E
$FEDF: 2E 2E 2E  ROL PPUADDR_2E2E
$FEE2: 2E 40 2E  ROL PPUCTRL_2E40
$FEE5: 2E 2E 2E  ROL PPUADDR_2E2E
$FEE8: 2E 2E 2E  ROL PPUADDR_2E2E
$FEEB: 2E 2E 40  ROL $402E
$FEEE: 2E 2E 2E  ROL PPUADDR_2E2E
$FEF1: 2E 2E 40  ROL $402E
$FEF4: 2E 2E 2E  ROL PPUADDR_2E2E
$FEF7: 2E 40 2E  ROL PPUCTRL_2E40
$FEFA: 2E 2E 2E  ROL PPUADDR_2E2E
$FEFD: 40        RTI
$FEFE: 2E 2E 2E  ROL PPUADDR_2E2E
$FF01: 2E 2E 40  ROL $402E
$FF04: 2E 2E 2E  ROL PPUADDR_2E2E
$FF07: 2E 40 2E  ROL PPUCTRL_2E40
$FF0A: 2E 2E 2E  ROL PPUADDR_2E2E
$FF0D: 40        RTI
$FF0E: 2E 2E 2E  ROL PPUADDR_2E2E
$FF11: 2E 2E 40  ROL $402E
$FF14: 2E 2E 2E  ROL PPUADDR_2E2E
$FF17: 2E 40 2E  ROL PPUCTRL_2E40
$FF1A: 2E 2E 2E  ROL PPUADDR_2E2E
$FF1D: 40        RTI
$FF1E: 2E 2E 2E  ROL PPUADDR_2E2E
$FF21: 2E 2E 40  ROL $402E
$FF24: 2E 2E 2E  ROL PPUADDR_2E2E
$FF27: 2E 40 2E  ROL PPUCTRL_2E40
$FF2A: 2E 2E 2E  ROL PPUADDR_2E2E
$FF2D: 40        RTI
$FF2E: 2E 2E 2E  ROL PPUADDR_2E2E
$FF31: 2E 40 2E  ROL PPUCTRL_2E40
$FF34: 2E 2E 2E  ROL PPUADDR_2E2E
$FF37: 2E 40 2E  ROL PPUCTRL_2E40
$FF3A: 2E 2E 2E  ROL PPUADDR_2E2E
$FF3D: 40        RTI
$FF3E: 2E 2E 2E  ROL PPUADDR_2E2E
$FF41: 40        RTI
$FF42: 2E 2E 2E  ROL PPUADDR_2E2E
L_FF45:
$FF45: 2E 2E 2E  ROL PPUADDR_2E2E
$FF48: 2E 2E 2E  ROL PPUADDR_2E2E
$FF4B: 40        RTI
$FF4C: 40        RTI
$FF4D: 40        RTI
$FF4E: 2E 2E FF  ROL $FF2E
$FF51: FF        db $FF
$FF52: FF        db $FF
$FF53: FF        db $FF
$FF54: FF        db $FF
$FF55: FF        db $FF
$FF56: FF        db $FF
$FF57: FF        db $FF
$FF58: FF        db $FF
$FF59: FF        db $FF
$FF5A: FF        db $FF
$FF5B: FF        db $FF
$FF5C: FF        db $FF
$FF5D: FF        db $FF
$FF5E: FF        db $FF
$FF5F: FF        db $FF
$FF60: FF        db $FF
$FF61: FF        db $FF
$FF62: FF        db $FF
$FF63: FF        db $FF
$FF64: FF        db $FF
$FF65: FF        db $FF
$FF66: FF        db $FF
$FF67: FF        db $FF
$FF68: FF        db $FF
$FF69: FF        db $FF
$FF6A: FF        db $FF
$FF6B: FF        db $FF
$FF6C: FF        db $FF
$FF6D: FF        db $FF
$FF6E: FF        db $FF
$FF6F: FF        db $FF
$FF70: FF        db $FF
$FF71: FF        db $FF
$FF72: FF        db $FF
$FF73: FF        db $FF
$FF74: FF        db $FF
$FF75: FF        db $FF
$FF76: FF        db $FF
$FF77: FF        db $FF
$FF78: FF        db $FF
$FF79: FF        db $FF
$FF7A: FF        db $FF
$FF7B: FF        db $FF
$FF7C: FF        db $FF
$FF7D: FF        db $FF
$FF7E: FF        db $FF
$FF7F: FF        db $FF
$FF80: FF        db $FF
$FF81: FF        db $FF
$FF82: FF        db $FF
$FF83: FF        db $FF
$FF84: FF        db $FF
$FF85: FF        db $FF
$FF86: FF        db $FF
$FF87: FF        db $FF
$FF88: FF        db $FF
$FF89: FF        db $FF
$FF8A: FF        db $FF
$FF8B: FF        db $FF
$FF8C: FF        db $FF
$FF8D: FF        db $FF
$FF8E: FF        db $FF
$FF8F: FF        db $FF
$FF90: FF        db $FF
$FF91: FF        db $FF
$FF92: FF        db $FF
$FF93: FF        db $FF
$FF94: FF        db $FF
$FF95: FF        db $FF
$FF96: FF        db $FF
$FF97: FF        db $FF
$FF98: FF        db $FF
$FF99: FF        db $FF
$FF9A: FF        db $FF
$FF9B: FF        db $FF
$FF9C: FF        db $FF
$FF9D: FF        db $FF
$FF9E: FF        db $FF
$FF9F: FF        db $FF
$FFA0: FF        db $FF
$FFA1: FF        db $FF
$FFA2: FF        db $FF
$FFA3: FF        db $FF
$FFA4: FF        db $FF
$FFA5: FF        db $FF
$FFA6: FF        db $FF
$FFA7: FF        db $FF
$FFA8: FF        db $FF
$FFA9: FF        db $FF
$FFAA: FF        db $FF
$FFAB: FF        db $FF
$FFAC: FF        db $FF
$FFAD: FF        db $FF
$FFAE: FF        db $FF
$FFAF: FF        db $FF
$FFB0: FF        db $FF
$FFB1: FF        db $FF
$FFB2: FF        db $FF
$FFB3: FF        db $FF
$FFB4: FF        db $FF
$FFB5: FF        db $FF
$FFB6: FF        db $FF
$FFB7: FF        db $FF
$FFB8: FF        db $FF
$FFB9: FF        db $FF
$FFBA: FF        db $FF
$FFBB: FF        db $FF
$FFBC: FF        db $FF
$FFBD: FF        db $FF
L_FFBE:
$FFBE: FF        db $FF
$FFBF: FF        db $FF
L_FFC0:
$FFC0: FF        db $FF
$FFC1: FF        db $FF
$FFC2: FF        db $FF
$FFC3: FF        db $FF
$FFC4: FF        db $FF
$FFC5: FF        db $FF
$FFC6: FF        db $FF
$FFC7: FF        db $FF
$FFC8: FF        db $FF
$FFC9: FF        db $FF
$FFCA: FF        db $FF
$FFCB: FF        db $FF
$FFCC: FF        db $FF
$FFCD: FF        db $FF
$FFCE: FF        db $FF
$FFCF: FF        db $FF
$FFD0: FF        db $FF
$FFD1: FF        db $FF
$FFD2: FF        db $FF
$FFD3: FF        db $FF
$FFD4: FF        db $FF
$FFD5: FF        db $FF
$FFD6: FF        db $FF
$FFD7: FF        db $FF
$FFD8: FF        db $FF
$FFD9: FF        db $FF
$FFDA: FF        db $FF
$FFDB: FF        db $FF
$FFDC: FF        db $FF
$FFDD: FF        db $FF
$FFDE: FF        db $FF
$FFDF: FF        db $FF
$FFE0: FF        db $FF
$FFE1: FF        db $FF
$FFE2: FF        db $FF
$FFE3: FF        db $FF
$FFE4: FF        db $FF
$FFE5: FF        db $FF
$FFE6: FF        db $FF
$FFE7: FF        db $FF
$FFE8: FF        db $FF
$FFE9: FF        db $FF
$FFEA: FF        db $FF
$FFEB: FF        db $FF
$FFEC: FF        db $FF
$FFED: FF        db $FF
$FFEE: FF        db $FF
$FFEF: FF        db $FF
$FFF0: FF        db $FF
$FFF1: FF        db $FF
$FFF2: FF        db $FF
$FFF3: FF        db $FF
$FFF4: FF        db $FF
$FFF5: FF        db $FF
$FFF6: FF        db $FF
$FFF7: FF        db $FF
$FFF8: FF        db $FF
$FFF9: FF        db $FF

; CPU vectors are 16-bit addresses stored low byte first, not instructions.
$FFFA: 00 D4     dw NMI                ; NMI vector: NMI ($D400)
$FFFC: 70 C0     dw ResetEntry         ; Reset vector: ResetEntry ($C070)
$FFFE: 70 C0     dw ResetEntry         ; IRQ/BRK vector: ResetEntry ($C070)

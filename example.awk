#!/usr/bin/awk -f

# Matches first three tab-separated columns, merging same-keyed
# lines onto a single line.
# WARNING: lines that don't match three-tab pattern are NOT echoed.

BEGIN {
  f1 = ""
; f2 = ""
; f3 = ""
; line = ""
}
/(^[^	]*	[^	]*	[^	]*	)/ {
  if ( (f1 == $1) && (f2 == $2) && (f3 == $3) ) {
    line = line "	" $0
  } else {
     f1 = $1
    ;f2 = $2
    ;f3 = $3
    ;print line
    ;line = $0
  }
}
END { print line }

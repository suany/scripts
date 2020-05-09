#!/usr/bin/awk -f

# Remember values of first two tab-separated non-empty columns;
# then fills in those values for rows whose first two columns
# are # empty.

BEGIN {
    FS = "	"
  ; col1 = ""
  ; col2 = ""
}
/(^[^	]+	[^	]+	)/ {
    col1 = $1
    col2 = $2
  ; print
}
/(^		)/ {
    sub("		", col1 "	" col2 "	", $0)
  ; print
}

#!/usr/bin/awk -f

BEGIN { state = -1 }
/^#/ { state = 0; next }
{ if(state != -1) { state++; print } }
END { exit state }

: "\
@sh.exe %0 %* \
@exit      \
"

# NOTE: The above four lines are a handy way for cmd to call sh on this same
#       file, with the only caveat being that an additional argument '\' is
#       appended to the end of the argument list.

case "$1" in
  ""|'\')
    echo No args
    ;;
  *)
    echo Arg $1
    ;;
esac

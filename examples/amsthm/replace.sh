#!/bin/bash

# getopts

## reset getopts
OPTIND=1

## Initialize parameters
TRIM=false
delete_originals=false

## get the options
while getopts "f:t:" opt; do
	case "$opt" in
	f)	replace_from=$OPTARG
		;;
	t)	replace_to=$OPTARG
		;;
	esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

##Capitalize first letter
Replace_from="$(tr '[:lower:]' '[:upper:]' <<< ${replace_from:0:1})${replace_from:1}"
Replace_to="$(tr '[:lower:]' '[:upper:]' <<< ${replace_to:0:1})${replace_to:1}"

## check
echo 'I am going to replace '$replace_from' to '$replace_to ' and'
echo 'I am going to replace '$Replace_from' to '$Replace_to

# Replacement

## get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
# ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.

## copy
cp "$@" "$replace_to.$EXT"

## replace
sed -i '' s/$replace_from/$replace_to/g "$replace_to.$EXT"
sed -i '' s/$Replace_from/$Replace_to/g "$replace_to.$EXT"
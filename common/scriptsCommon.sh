resetColor() {
    printf "\e[39m"
}
turnRed() {
    printf "\e[31m"
}
turnGreen() {
    printf "\e[32m"
}
printError() {
    local errorText=$1
    turnRed
    echo $errorText
    resetColor
}
printInfo() {
    turnGreen
    echo $1
    resetColor
}
terminate() {
    exit 1
}
checkDirExist() {
    local directoryPath=$1
    if [[ -d $directoryPath ]] ; then
        printInfo "Found directory: $directoryPath"
    else
        printError "Can't find mandatory directory: $directoryPath"
        terminate
    fi
}
checkFileExist() {
    local filePath=$1
    if [[ -f $filePath ]] ; then
        printInfo "Found file: $filePath"
    else
        printError "Can't find mandatory file: $filePath"
        terminate
    fi
}

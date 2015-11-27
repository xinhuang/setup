$download = "$pwd\download"
$log = "$pwd\log"
$bin = "$pwd\bin"

function mk-dir($path) {
    if (Test-Path -path $path -pathType Container) {
        return
    }
    mkdir $path
}

function download($url, $path) {
    Invoke-WebRequest $url -OutFile $path
}

function install-msi($path) {
    $filename = Split-Path -path $path -leaf
    msiexec /i $path /passive /qb /norestart /log $log\install_$filename.log
}

mk-dir $download
mk-dir $log

download "https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi" "$download\python-2.7.10.msi"
install-msi "$download\python-2.7.10.msi"

$download = "$pwd\download"
$log = "$pwd\log"

mkdir $download
mkdir $log

Invoke-WebRequest https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi -OutFile $download\python-2.7.10.msi
msiexec /i download\python-2.7.10.msi /passive /qb /norestart /log log\install_python-2.7.10.log

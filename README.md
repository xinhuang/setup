# My Machine Setup Scripts

## Usage

For Windows, use `powershell -File init.ps1`.

For Linux, use `sudo bash init.sh`.

## Software List

### General

> Python 2.7.10  
> Easy Setup  
> Pip
> git

### Linux

> apt-fast
> Ruby

### Windows

> choco

## Package Definition JSON Format

```
{
  "name": "apt-fast",
  "dependencies": [],
  "installation": {
    "linux": {
      "apt": { "repo": ["ppa:saiarcot895/myppa"] },
      "post-install": {
        <!-- New services can be added like this. Modifying existing service is also allowed. -->
        "services": {
          "apt": {
            <!-- {name} will be the package name -->
            "install": "apt-fast -y install {name}"
          }
        }
      }
    }
    <!-- There is no apt-fast for Windows. This is just for demostration purpose -->
    "windows": {
      "url": "http://some-url",
      <!-- {path} will be the package download path -->
      "command": "cmd /c {path} {name}",
      "post-install": {
        "services": {
          "url": {
            <!-- {value} will be the entire value of the entry -->
            "install": "flashget {value}"
          }
        }
      }
    }
  }
}
```

